from django.urls import path
from . import views

urlpatterns = [
    path('save_comment', views.save_comment, name='save_comment')
]