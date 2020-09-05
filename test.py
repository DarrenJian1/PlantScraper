from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.orm import sessionmaker
from selenium import webdriver
import time
import requests
import settings
from bs4 import BeautifulSoup
import fbchat
from fbchat import Client
from fbchat.models import *
from getpass import getpass

print("Starting Ken Scrape...  ")
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
options.add_argument("start-maximized")
options.add_argument("enable-automation")
options.add_argument("--no-sandbox")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-browser-side-navigation")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome("../chromedriver", options=options)

driver.get("https://kensphilodendrons.com/shop/")

page_source = driver.page_source
driver.quit()


soup = BeautifulSoup(page_source, 'lxml')
in_stock = []
#instocks_selector = soup.find_all('li', class_='instock product-type-simple')
instocks_selector = soup.select('div.product-type-simple')

for instock_selector in instocks_selector:
    avoid = True
    name_id = instock_selector.find('p', class_='woocommerce-loop-product__title').get_text()
    instock_url = instock_selector.find('a')['href']
    print(name_id)
    print(instock_url)
    # listing = session.query(Listing).filter_by(link= instock_url).first()
    # for words in settings.BLACKLIST_KEN_WORDS:
    #     if words in name_id.lower():
    #         avoid = False
    #         break
    # if listing is None and avoid:

    #     listing = Listing(
    #         link=instock_url,
    #         name=name_id,
    #         source="kensphilodendrons",
    #     )

    #     session.add(listing)
    #     session.commit()

    #     in_stock.append(["kensphilodendrons",name_id,instock_url])
print("Ken scrape done")

#############
#############

# instock_url = "https://unsolicitedplanttalks.com/plants/p/jd8y7vfbjggp7tmw7kmbd0z7j13sl5"
# notinstock_url = "https://unsolicitedplanttalks.com/plants/p/hx8z321rys2val7jjuh0brhts13ax6"
# s = requests.session()
# page = s.get(instock_url, headers=settings.HEADER)
# print(page)
# page_source = page.content


# print('webscraping...')
# soup = BeautifulSoup(page_source, 'lxml')
# in_stock = []
# instocks_selector = soup.find_all('article', class_='sold-out')
# print(instocks_selector)
# print("Is it in stock?: " + str(len(instocks_selector)==0))
# name_id = soup.find('h1', class_='ProductItem-details-title')
# print(name_id)

#########
##########

# for instock_selector in instocks_selector:
#     avoid = True
#     name_id = instock_selector.find('h2', class_='woocommerce-loop-product__title').get_text()
#     listing = session.query(Listing).filter_by(name= name_id).first()
#     for words in settings.BLACKLIST_WORDS:
#         if words in name_id.lower():
#             avoid = False
#             break
#     if listing is None and avoid:
#         instock_name = instock_selector.find('h2', class_='woocommerce-loop-product__title').get_text()
#         instock_url = instock_selector.find('a')['href']
#         print(instock_url)

#         listing = Listing(
#             link=instock_url,
#             name=instock_name,
#             source="logees",
#         )

#         session.add(listing)
#         session.commit()

#         in_stock.append(["logees",instock_name,instock_url])
        
# return in_stock