
from django import forms
#
class CSVSpecialtyImportForm(forms.Form):
    csv_file = forms.FileField()

class CSVImgImportForm(forms.Form):
    csv_file = forms.FileField()

class CSVUserImportForm(forms.Form):
    csv_file = forms.FileField()


class CSVTeachImportForm(forms.Form):
    csv_file = forms.FileField()


class CSVStudsImportForm(forms.Form):
    csv_file = forms.FileField()