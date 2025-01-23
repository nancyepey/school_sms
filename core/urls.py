from django.contrib import admin
from django.urls import path, include
# from . import views
from . views import *

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('forgot-password/', forgot_password_view, name='forgot-password'),
    path('reset-password/<str:token>/', reset_password_view, name='reset-password'),
    path('logout/', logout_view, name='logout'),


    # path('', views.index, name="index"),
    # path('add_class/', views.add_class, name="add_class"),
    # path('classes/', views.class_list, name="class_list"),
    # path('edit/<str:slug>/', views.edit_class, name="edit_class"),
]
