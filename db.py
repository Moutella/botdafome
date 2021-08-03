from configparser import ConfigParser
from datetime import datetime
import pymongo


class olist_db:
    def __init__(self, url=None):
        if url:
            self.client = pymongo.MongoClient(url)
        else:
            config = ConfigParser()
            config.read('.config')
            self.client = pymongo.MongoClient(config["DATABASE"]['url'])

    def add_availability(self):
        self.client.olistbot.dynconfigs.insert_one({
            "available": False,
            "name": "availability",
            "time": datetime.utcnow()
        })

    def get_availability(self):
        dado = self.client.olistbot.dynconfigs.find_one({
            "name": "availability"
        })

        return dado

    def set_availability(self, available):
        query = {"name": "availability"}
        values = {"$set": {"available": available, "time": datetime.utcnow()}}
        self.client.olistbot.dynconfigs.update_one(query, values)


if __name__ == "__main__":
    db = olist_db()
    # db.add_availability()
    db.set_availability(True)
    dado = db.get_availability()
    print(dado)
