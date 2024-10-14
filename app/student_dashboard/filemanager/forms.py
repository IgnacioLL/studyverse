from django import forms

class CreateFolderForm(forms.Form):
    folder_name = forms.CharField(max_length=255)  
    asignatura_id = forms.IntegerField()
