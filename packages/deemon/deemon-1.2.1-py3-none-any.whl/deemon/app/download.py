from pathlib import Path

import plexapi.exceptions
from plexapi.server import PlexServer
from deemon.app import dmi
from deemon.app import Deemon
import logging
import deezer
import sys

logger = logging.getLogger(__name__)


class QueueItem:

    def __init__(self, artist=None, album=None, url=None, playlist=None):
        if artist:
            self.artist_name = artist["name"]
            self.album_id = album["id"]
            self.album_title = album["title"]
            self.url = album["link"]
        if url:
            self.artist_name = None
            self.url = url
            self.playlist_name = playlist


class Download(Deemon):

    def __init__(self):
        super().__init__()
        self.dz = deezer.Deezer()
        self.di = dmi.DeemixInterface()
        self.queue_list = []
        self.bitrate = self.config["bitrate"]
        self.record_type = self.config["record_type"]

        if not self.di.login():
            sys.exit(1)

    def get_plex_server(self):
        baseurl = self.config["plex_baseurl"]
        token = self.config["plex_token"]
        if (baseurl != "") and (token != ""):
            try:
                print("Plex settings found, trying to connect... ", end="")
                plex_server = PlexServer(baseurl, token, timeout=10)
                print(" OK")
                return plex_server
            except Exception:
                print(" FAILED")
                logger.error("Error: Unable to reach Plex server, please refresh manually.")
                return False

    def download_queue(self, queue):
        if queue:
            plex = self.get_plex_server()
            num_queued = len(queue)
            print("----------------------------")
            logger.info("Sending " + str(num_queued) + " release(s) to deemix for download:")

            for q in queue:
                logger.debug(f"Queued: {vars(q)}")
                if q.artist_name:
                    logger.info(f"+ {q.artist_name} - {q.album_title}... ")
                else:
                    logger.info(f"+ Updating playlist: {q.playlist_name}...")
                logger.debug(f"bitrate set to {self.bitrate}")
                self.di.download_url([q.url], self.bitrate)

            print("")
            logger.info("Downloads complete!")
            if plex:
                try:
                    plex.library.section(self.config["plex_library"]).update()
                    logger.debug("Plex library refreshed successfully")
                except plexapi.exceptions.BadRequest as e:
                    logger.error("Error occurred while refreshing your library. See logs for additional info.")
                    logger.debug(f"Error during Plex refresh: {e}")

    def add_to_queue(self, artist, album):
        for _album in album['data']:
            if (self.record_type == _album["record_type"]) or (self.record_type == "all"):
                logger.debug(f"QUEUE: Adding '{_album['title']}' to queue...")
                artist["bitrate"] = self.bitrate
                self.queue_list.append(QueueItem(artist, _album))

    def download(self, opt: dict):
        logger.debug("download called with options: " + str(opt))
        artist = {}

        if opt["bitrate"]:
            self.bitrate = opt["bitrate"]
        if opt["record_type"]:
            self.record_type = opt["record_type"]

        if opt["url"]:
            logger.info("Sending URL to deemix for processing:")
            self.di.download_url([opt["url"]], opt["bitrate"])

        if opt["file"]:
            logger.info(f"Reading from file {opt['file']}")
            if Path(opt['file']).exists():
                with open(opt['file'], 'r', encoding="utf8", errors="replace") as f:
                    make_csv = f.read().replace('\n', ',')
                    csv_to_list = make_csv.split(',')
                    artist_list = sorted(list(filter(None, csv_to_list)))
                    for name in artist_list:
                        try:
                            artist = self.dz.api.search_artist(name, limit=1)['data'][0]
                            album = self.dz.api.get_artist_albums(artist["id"])
                            self.add_to_queue(artist, album)
                            logger.info(f"Artist `{name}` added to queue")
                        except IndexError:
                            logger.warning(f"Artist '{name}' not found")

        if opt["artist_id"] or opt["artist"]:
            if opt["artist_id"]:
                artist = self.dz.api.get_artist(opt["artist_id"])
            elif opt["artist"]:
                artist = self.dz.api.search_artist(opt["artist"], limit=1)['data'][0]
                opt["artist_id"] = artist["id"]

            album = self.dz.api.get_artist_albums(opt["artist_id"])
            self.add_to_queue(artist, album)

        if opt["album_id"]:
            album = {'data': [self.dz.api.get_album(opt["album_id"])]}
            artist["name"] = album["data"][0]["artist"]["name"]
            self.add_to_queue(artist, album)

        self.download_queue(self.queue_list)
        self.db.commit()
