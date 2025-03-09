from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.student_list, name="student_list"),
    path('add/', views.add_student, name="add_student"),
    path('students/<str:slug>/', views.view_student, name="view_student"),
    path('edit/<str:slug>/', views.edit_student, name="edit_student"),
    path('delete/<str:slug>/', views.delete_student, name="delete_student"),
    path('download_csv/<student_list>/', views.generate_csv, name="stud_csv"),
    # path('csv_download/<qs>/', views.qs_to_local_csv, name="qs_stud_csv"),
]
