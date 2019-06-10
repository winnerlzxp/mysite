from django.urls import path
from . import views

urlpatterns = [
    path('like_click', views.like_click, name='like_click')
]