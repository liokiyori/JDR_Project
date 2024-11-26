from pymongo import MongoClient

def connection_db():
    client = MongoClient("mongodb://root:example@localhost:27017/")
    article_db = client["articles_db"]
    return article_db