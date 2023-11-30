from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title= models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True)
    important = models.BooleanField(default=False) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title + ' - por ' + self.user.username

# Modelo Roles
class RolSenaEmpresa(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    

    def __str__(self):
        return self.nombre
    
#Modelo Sena Empresa
class SenaEmpresa(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=255)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return self.nombre
    
#Modelo Aprendiz    
class Estudiante(models.Model):
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    TIPO_DOCUMENTO_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('TI', 'Tarjeta de Identidad'),
        ('CE', 'Cédula de Extranjería'),
    ]
    tipo_documento = models.CharField(max_length=2, choices=TIPO_DOCUMENTO_CHOICES)
    num_documento = models.CharField(max_length=20)
    fecha_expedicion = models.DateField()
    lugar_expedicion = models.CharField(max_length=255)
    nombre_tecnologo = models.CharField(max_length=100)
    ficha_tecnologo = models.CharField(max_length=20)
    id_rol_sena_empresa = models.ForeignKey('RolSenaEmpresa', on_delete=models.CASCADE)
    id_sena_empresa = models.ForeignKey('SenaEmpresa', on_delete=models.CASCADE)
    id_certificado = models.ForeignKey('Certificado', on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return f"{self.nombres} {self.apellidos}"    

#Modelo Certificado
class Certificado(models.Model):
    fecha_expedicion = models.DateField(auto_now_add=True)
    lugar_expedicion = models.TextField()
    asunto = models.TextField()
    id_sena_empresa = models.ForeignKey('SenaEmpresa', on_delete=models.CASCADE)
    id_instructor = models.ForeignKey('Instructor', on_delete=models.CASCADE)
    id_estudiante = models.ForeignKey('Estudiante', on_delete=models.CASCADE)

    def __str__(self):
        return f"Certificado {self.id} - {self.asunto}"
    
#Modelo Instructor
class Instructor(models.Model):
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    ocupacion = models.CharField(max_length=255)
    cargo = models.CharField(max_length=255)
    tipo_documento = models.CharField(max_length=50)
    numero_documento = models.CharField(max_length=50)
    fecha_expedicion = models.DateField()
    lugar_expedicion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15, null=True, blank=True)
    firma = models.ImageField(upload_to='firmas/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"