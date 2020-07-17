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

instock_url = "https://www.gabriellaplants.com/collections/home-page/products/4-white-butterfly-syngonium"
notinstock_url = "https://www.gabriellaplants.com/collections/philodendron/products/4-pink-princess-philodendron"
s = requests.session()
s.get(instock_url)
page = s.get(instock_url)
page_source = page.content


print('webscraping...')
soup = BeautifulSoup(page_source, 'lxml')
in_stock = []
instocks_selector = soup.find_all('div', class_='availability value_in')
print(instocks_selector)
print("Is it in stock?: " + str(len(instocks_selector)>0))
name_id = soup.find('h1', class_='product_title entry-title')
print(name_id)

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