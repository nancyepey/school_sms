
from django import forms
#
class CSVSubjectImportForm(forms.Form):
    csv_file = forms.FileField()

