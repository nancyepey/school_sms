from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('add_test/', views.add_test, name="add_test"),
    path('evals/', views.eval_list, name="test_list"), 
    path('edit/<str:slug>/', views.edit_test, name="edit_test"),
    path('delete/<str:slug>/', views.delete_test, name="delete_test"),

    #calculate marks and class ranking
    # path('get_marks/', views.get_marks, name="get_marks"),
    path('calculate_marks/', views.cal_mark_class, name="calculate_mark_class"),
    path('calculate_stud_marks/', views.stud_cal_mark, name="cal_stud_marks"),
    path('class_ranking/', views.cal_classranking, name="classranking_class"),
    path('all_class_ranking/', views.all_classrank, name="all_classrank"),
    path('all_ranking/', views.rankx_all, name="all_ranking"),
    path('add_ranking/', views.rankx_add, name="add_ranking"),




    #reportcard
    path('reports/', views.report_card_list, name="report_cards"),
    # path('reports/create/', views.create_report_card, name="add_report_cards"),
    path('reports/create/', views.addReportCard, name="add_report_cards"),
    path('delete_report/<str:slug>/', views.delete_report_card, name="del_report_card"),
    # path('reports/card/', views.generate_pdf, name="generate_pdf"),

    #stats
    path('consolidation/', views.consolidation, name="consolidations"),
    # path('non_consolidation/', views.report_card_list, name="report_cards"),


    path('reports/card/<str:slug>/', views.viewDocumentInvoice, name="viewDocumentInvoice"),

    #download
    #csv
    
    path('csv_test/', views.tests_generate_csv, name="test_downloadcsv"),
    path('report_csv/', views.reportcard_generate_csv, name="report_downloadcsv"),
    path('ranking_csv/', views.ranking_generate_csv, name="ranking_downloadcsv"),
    path('testmoyspecsubj_csv/', views.testmoyspecsubj_generate_csv, name="testmoyspecsubj_downloadcsv"),
]
