from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Configuration
url = "https://www.dndbeyond.com/posts"

# Lancer le navigateur Selenium
options = webdriver.ChromeOptions()
browser = webdriver.Chrome(options=options)

browser.get(url)

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
    
    # Extraire l'image
    image_element = article.find("a", class_="post-excerpt__preview-link")
    if image_element and 'style' in image_element.attrs:
        image_url = image_element['style'].split('url(')[1].split(')')[0].strip()
    else:
        image_url = "N/A"
    
    # Extraire le lien
    link_element = title_element.find("a") if title_element else None
    link_url = link_element['href'] if link_element else "N/A"

    # Extraire la date
    time_element = article.find("time")
    published_date = time_element.get_text(strip=True) if time_element else "N/A"
    
    # Ajouter les données extraites à la liste
    data.append({
        "title": title,
        "image": image_url,
        "link": link_url,
        "published_date": published_date
    })

# Afficher les données récupérées
for item in data:
    print(f"Title: {item['title']}")
    print(f"Image: {item['image']}")
    print(f"Link: {item['link']}")
    print(f"Published Date: {item['published_date']}")
    print("-" * 50)