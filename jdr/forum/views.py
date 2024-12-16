from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponseForbidden
from .models import Thread, Post


@login_required(login_url='/login/')
def forum_home(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT forum_thread.id, forum_thread.title, forum_thread.created_at, auth_user.username
            FROM forum_thread
            JOIN auth_user ON forum_thread.author_id = auth_user.id
        """)
        threads = cursor.fetchall()
    return render(request, 'home_forum.html', {'threads': threads})


@login_required(login_url='/login/')
def create_thread(request):
    if request.method == 'POST':
        title = request.POST['title']
        author_id = request.user.id
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO forum_thread (title, author_id, created_at) VALUES (%s, %s, NOW())", [
                           title, author_id])
        return redirect('forum_home')
    return render(request, 'create_thread.html')


@login_required(login_url='/login/')
def thread_detail(request, thread_id):
    """
Fonction de vue pour afficher les détails d'un fil de discussion spécifique.

Cette vue nécessite que l'utilisateur soit connecté. Si l'utilisateur n'est pas connecté,
il sera redirigé vers la page de connexion.

Arguments:
    request (HttpRequest): L'objet de la requête HTTP.
    thread_id (int): L'ID du fil de discussion à afficher.

Renvoie:
    HttpResponse: La page de détail du fil de discussion rendue avec les messages et le titre du fil.

Requêtes:
    - Récupère tous les messages dans le fil de discussion spécifié ainsi que les noms d'utilisateur de leurs auteurs.
    - Récupère le titre du fil de discussion spécifié.
"""
    with connection.cursor() as cursor:
        cursor.execute("""
                        SELECT forum_post.*, auth_user.username
                        FROM forum_post 
                        JOIN auth_user ON forum_post.author_id = auth_user.id
                        WHERE forum_post.thread_id = %s
                        """, [thread_id])
        posts = cursor.fetchall()
    with connection.cursor() as cursor:
        cursor.execute("SELECT title FROM forum_thread WHERE id=%s", [thread_id])
        thread_title = cursor.fetchone()
    return render(request, 'thread_detail.html', {'posts': posts, 'thread_id': thread_id, 'thread_title': thread_title})


@login_required(login_url='/login/')
def create_post(request, thread_id):
    if request.method == 'POST':
        content = request.POST['content']
        author_id = request.user.id
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO forum_post (thread_id, content, author_id, created_at) VALUES (%s, %s, %s, NOW())", [
                           thread_id, content, author_id])
        return redirect('thread_detail', thread_id=thread_id)
    return render(request, 'create_post.html', {'thread_id': thread_id})


@login_required(login_url='/login/')
def update_post(request, post_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM forum_post WHERE id=%s", [post_id])
        post = cursor.fetchone()

    if post[3] != request.user.id:  # Vérifie si l'utilisateur est l'auteur
        return HttpResponseForbidden("Vous n'êtes pas autorisé à modifier ce message.")

    if request.method == 'POST':
        content = request.POST['content']
        with connection.cursor() as cursor:
            cursor.execute("UPDATE forum_post SET content=%s WHERE id=%s", [
                           content, post_id])
        return redirect('thread_detail', thread_id=post[4])

    return render(request, 'update_post.html', {'post': post})


@login_required(login_url='/login/')
def delete_post(request, post_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM forum_post WHERE id=%s", [post_id])
        post = cursor.fetchone()

    if post is None:
        return HttpResponseForbidden("Le message n'existe pas.")

    if post[3] != request.user.id:  # Vérifie si l'utilisateur est l'auteur
        return HttpResponseForbidden("Vous n'êtes pas autorisé à supprimer ce message.")

    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM forum_post WHERE id=%s", [post_id])
        return redirect('thread_detail', thread_id=post[4])
