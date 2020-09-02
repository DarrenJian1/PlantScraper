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

instock_url = "https://unsolicitedplanttalks.com/plants/p/jd8y7vfbjggp7tmw7kmbd0z7j13sl5"
notinstock_url = "https://unsolicitedplanttalks.com/plants/p/hx8z321rys2val7jjuh0brhts13ax6"
s = requests.session()
page = s.get(instock_url, headers=settings.HEADER)
print(page)
page_source = page.content


print('webscraping...')
soup = BeautifulSoup(page_source, 'lxml')
in_stock = []
instocks_selector = soup.find_all('article', class_='sold-out')
print(instocks_selector)
print("Is it in stock?: " + str(len(instocks_selector)==0))
name_id = soup.find('h1', class_='ProductItem-details-title')
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