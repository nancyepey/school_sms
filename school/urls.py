
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('admin_dashboard/', views.admin_dashboard, name="admin_dashboard"),
    path('teacher_dashboard/', views.teacher_dashboard, name="teacher_dashboard"),
    #
    path('add_class/', views.add_class, name="add_class"),
    path('classes/', views.class_list, name="class_list"),
    path('edit/<str:slug>/', views.edit_class, name="edit_class"),
    path('delete/<str:slug>/', views.del_class, name="delete_class"),
    #
    path('add_specialty/', views.add_specialty, name="add_specialty"),
    path('specialty/', views.specialty_list, name="specialty_list"),
    path('edit_specialty/<str:slug>/', views.edit_specialty, name="edit_specialty"),
    path('delete/<str:slug>/', views.del_specialty, name="delete_specialty"),

    #
    path('company/', views.companySettings, name="company_details"),
    #import export
    path('import_export/', views.import_export, name="import_exports_v"),
    #csv
    path('csv_specialty/', views.specialty_generate_csv, name="csv_download_specialty"),
    path('csv_class/', views.class_generate_csv, name="class_csv_download"),
    #import
    path('importcsv_img/', views.import_images, name="importcsv_img"),
    path('importcsv_users/', views.import_users, name="importcsv_user"),
]
