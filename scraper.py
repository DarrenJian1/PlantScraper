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



engine = create_engine('sqlite:///listings.db', echo=False)
Base = declarative_base()

class Listing(Base):
    """
    A table to store data on craigslist listings.
    """

    __tablename__ = 'listings'
    id = Column(Integer, primary_key=True)
    link = Column(String, unique=True)
    name = Column(String, unique=True)
    source = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def scrape_nse():

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome("./chromedriver", options=options)

    driver.get("https://www.nsetropicals.com/shop/")

    page_source = driver.page_source
    driver.quit()


    soup = BeautifulSoup(page_source, 'lxml')
    in_stock = []
    #instocks_selector = soup.find_all('li', class_='instock product-type-simple')
    instocks_selector = soup.select('li.instock.product-type-simple')

    for instock_selector in instocks_selector:
        avoid = True
        name_id = instock_selector.find('h2', class_='woocommerce-loop-product__title').get_text()
        instock_url = instock_selector.find('a')['href']
        listing = session.query(Listing).filter_by(link= instock_url).first()
        for words in settings.BLACKLIST_WORDS:
            if words in name_id.lower():
                avoid = False
                break
        if listing is None and avoid:

            listing = Listing(
                link=instock_url,
                name=name_id,
                source="nsetropicals",
            )

            session.add(listing)
            session.commit()

            in_stock.append(["nsetropicals",name_id,instock_url])
            
    return in_stock


def scrape_logee():

    in_stock = []
    isItInStock = []

    for each_item in settings.LOGEES_SEARCH:
        s = requests.session()
        s.get(each_item)
        page = s.get(each_item)
        page_source = page.content

        soup = BeautifulSoup(page_source, 'lxml')
        isInStock = soup.find_all('p', class_='availability in-stock')
        name_id = soup.find('div', class_='product-name').get_text()
        listing = session.query(Listing).filter_by(link= each_item).first()
        if(len(isInStock)>0):
            isItInStock.append(['logees',name_id,each_item])
        elif listing:
            print("Logee Scraping: deleting " + listing.name)
            session.delete(listing)
            session.commit()

    for in_stock_item in isItInStock:
        name_id = in_stock_item[1]
        instock_url = in_stock_item[2]
        listing = session.query(Listing).filter_by(link= instock_url).first()
        if listing is None:

            listing = Listing(
                link=instock_url,
                name=name_id,
                source="logees",
            )

            session.add(listing)
            session.commit()

            in_stock.append(["logees",name_id,instock_url])
            
    return in_stock

def scrape_gabriella():

    in_stock = []
    isItInStock = []

    for each_item in settings.GABRIELLA_SEARCH:
        s = requests.session()
        s.get(each_item)
        page = s.get(each_item)
        page_source = page.content

        soup = BeautifulSoup(page_source, 'lxml')
        isInStock = soup.find_all('div', class_='availability value_in')
        name_id = soup.find('h1', class_='product_title entry-title').get_text()
        listing = session.query(Listing).filter_by(link= each_item).first()
        if(len(isInStock)>0):
            isItInStock.append(['gabriellaplants',name_id,each_item])
        elif listing:
            listing = session.query(Listing).filter_by(link= each_item).first()
            session.delete(listing)
            session.commit()

    for in_stock_item in isItInStock:
        name_id = in_stock_item[1]
        instock_url = in_stock_item[2]
        listing = session.query(Listing).filter_by(link= instock_url).first()
        if listing is None:

            listing = Listing(
                link=instock_url,
                name=name_id,
                source="gabriellaplants",
            )

            session.add(listing)
            session.commit()

            in_stock.append(["gabriellaplants",name_id,instock_url])
            
    return in_stock

def fb_message(results):
    client = fbchat.Client('') 
    for result in results:
        source = result[0]
        plant = result[1]
        url = result[2]

    #username = str(raw_input("Username: ")) 
        messageString = source + " has restocked on: " + plant + "\n\n" + url
        #friends = client.searchForUsers("darren jian")  # return a list of names 
        #friend = friends[0] 
        #client.send(Message(text=messageString), thread_id=friend.uid, thread_type=ThreadType.USER)
        client.send(Message(text=messageString), thread_id="3091592367572794", thread_type=ThreadType.GROUP)

    client.logout()

def do_scrape():
    nse_results = scrape_nse()
    logee_results = scrape_logee()
    gabriella_results = scrape_gabriella()
    results = nse_results + logee_results + gabriella_results
    if len(results)>0:
        fb_message(results)
    update_listing()



    #Test Deleting an element in our session query
    # listing = session.query(Listing).filter_by(link="https://www.nsetropicals.com/product/variegated-ficus-triangularis/").first()
    # session.delete(listing)
    # session.commit()
    
def update_listing():
    for past_instock in session.query(Listing).filter_by(source="nsetropicals"):
        print(past_instock.link)

        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        driver = webdriver.Chrome("./chromedriver", options=options)

        driver.get(past_instock.link)

        page_source = driver.page_source
        driver.quit()


        soup = BeautifulSoup(page_source, 'lxml')
        in_stock = []
        #instocks_selector = soup.find_all('li', class_='instock product-type-simple')
        instocks_selector = soup.select('div.instock.product-type-simple')

        if len(instocks_selector) == 0:
            session.delete(past_instock)
    session.commit()
    #listing = session.query(Listing).filter_by(source="nsetropicals")
    #print(listing.all())


