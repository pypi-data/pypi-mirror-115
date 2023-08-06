import requests

#TODO make this seperate module to capsulate

class MovieInfo:
    def __init__(self, json):
        self.imdb_id: str = json["imdb_id"]
        self.title: str = json["title"]
        self.year: int = int(json["year"])
        
        try:
            self.slug: str = json["slug"]
        except KeyError:
            self.slug = None

        try:
            self.type: str = json["type"]
        except KeyError:
            self.type = None

        self.synopsis: str = json["synopsis"]
        self.runtime: int = float(json["runtime"])
        self.rating = {
            "percentage": float(json["rating"]["percentage"]),
            "watching": float(json["rating"]["watching"]),
            "votes": float(json["rating"]["votes"]),
        }
        #TODO fix but causes problems cause sub dict keys can be null
        # self.images = {
        #     "banner": json["images"]["banner"],
        #     "fanart": json["images"]["fanart"],
        #     "poster": json["images"]["poster"],
        # }
        self.genres = json["genres"]
        try:
            self.language:str = json["language"]
        except KeyError:
            self.language = None
        self.released:int = json["released"]
        self.trailer:str = json["trailer"]
        self.certification:str = json["certification"]

        self.torrents = {}
        try:
            self.torrents["1080p"] = {
                "provider": json["torrents"]["en"]["1080p"]["provider"],
                "filesize": json["torrents"]["en"]["1080p"]["filesize"],
                "size": json["torrents"]["en"]["1080p"]["size"],
                "peer": json["torrents"]["en"]["1080p"]["peer"],
                "seed": json["torrents"]["en"]["1080p"]["seed"],
                "url": json["torrents"]["en"]["1080p"]["url"]
            }
        except (KeyError, TypeError) as e:
            pass
        try:
            self.torrents["720p"] = {
                "provider": json["torrents"]["en"]["720p"]["provider"],
                "filesize": json["torrents"]["en"]["720p"]["filesize"],
                "size": json["torrents"]["en"]["720p"]["size"],
                "peer": json["torrents"]["en"]["720p"]["peer"],
                "seed": json["torrents"]["en"]["720p"]["seed"],
                "url": json["torrents"]["en"]["720p"]["url"]
            }
        except (KeyError, TypeError) as e:
            pass

class UnknownMovieError(Exception):
    def __init__(self, message):
        super(UnknownMovieError, self).__init__(message)

class PopcornTimeApi:
    def __init__(self):
        # all previous servers dead
        # use community provided russian alternative for now
        self.base_url = "https://popcorn-ru.tk"

    def get_random(self):
        r = requests.get(self.base_url + "/random/movie")
        json = r.json()
        # TODO http error handling if server is down throw error or something
        return MovieInfo(json)

    def get_details(self, imdb_id:str):
        r = requests.get(self.base_url + "/movie/" + imdb_id)
        if len(r.text) == 0:
            raise UnknownMovieError("No movie found with imdb id: " + imdb_id)
        json = r.json()
        return MovieInfo(json)
