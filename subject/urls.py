from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.subject_list, name="subject_list"),
    path('add/', views.add_subject, name="add_subject"),
    # path('subjects/<str:slug>/', views.view_subject, name="view_subject"),
    path('edit/<str:slug>/', views.edit_subject, name="edit_subject"),
    path('delete/<str:slug>/', views.delete_subject, name="delete_subject"),
    #csv export
    path('csv_subjects/', views.subjects_generate_csv, name="downloadcsv_subject"),
]
