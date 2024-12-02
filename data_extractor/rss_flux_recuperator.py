import feedparser
from datetime import datetime

class RSSFlux_recuperator:
    def __init__(self):
        pass

    def recup_flux_rss(self, url):
        
        flux = feedparser.parse(url)

        if flux.bozo:
            print("Erreur de parsing du flux RSS")
            return None
        articles = []
        for entree in flux.entries:
            try:
                published_date = datetime.strptime(entree.published, '%a, %d %b %Y %H:%M:%S %z')
            except ValueError:
                published_date = "N/A"
            article = {
                "title": entree.title,
                "link": entree.link,
                "published_date": published_date
            }
            articles.append(article)

        return articles
