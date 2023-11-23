from django.contrib import admin
from .models import Task, RolSenaEmpresa, SenaEmpresa


class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created", )
    
class RolSenaEmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre', 'descripcion')
    
class SenaEmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ubicacion', 'fecha_inicio', 'fecha_fin')
    search_fields = ('nombre', 'ubicacion')   

# Registra los modelos en el panel de administración
admin.site.register(Task, TaskAdmin)
admin.site.register(RolSenaEmpresa, RolSenaEmpresaAdmin)
admin.site.register(SenaEmpresa, SenaEmpresaAdmin)