from django.shortcuts import render
from .mongonection import connection_db
# Create your views here.

def list_article(request):
    article_db = connection_db()
    articles = article_db.articles.find().sort("published_date", -1)
    return render(request, 'list_article.html', {'articles': articles})