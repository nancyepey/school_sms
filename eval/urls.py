from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('add_test/', views.add_test, name="add_test"),
    path('evals/', views.eval_list, name="test_list"),
]
