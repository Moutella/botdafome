from datetime import datetime
import requests

from db import olist_db
from simple_twitter_bot import SimpleTwitterBot


def main():
    product_link = "https://www.meli.lojaolist.com.br/MLB-1919043357-gift-card-virtual-ifood-pague-r10-e-ganhe-r15-_JM"
    value = requests.get(product_link)
    configs = olist_db()
    last_available = configs.get_availability()
    current_available = not 'pausado' in str(value.content)
    print(last_available)
    bot = SimpleTwitterBot()
    if not last_available['available'] and current_available:
        configs.set_availability(True)

        bot.tweet(f"O cupom ifood R$15 por R$10 voltou! {product_link}")
    elif last_available['available'] and not current_available:
        configs.set_availability(False)


if __name__ == "__main__":
    main()
