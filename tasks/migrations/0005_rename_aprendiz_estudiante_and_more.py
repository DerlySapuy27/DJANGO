# Generated by Django 4.2.6 on 2023-11-23 19:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_aprendiz_instructor_certificado_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Aprendiz',
            new_name='Estudiante',
        ),
        migrations.RenameField(
            model_name='certificado',
            old_name='id_aprendiz',
            new_name='id_estudiante',
        ),
    ]
