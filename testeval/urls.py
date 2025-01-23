from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('add_test/', views.add_test, name="add_test"),
    path('evals/', views.eval_list, name="test_list"),
    path('edit/<str:slug>/', views.edit_test, name="edit_test"),
    path('delete/<str:slug>/', views.delete_test, name="delete_test"),

    #reportcard
    path('reports/', views.report_card_list, name="report_cards"),
    path('reports/create/', views.create_report_card, name="add_report_cards"),
    path('reports/card/', views.generate_pdf, name="generate_pdf"),

    path('reports/card/<str:slug>/', views.viewDocumentInvoice, name="viewDocumentInvoice"),
]
