from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy import or_
from selenium import webdriver
import concurrent.futures
import time
import requests
import json
import settings
import schedule
from bs4 import BeautifulSoup
import fbchat
from fbchat import Client
from fbchat.models import *
from getpass import getpass

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler



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
    print("Starting NSE Scrape...  ")
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
        for words in settings.BLACKLIST_NSE_WORDS:
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
    print("NSE scrape done")
    return in_stock

def scrape_gardino():
    print("Starting Gardino Scrape...  ")
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

    driver.get("https://gardinonursery.com/product-category/categories/hoyas/hoyas-full-list/")

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
        for words in settings.BLACKLIST_GARDINO_WORDS:
            if words in name_id.lower():
                avoid = False
                break
        if listing is None and avoid:

            listing = Listing(
                link=instock_url,
                name=name_id,
                source="gardino",
            )

            session.add(listing)
            session.commit()

            in_stock.append(["gardino",name_id,instock_url])
    print("Gardino scrape done")
    return in_stock


def scrape_logee():
    print("Starting Logees Scrape...")
    in_stock = []
    isItInStock = []

    for each_item in settings.LOGEES_SEARCH:
        s = requests.session()
        #s.get(each_item)
        try:
            page = s.get(each_item, timeout=30, headers=settings.HEADER)
        except:
            print("Connection failure to logees.com")
        else:
            page_source = page.content

            soup = BeautifulSoup(page_source, 'lxml')
            try:
                isInStock = soup.find_all('p', class_='availability in-stock')
                name_id = soup.find('div', class_='product-name').get_text()
            except:
                print("Logees: Elements not found")
            else:
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
    print("Logees scrape done")
    return in_stock

def scrape_gabriella():
    print("Starting Gabriella Scrape...")

    in_stock = []
    isItInStock = []

    for each_item in settings.GABRIELLA_SEARCH:
        s = requests.session()
        #s.get(each_item)
        try:
            page = s.get(each_item, timeout=30, headers=settings.HEADER)
        except:
            print("Connection failure to gabriellaplants.com")
        else:
            page_source = page.content

            soup = BeautifulSoup(page_source, 'lxml')
            #isInStock = soup.find_all('div', class_='availability value_in')
            try:
                isInStock = soup.find_all('button', class_='single_add_to_cart_button')
                name_id = "blank"
                name_id = soup.find('h1', class_='product_title entry-title').get_text()
            except:
                print("Gabriella: Elements not found")
            else:
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
    print("Gabriella Scrape Done")
    return in_stock

def scrape_USPT():
    print("Starting UnsolicitedPlantTalk Scrape...")

    in_stock = []
    isItInStock = []

    for each_item in settings.USPT_SEARCH:
        s = requests.session()
        #s.get(each_item)
        try:
            page = s.get(each_item, timeout=30, headers=settings.HEADER)
        except:
            print("Connection failure to unsolicitedplanttalk.com")
        else:
            page_source = page.content
            soup = BeautifulSoup(page_source, 'lxml')
            try:
                isInStock = soup.find_all('article', class_='sold-out')
                name_id = "blank"
                name_id = soup.find('h1', class_='ProductItem-details-title').get_text()
            except:
                print("USPT: Elements not found")

            else:
                listing = session.query(Listing).filter_by(link= each_item).first()
                if(len(isInStock)==0):
                    isItInStock.append(['USPT',name_id,each_item])
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
                source="USPT",
            )

            session.add(listing)
            session.commit()

            in_stock.append(["USPT",name_id,instock_url])
    print("USPT Scrape Done")
    return in_stock

def scrape_aloha():
    print("Starting Aloha Scrape...")

    in_stock = []
    isItInStock = []

    for each_item in settings.ALOHA_SEARCH:
        s = requests.session()
        #s.get(each_item)
        try:
            page = s.get(each_item, timeout=30, headers=settings.HEADER)
        except:
            print("Connection failure to peaceofaloha.com")
        else:
            page_source = page.content

            soup = BeautifulSoup(page_source, 'lxml')
            #isInStock = soup.find_all('div', class_='availability value_in')
            try:
               # isInStock = soup.find_all('span', class_='buttonnext1499656494__content')
                isInStock = soup.find_all('button', {"data-hook":"add-to-cart","aria-disabled": "false"})
                name_id = "blank"
                #name_id = soup.find('h1', class_='product_title entry-title').get_text()
                name_id = soup.find('h1', {"data-hook":"product-title"}).get_text()
            except:
                print("Aloha: Elements not found")
                
            else:
                listing = session.query(Listing).filter_by(link= each_item).first()
                if(len(isInStock)>0):
                    isItInStock.append(['aloha',name_id,each_item])
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
                source="aloha",
            )

            session.add(listing)
            session.commit()

            in_stock.append(["aloha",name_id,instock_url])
    print("Aloha Scrape Done")
    return in_stock

def fb_message(results):
    client = fbchat.Client('plantscraper@gmail.com','PlantBot510') 
    for result in results:
        source = result[0]
        plant = result[1]
        url = result[2]

    #username = str(raw_input("Username: ")) 
        messageString = source + " has restocked on: " + plant + "\n\n" + url
        # friends = client.searchForUsers("darren jian")  # return a list of names 
        # friend = friends[0] 
        # client.send(Message(text=messageString), thread_id=friend.uid, thread_type=ThreadType.USER)
        client.send(Message(text=messageString), thread_id="3091592367572794", thread_type=ThreadType.GROUP)

    client.logout()

def slack_message(results): 
    print("Sending Slack Message")
    for result in results:
        source = result[0]
        plant = result[1]
        url = result[2]

        messageString = source + " has restocked on: " + plant + "\n" + url +"\n~~~~~~~~~~~~~~~~~~~"

        data = {
            'text': messageString,
            'username': 'Planty Bot',
            'icon_emoji': ':seedling:'
        }

        response = requests.post(settings.WEBHOOK_URL, data=json.dumps(data), headers={'Content-Type':'application/json'}) 

        #print('Response: ' + str(response.text))


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
        options.add_argument("start-maximized")
        options.add_argument("enable-automation")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-browser-side-navigation")
        options.add_argument("--disable-gpu")
        driver = webdriver.Chrome("../chromedriver", options=options)

        driver.get(past_instock.link)

        page_source = driver.page_source
        driver.quit()


        soup = BeautifulSoup(page_source, 'lxml')
        in_stock = []
        #instocks_selector = soup.find_all('li', class_='instock product-type-simple')
        instocks_selector = soup.select('div.instock.product-type-simple')
        if len(instocks_selector) == 0:
            session.delete(past_instock)
    for past_instock in session.query(Listing).filter_by(source="gardino"):
        print(past_instock.link)

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

def do_scrape():
    # nse_results = scrape_nse()
    # gardino_results = scrape_gardino()
    # logee_results = scrape_logee()
    # gabriella_results = scrape_gabriella()
    # aloha_results = scrape_aloha()
    # USPT_results = scrape_USPT()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        f1 = executor.submit(scrape_nse)
        f2 = executor.submit(scrape_gardino)
        f3 = executor.submit(scrape_logee)
        f4 = executor.submit(scrape_gabriella)
        f5 = executor.submit(scrape_aloha)
        f6 = executor.submit(scrape_USPT)

        nse_results = f1.result()
        gardino_results = f2.result()
        logee_results = f3.result()
        gabriella_results = f4.result()
        aloha_results = f5.result()
        USPT_results = f6.result()

        output = nse_results + logee_results + gabriella_results + gardino_results + aloha_results + USPT_results
        if len(output)>0:
            #fb_message(results)
            slack_message(output)
        update_listing()
        #update_gardino_listing()

if __name__ == "__main__":
    # schedule.every().minute.at(":00").do(do_scrape)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)

    # sched = BackgroundScheduler(daemon=True)
    # sched.add_job(do_scrape, 'cron',minute='*')
    # sched.start()

    scheduler = BlockingScheduler()
    #trigger = 
    scheduler.add_job(do_scrape, 'cron', hour='6-21',minute='*',second='0')
    print('Press Ctrl+{0} to exit'.format('C'))
    try:
        scheduler.start()
    except (SystemExit):
        pass
    except (KeyboardInterrupt):
        exit


