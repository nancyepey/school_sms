
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.teacher_list, name="teacher_list"),
    path('add/', views.add_teacher, name="add_teacher"),
    path('teachers/<str:slug>/', views.view_teacher, name="view_teacher"),
    path('edit/<str:slug>/', views.edit_teacher, name="edit_teacher"),
    path('delete/<str:slug>/', views.delete_teacher, name="delete_teacher"),
    #csv
    path('csv_teachers/', views.teacher_generate_csv, name="downloadcsv_teacher"),
    path('img_csv/', views.images_generate_csv, name="img_downloadcsv"),
    path('alluser_csv/', views.users_generate_csv, name="users_downloadcsv"),

]

