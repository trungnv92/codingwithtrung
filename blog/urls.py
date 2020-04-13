from django.urls import path, include
from .views import create_post_view, detail_post_view, edit_post_view

app_name = 'blog'
urlpatterns = [
    path('create/', create_post_view, name='create'),
    path('<slug>/', detail_post_view, name='detail'),
    path('<slug>/edit', edit_post_view, name='edit'),
]
