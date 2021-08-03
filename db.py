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

    def add_availability(self, product_link):
        self.client.olistbot.dynconfigs.insert_one({
            "available": False,
            "name": product_link,
            "time": datetime.utcnow()
        })

    def get_availability(self, product_link):
        dado = self.client.olistbot.dynconfigs.find_one({
            "name": product_link
        })
        if not dado:
            self.add_availability(product_link)

        return dado

    def set_availability(self, product_link, available):
        query = {"name": product_link}
        values = {"$set": {"available": available, "time": datetime.utcnow()}}
        self.client.olistbot.dynconfigs.update_one(query, values)


if __name__ == "__main__":
    db = olist_db()
    # db.add_availability()
    dado = db.get_availability(
        "https://www.meli.lojaolist.com.br/MLB-1919043357-gift-card-virtual-ifood-pague-r10-e-ganhe-r15-_JM")
    print(dado)
