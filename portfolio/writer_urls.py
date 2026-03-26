from django.urls import path
from . import writer_views

app_name = 'writer'

urlpatterns = [
    path('',                            writer_views.dashboard,    name='dashboard'),
    path('login/',                      writer_views.writer_login, name='login'),
    path('logout/',                     writer_views.writer_logout, name='logout'),
    path('posts/new/',                  writer_views.post_create,  name='post_create'),
    path('posts/<slug:slug>/edit/',     writer_views.post_edit,    name='post_edit'),
    path('posts/<slug:slug>/delete/',   writer_views.post_delete,  name='post_delete'),
    path('tags/',                       writer_views.tags_view,    name='tags'),
]
