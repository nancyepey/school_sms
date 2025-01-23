from django.db import models
#
# from teacher.models import Teacher
from school.models import ClassRoom
from student.models import Student
from subject.models import Subject


# Create your models here.

class Eval(models.Model):
    title              = models.CharField(max_length=100)
    titre              = models.CharField(max_length=100, null=True, blank=True)
    value                = models.DecimalField(max_digits=10, decimal_places=2) #
    coef                = models.DecimalField(max_digits=10, decimal_places=0) #
    subject_code        = models.CharField(max_length=100, unique=True,null=True, blank=True)
    # Define a foreign key relationship with eval
    # Multiple eval can be assigned to one subject
    subject             = models.ForeignKey(Subject, on_delete=models.CASCADE)
    observation         = models.TextField( null=True, blank=True)

    # Define a foreign key relationship with eval
    # Multiple eval can be assigned to one student
    student              = models.ForeignKey(Student, on_delete=models.CASCADE)

    teacher             = models.CharField(max_length=100)
    added_by            = models.CharField(max_length=100, null=True)
    modified_by         = models.CharField(max_length=100, null=True, blank=True)
    is_actif            = models.BooleanField(default=True)
    created_on          = models.DateTimeField(auto_now_add=True)
    updated_on          = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"{self.title} "



#ranking
class ClassRanking(models.Model):
    term                    = models.CharField(max_length=100)
    classroom             = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    total_coeff           = models.DecimalField(max_digits=10, decimal_places=2) #
    total_marks           = models.DecimalField(max_digits=10, decimal_places=2) #
    total_avg           = models.DecimalField(max_digits=10, decimal_places=2) #
    observation         = models.TextField( null=True, blank=True)

    # Define a foreign key relationship with ranking
    # Multiple ranking can be assigned to one student
    student              = models.ForeignKey(Student, on_delete=models.CASCADE)

    freefield           = models.CharField(max_length=100, null=True, blank=True)
    freefield2           = models.CharField(max_length=100, null=True, blank=True)
    added_by            = models.CharField(max_length=100, null=True)
    modified_by         = models.CharField(max_length=100, null=True, blank=True)
    is_actif            = models.BooleanField(default=True)
    created_on          = models.DateTimeField(auto_now_add=True)
    updated_on          = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"{self.title} "


class ReportCard(models.Model):
    student = models.ForeignKey(Student, related_name="studentreportcard",  on_delete=models.CASCADE)
    # evuation = models.ForeignKey(Eval,  on_delete=models.CASCADE)
    student_rank = models.DecimalField(max_digits=10, decimal_places=0)
    general_subjs_avr = models.DecimalField(max_digits=10, decimal_places=0)
    prof_subjs_avr = models.DecimalField(max_digits=10, decimal_places=0)
    total_avr = models.DecimalField(max_digits=10, decimal_places=0)
    best_avr =  models.DecimalField(max_digits=10, decimal_places=0)
    worst_avr =  models.DecimalField(max_digits=10, decimal_places=0)
    firstterm_avr =  models.DecimalField(max_digits=10, decimal_places=0)
    secondterm_avr =  models.DecimalField(max_digits=10, decimal_places=0)
    date_of_report_card_generation = models.DateField(auto_now_add=True)

    term                = models.CharField(max_length=100, null=True, blank=True)
    academic_year       = models.CharField(max_length=100, null=True, blank=True)
    resumption       = models.CharField(max_length=100, null=True, blank=True)
    subj_moy         = models.CharField(max_length=100, null=True, blank=True)

    moreinfo            = models.TextField(null=True, blank=True)
    added_by            = models.CharField(max_length=100, null=True)
    modified_by         = models.CharField(max_length=100, null=True, blank=True)
    is_actif            = models.BooleanField(default=True)
    created_on          = models.DateTimeField(auto_now_add=True)
    updated_on          = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['student_rank', 'date_of_report_card_generation']
    
    def __str__(self):
        return f"{self.student}_{self.student_rank}_{self.created_on} "
