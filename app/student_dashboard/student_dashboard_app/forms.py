from django import forms
from .models import Asignatura, Asignacion

class AsignaturaForm(forms.ModelForm):
    class Meta:
        model = Asignatura
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AsignacionForm(forms.ModelForm):
    class Meta:
        model = Asignacion
        fields = ['asignatura', 'titulo', 'descripcion']
        widgets = {
            'asignatura': forms.Select(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['asignatura'].queryset = Asignatura.objects.all()