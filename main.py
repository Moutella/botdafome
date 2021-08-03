from datetime import datetime
import requests

from db import olist_db
from simple_twitter_bot import SimpleTwitterBot


def main():
    product_links = ["https://www.meli.lojaolist.com.br/MLB-1919043357-gift-card-virtual-ifood-pague-r10-e-ganhe-r15-_JM",
                     "https://oliststoresp.mercadoshops.com.br/MLB-1957034504-gift-card-virtual-ifood-pague-r10-e-ganhe-r15-_JM"]
    for product_link in product_links:
        value = requests.get(product_link)
        configs = olist_db()
        last_available = configs.get_availability(product_link)
        current_available = not 'pausado' in str(value.content)
        print(last_available)
        bot = SimpleTwitterBot()
        if not last_available['available'] and current_available:
            configs.set_availability(product_link, True)

            bot.tweet(
                f"O cupom iFood R$15 por R$10 voltou! {product_link} - {datetime.now()}")
        elif last_available['available'] and not current_available:
            configs.set_availability(product_link, False)


if __name__ == "__main__":
    main()
