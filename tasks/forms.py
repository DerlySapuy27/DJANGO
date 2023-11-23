from django.forms import ModelForm
from .models import Task
from django import forms
from .models import RolSenaEmpresa, SenaEmpresa


###Crear Tareas###
class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        
        
###CRUD ROLES###
class RolSenaEmpresaForm(forms.ModelForm):
    class Meta:
        model = RolSenaEmpresa
        fields = ['nombre', 'descripcion']
        
###CRUD SENA EMPRESA###
class SenaEmpresaForm(forms.ModelForm):
    class Meta:
        model = SenaEmpresa
        fields = ['nombre', 'ubicacion', 'fecha_inicio', 'fecha_fin']
