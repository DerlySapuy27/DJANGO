# tasks/admin.py
from django.contrib import admin
from .models import Task, RolSenaEmpresa, SenaEmpresa, Estudiante, Certificado, Instructor

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created", )
    
class RolSenaEmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre', 'descripcion')

class SenaEmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ubicacion', 'fecha_inicio', 'fecha_fin')
    search_fields = ('nombre', 'ubicacion')

class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'tipo_documento', 'num_documento', 'fecha_expedicion', 'lugar_expedicion', 'nombre_tecnologo', 'ficha_tecnologo', 'id_rol_sena_empresa', 'id_sena_empresa')
    search_fields = ('nombres', 'apellidos', 'num_documento')

class CertificadoAdmin(admin.ModelAdmin):
    list_display = ('id_sena_empresa', 'id_instructor', 'id_estudiante', 'fecha_expedicion', 'lugar_expedicion', 'asunto')
    search_fields = ('id_estudiante__nombres', 'id_estudiante__apellidos', 'asunto')

class InstructorAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'ocupacion', 'cargo', 'tipo_documento', 'numero_documento', 'fecha_expedicion', 'lugar_expedicion', 'telefono')
    search_fields = ('nombres', 'apellidos', 'numero_documento')

# Registra los modelos en el panel de administración
admin.site.register(Task, TaskAdmin)
admin.site.register(RolSenaEmpresa, RolSenaEmpresaAdmin)
admin.site.register(SenaEmpresa, SenaEmpresaAdmin)
admin.site.register(Estudiante, EstudianteAdmin)
admin.site.register(Certificado, CertificadoAdmin)
admin.site.register(Instructor, InstructorAdmin)
