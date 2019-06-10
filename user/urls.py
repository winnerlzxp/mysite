from django.urls import path
from . import views

# start with blog
urlpatterns = [

    path('detail_login/', views.detail_login, name='detail_login'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('user_info/', views.user_info, name='user_info'),
    path('edit_nickname/', views.edit_nickname, name='edit_nickname'),
    path('bind_email/', views.bind_email, name='bind_email'),
    path('send_verify_code/', views.send_verify_code, name='send_verify_code'),
    path('edit_pass/', views.edit_pass, name='edit_pass'),
    path('find_pass/', views.find_pass, name='find_pass'),
]