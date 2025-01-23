from django.contrib import admin

#
from . models import Eval, ReportCard

# Register your models here.

@admin.register(Eval)
class EvalAdmin(admin.ModelAdmin):
    #
    list_display = ('student','title', 'titre', 'value', 'coef', 'subject', 'teacher', 'observation')
    search_fields = ('student', 'title', 'titre' ,'coef','eval_subj', 'teacher', 'subject')
    list_filter = ('student', 'title','titre', 'coef', 'teacher',)
    # readonly_fields = ('eval_image',) # Optional: makes the image field read only


@admin.register(ReportCard)
class ReportCardAdmin(admin.ModelAdmin):
    #
    list_display = ('student', 'total_avr',  'student_rank', 'date_of_report_card_generation' )
    search_fields = ('student', 'total_avr' ,'student_rank','date_of_report_card_generation')
    list_filter = ('student','total_avr', 'student_rank', 'date_of_report_card_generation')

