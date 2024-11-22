from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import connection
from .models import Article, Comment

@login_required(login_url='/login/')
def forum_home(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM forum_article")
        articles = cursor.fetchall()
    return render(request, 'home_forum.html', {'articles': articles})

@login_required(login_url='/login/')
def create_article(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        author_id = request.user.id
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO forum_article (title, content, author_id, created_at, updated_at) VALUES (%s, %s, %s, NOW(), NOW())", [title, content, author_id])
        return redirect('forum_home')
    return render(request, 'create_article.html')

@login_required(login_url='/login/')
def update_article(request, article_id):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        with connection.cursor() as cursor:
            cursor.execute("UPDATE forum_article SET title=%s, content=%s, updated_at=NOW() WHERE id=%s", [title, content, article_id])
        return redirect('forum_home')
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM forum_article WHERE id=%s", [article_id])
        article = cursor.fetchone()
    return render(request, 'update_article.html', {'article': article})

@login_required(login_url='/login/')
def delete_article(request, article_id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM forum_article WHERE id=%s", [article_id])
        return redirect('forum_home')
    return redirect('forum_home')