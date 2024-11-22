from django.urls import path
from . import views

urlpatterns = [
    path('', views.forum_home, name='forum_home'),
    path('create_thread/', views.create_thread, name='create_thread'),
    path('thread/<int:thread_id>/', views.thread_detail, name='thread_detail'),
    path('thread/<int:thread_id>/create_post/', views.create_post, name='create_post'),
    path('update_post/<int:post_id>/', views.update_post, name='update_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
]