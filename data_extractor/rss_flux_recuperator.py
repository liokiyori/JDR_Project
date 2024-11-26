import feedparser

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
            article = {
                "title": entree.title,
                "link": entree.link,
                "published_date": entree.published
            }
            articles.append(article)

        return articles
