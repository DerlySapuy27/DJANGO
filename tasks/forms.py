from django.forms import ModelForm
from .models import Task
from django import forms
from .models import RolSenaEmpresa, SenaEmpresa, Estudiante, Certificado, Instructor


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
        
class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['nombres', 'apellidos', 'tipo_documento', 'num_documento', 'fecha_expedicion', 'lugar_expedicion', 'nombre_tecnologo', 'ficha_tecnologo', 'id_rol_sena_empresa', 'id_sena_empresa', 'id_certificado']

class CertificadoForm(forms.ModelForm):
    class Meta:
        model = Certificado
        fields = ['id_sena_empresa', 'id_instructor', 'id_estudiante', 'lugar_expedicion', 'asunto']

class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ['nombres', 'apellidos', 'ocupacion', 'cargo', 'tipo_documento', 'numero_documento', 'fecha_expedicion', 'lugar_expedicion', 'telefono', 'firma']        
