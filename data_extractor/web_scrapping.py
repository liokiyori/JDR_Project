from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dateutil import parser
import time

class Webscraping_recuperator:

    def __init__(self, url):
        self.url = url

    def recup_data(self):
        # Configuration

        # Lancer le navigateur Selenium
        options = webdriver.ChromeOptions()
        browser = webdriver.Chrome(options=options)

        browser.get(self.url)

        # Attendre que la page se charge
        time.sleep(5)

        # Récupérer le contenu HTML
        html_content = browser.page_source
        browser.quit()

        # Parser avec BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Trouver tous les éléments <li> contenant des articles
        li_elements = soup.find_all("li")

        # Initialiser une liste pour stocker les données
        data = []

        # Parcourir chaque élément <li>
        for li in li_elements:
            article = li.find("article")  # Cherche la balise <article> dans chaque <li>
            if not article:
                continue  # Si pas d'article, on passe au suivant
            
            # Extraire le titre
            title_element = article.find("div", class_="post-excerpt__title")
            title = title_element.get_text(strip=True) if title_element else "N/A"
            
            # Extraire le lien
            link_element = title_element.find("a") if title_element else None
            link_url = link_element['href'] if link_element else "N/A"

            # Extraire la date
            time_element = article.find("time")
            published_date = time_element.get_text(strip=True) if time_element else "N/A"

            # Formater la date
            try:
                if "ago" in published_date:
                    if "days ago" in published_date:
                        days_ago = int(published_date.split()[0])
                        published_date = datetime.now() - timedelta(days=days_ago)
                    elif "hours ago" in published_date:
                        hours_ago = int(published_date.split()[0])
                        published_date = datetime.now() - timedelta(hours=hours_ago)
                else:
                    published_date = parser.parse(published_date)
            except ValueError:
                published_date = None
            
            # Ajouter les données extraites à la liste
            data.append({
                "title": title,
                "link": link_url,
                "published_date": published_date
            })
        return data