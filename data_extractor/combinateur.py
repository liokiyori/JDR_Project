import os
from dotenv import load_dotenv
from rss_flux_recuperator import RSSFlux_recuperator
from web_scrapping import Webscraping_recuperator
from pymongo import MongoClient
from datetime import datetime

load_dotenv()
user = os.environ.get("user_name")
password = os.environ.get("user_password")


class Combinator:
    def __init__(self):
        self.client = MongoClient(
            f"mongodb://{user}:{password}@localhost:27017/")
        self.db = self.client["articles_db"]
        self.collection = self.db["articles"]

    def initialize_db(self):
        if "articles" not in self.db.list_collection_names():
            self.db.create_collection("articles")
            print("Collection 'articles' créée dans la base de données 'articles_db'.")
        else:
            print(
                "La collection 'articles' existe déjà dans la base de données 'articles_db'.")

    def save_to_mongo(self, articles):
        for article in articles:
            if not self.collection.find_one({"link": article["link"]}):
                self.collection.insert_one(article)
                print(f"Enregistré : {article['title']}")
            else:
                print(f"Déjà existant : {article['title']}")


if __name__ == "__main__":
    rss_url = os.environ.get("rss_url")
    web_url = os.environ.get("web_url")

    combinator = Combinator()
    combinator.initialize_db()

    rss_recuperator = RSSFlux_recuperator()
    web_recuperator = Webscraping_recuperator(web_url)
    try:
        rss_articles = rss_recuperator.recup_flux_rss(rss_url)
        web_articles = web_recuperator.recup_data()
        all_articles = (rss_articles or []) + (web_articles or [])
    except Exception as e:
        print(f"Erreur lors de la récupération des articles : {e}")

    combinator.save_to_mongo(all_articles)
