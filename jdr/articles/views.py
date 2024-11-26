from django.shortcuts import render
from .mongonection import connection_db
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url="login")
def list_article(request):
    article_db = connection_db()
    articles = article_db.articles.find().sort("published_date", -1)
    return render(request, 'list_article.html', {'articles': articles})