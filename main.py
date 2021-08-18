import re
import requests

from pytz import timezone
from datetime import datetime
from bs4 import BeautifulSoup

from simple_twitter_bot import SimpleTwitterBot
from db import olist_db


def main():
    # product_links = ["https://www.meli.lojaolist.com.br/MLB-1919043357-gift-card-virtual-ifood-pague-r10-e-ganhe-r15-_JM",
    #                  "https://oliststoresp.mercadoshops.com.br/MLB-1957034504-gift-card-virtual-ifood-pague-r10-e-ganhe-r15-_JM"]

    product_links = ["https://www.meli.lojaolist.com.br/MLB-1944495270-whisky-old-virginia-bourbon-6-anos-700ml-_JM#reco_item_pos=2&reco_backend=machinaxlis-seller-items&reco_backend_type=function&reco_client=vip-seller_items_above-shops&reco_id=3709d7dd-14de-4b48-8855-f27277baba55"]
    for product_link in product_links:
        value = requests.get(product_link)
        configs = olist_db()
        last_available = configs.get_availability(product_link)
        current_available = not 'pausado' in str(value.content)
        soup = BeautifulSoup(value.content, 'html.parser')
        title = soup.select_one(".ui-pdp-title").getText()
        qty_elem = soup.select_one(
            ".ui-pdp-buybox__quantity__available")
        qty = 0
        if qty_elem:
            qty_str = qty_elem.getText()
            qty = re.findall(r'\d+', qty_str)
            if qty:
                qty = qty[0]
        bot = SimpleTwitterBot()
        if not last_available['available'] and current_available:
            configs.set_availability(product_link, True, qty)
            # configs.set_availability(product_link, True)
            br = timezone("America/Sao_Paulo")
            date = datetime.now(timezone('UTC')).astimezone(br)
            bot.tweet(
                f"{title}\n[{qty} disponíveis]\n{date}\n{product_link}")
        elif last_available['available'] and not current_available:
            configs.set_availability(product_link, False)


if __name__ == "__main__":
    main()
