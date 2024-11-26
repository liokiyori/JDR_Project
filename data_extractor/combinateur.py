import os
from dotenv import load_dotenv
from rss_flux_recuperator import RSSFlux_recuperator
from web_scrapping import Webscraping_recuperator
from pymongo import MongoClient

load_dotenv()

def save_to_mongo(articles):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["articles_db"]
    collection = db["articles"]
    for article in articles:
        if not collection.find_one({"link": article["link"]}):
            collection.insert_one(article)

if __name__ == "__main__":
    rss_url = os.environ.get("rss_url")
    web_url = os.environ.get("web_url")

    rss_recuperator = RSSFlux_recuperator()
    web_recuperator = Webscraping_recuperator(web_url)

    rss_articles = rss_recuperator.recup_flux_rss(rss_url)
    web_articles = web_recuperator.recup_data()
    print(rss_articles)
    print("-" * 50)
    print(web_articles)

    all_articles = (rss_articles or []) + (web_articles or [])

    save_to_mongo(all_articles)