from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import RolSenaEmpresa, SenaEmpresa, Task, Estudiante, Certificado, Instructor
from .forms import RolSenaEmpresaForm, SenaEmpresaForm, TaskForm, EstudianteForm, InstructorForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.template.loader import get_template
from django.template import Context




#VISTA INICIO#
def home(request):
    return render(request, 'home.html')

#login
def signup(request):
    
    if request.method == 'GET':
        return render(request, 'signup.html',{
            'form': UserCreationForm
    })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],
                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks:tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
            'form': UserCreationForm,
            "error": 'Username already exists'
    })
        return render(request, 'signup.html',{
            'form': UserCreationForm,
            "error": 'Password do not match'
    })
        
#################################prueba vista tasks################     
def tasks(request):
    tasks = Task.objects.all()
    return render(request, 'tasks.html', {'tasks': tasks})

def create_task(request):   
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks:tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Please provide valida data'
        })
        
##########LOGIN################
def signout(request):
    logout(request)
    return redirect('tasks:home') 

########Iniciar sesion###################
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
        'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST
            ['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or Password is incorrect'
            })
        else:
            login(request, user)
            return redirect('tasks:home')
        
#########proceso CRUD de roles SENA EMPRESA###########
def rol(request):
    # Recuperar todos los registros de la base de datos
    roles = RolSenaEmpresa.objects.all()
    return render(request, 'rol.html', {'roles': roles})

def crear_rol_modal(request):
    if request.method == 'POST':
        form = RolSenaEmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            roles = RolSenaEmpresa.objects.all()
            data = [{'nombre': rol.nombre, 'descripcion': rol.descripcion} for rol in roles]
            return JsonResponse({'success': True, 'roles': data})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = RolSenaEmpresaForm()
    return render(request, 'crear_rol_modal.html', {'form': form})

def editar_rol_modal(request, id):
    try:
        rol = get_object_or_404(RolSenaEmpresa, id=id)

        if request.method == 'POST':
            edit_nombre = request.POST.get('edit_nombre')
            edit_descripcion = request.POST.get('edit_descripcion')
            
            rol.nombre = edit_nombre
            rol.descripcion = edit_descripcion
            rol.save()
            # Redirige a la URL 'nombre_de_tu_vista' después de guardar los cambios
            return redirect('tasks:rol')
        else:
            form = RolSenaEmpresaForm(instance=rol)
        return render(request, 'tasks/rol.html', {'form': form, 'rol': rol})
    except Exception as e:
        print(f"Error en la vista editar_rol_modal: {e}")
        return JsonResponse({'error': str(e)}, status=500)

def eliminar_rol_modal(request, id):
    rol = get_object_or_404(RolSenaEmpresa, id=id)
    if request.method == 'POST':
        rol.delete()
        # Especifica la URL de redirección después de eliminar el rol
        return redirect('tasks:rol')
    else:
        return JsonResponse({'success': False})
    

#########CRUD SENA EMPRESA###########
def senaempresa(request):
    sena_empresas = SenaEmpresa.objects.all()
    return render(request, 'senaempresa.html', {'sena_empresas': sena_empresas})

def crear_sena_empresa_modal(request):
    if request.method == 'POST':
        form = SenaEmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            sena_empresas = SenaEmpresa.objects.all()
            data = [{'nombre': empresa.nombre, 'ubicacion': empresa.ubicacion, 'fecha_inicio': empresa.fecha_inicio, 'fecha_fin': empresa.fecha_fin} for empresa in sena_empresas]
            return JsonResponse({'success': True, 'sena_empresas': data})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = SenaEmpresaForm()
    return render(request, 'senaempresa.html', {'form': form})

def eliminar_sena_empresa_modal(request, id):
    try:
        sena_empresa = get_object_or_404(SenaEmpresa, id=id)

        if request.method == 'POST':
            sena_empresa.delete()
            return redirect('tasks:senaempresa')
        else:
            return JsonResponse({'success': False, 'message': 'Método no permitido'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
def editar_sena_empresa_modal(request, id):
    try:
        sena_empresa = get_object_or_404(SenaEmpresa, id=id)

        if request.method == 'POST':
            edit_nombre = request.POST.get('edit_nombre')
            edit_ubicacion = request.POST.get('edit_ubicacion')
            edit_fecha_inicio = request.POST.get('edit_fecha_inicio')
            edit_fecha_fin = request.POST.get('edit_fecha_fin')
            
            sena_empresa.nombre = edit_nombre
            sena_empresa.ubicacion = edit_ubicacion
            sena_empresa.fecha_inicio = edit_fecha_inicio
            sena_empresa.fecha_fin = edit_fecha_fin
            sena_empresa.save()
            return redirect('tasks:senaempresa')   
        else:
            form = SenaEmpresaForm(instance=sena_empresa)
        return render(request, 'tasks/senaempresa.html', {'form': form, 'sena_empresa': sena_empresa})
    except Exception as e:
        print(f"Error en la vista editar_sena_empresa_modal: {e}")
        return JsonResponse({'error': str(e)}, status=500)   
    
###########################CRUD APRENDIZ##############

def estudiante(request):
    estudiantes = Estudiante.objects.all()
    return render(request, 'estudiante.html', {'estudiantes': estudiantes})


def crear_estudiante_modal(request):
    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            nuevo_estudiante = form.save()

            # Obtener los datos necesarios para incluir en la respuesta JSON
            estudiantes = Estudiante.objects.all()
            data = [{   'nombres': estudiante.nombres, 'apellidos': estudiante.apellidos,
                        'tipo_documento': estudiante.tipo_documento, 'num_documento': estudiante.num_documento,
                        'fecha_expedicion': estudiante.fecha_expedicion, 'lugar_expedicion': estudiante.lugar_expedicion,
                        'nombre_tecnologo': estudiante.nombre_tecnologo, 'ficha_tecnologo': estudiante.ficha_tecnologo,
                        'id_rol_sena_empresa': estudiante.id_rol_sena_empresa, 'id_sena_empresa': estudiante.id_sena_empresa,
                        'id_certificado': estudiante.id_certificado} for estudiante in estudiantes]

            # Si es una solicitud Ajax, devuelve la respuesta JSON
            if request.is_ajax():
                response_data = {'success': True, 'estudiantes': data}
                return JsonResponse(response_data)
            # Si no es una solicitud Ajax, redirige a la vista de estudiantes
            else:
                return redirect(('tasks:estudiante'))
        else:
            # Si la validación del formulario falla, devuelve la respuesta JSON con errores
            response_data = {'success': False, 'errors': form.errors}
            return JsonResponse(response_data)
    else:
        # Si la solicitud no es POST, renderiza el formulario
        form = EstudianteForm()
        return render(request, 'crear_estudiante_modal.html', {'form': form})

def eliminar_estudiante_modal(request, id):
    try:
        estudiantes = get_object_or_404(Estudiante, id=id)

        if request.method == 'POST':
            estudiantes.delete()
            return redirect('tasks:estudiante')
        else:
            return JsonResponse({'success': False, 'message': 'Método no permitido'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    

def editar_estudiante_modal(request, id):
    try:
        estudiante = get_object_or_404(Estudiante, id=id)

        if request.method == 'POST':
            edit_nombres = request.POST.get('edit_nombres')
            edit_apellidos = request.POST.get('edit_apellidos')
            edit_tipo_documento = request.POST.get('edit_tipo_documento')
            edit_num_documento = request.POST.get('edit_num_documento')
            edit_fecha_expedicion = request.POST.get('edit_fecha_expedicion')
            edit_lugar_expedicion = request.POST.get('edit_lugar_expedicion')
            edit_nombre_tecnologo = request.POST.get('edit_nombre_tecnologo')
            edit_ficha_tecnologo = request.POST.get('edit_ficha_tecnologo')
            edit_id_rol_sena_empresa = request.POST.get('edit_id_rol_sena_empresa')
            edit_id_sena_empresa = request.POST.get('edit_id_sena_empresa')
            edit_id_certificado = request.POST.get('edit_id_certificado')
            
            estudiante.nombres = edit_nombres
            estudiante.apellidos = edit_apellidos
            estudiante.tipo_documento = edit_tipo_documento
            estudiante.num_documento = edit_num_documento
            estudiante.fecha_expedicion = edit_fecha_expedicion
            estudiante.lugar_expedicion = edit_lugar_expedicion
            estudiante.nombre_tecnologo = edit_nombre_tecnologo
            estudiante.ficha_tecnologo = edit_ficha_tecnologo
            estudiante.id_rol_sena_empresa = edit_id_rol_sena_empresa
            estudiante.id_sena_empresa = edit_id_sena_empresa
            estudiante.id_certificado = edit_id_certificado
            estudiante.save()
            
            return redirect('tasks:estudiante')   
        else:
            form = EstudianteForm(instance=estudiante)
        return render(request, 'tasks/estudiante.html', {'form': form, 'estudiante': estudiante})
    except Exception as e:
        print(f"Error en la vista editar_estudiante_modal: {e}")
        return JsonResponse({'error': str(e)}, status=500)     

class CrearEstudianteView(View):
    template_name = 'estudiante.html'
class RolesJsonView(View):
    def get(self, request, *args, **kwargs):
        roles = RolSenaEmpresa.objects.values('id', 'nombre')
        return JsonResponse({'roles': list(roles)})  
class SenaEmpresasJsonView(View):
    def get(self, request, *args, **kwargs):
        sena_empresas = SenaEmpresa.objects.values('id', 'nombre')
        return JsonResponse({'sena_empresas': list(sena_empresas)})    

# views.py-atraer datos en JSON
class EstudianteJsonView(View):
    def get(self, request, *args, **kwargs):
        estudiante_id = kwargs.get('id')
        estudiante = get_object_or_404(Estudiante, id=estudiante_id)

        data = {
            'nombres': estudiante.nombres,
            'apellidos': estudiante.apellidos,
            'tipo_documento': estudiante.tipo_documento,
            'num_documento': estudiante.num_documento,
            'fecha_expedicion': estudiante.fecha_expedicion.strftime('%Y-%m-%d'),
            'lugar_expedicion': estudiante.lugar_expedicion,
            'nombre_tecnologo': estudiante.nombre_tecnologo,
            'ficha_tecnologo': estudiante.ficha_tecnologo,
            'id_rol_sena_empresa': estudiante.id_rol_sena_empresa.id if estudiante.id_rol_sena_empresa else None,
            'id_sena_empresa': estudiante.id_sena_empresa.id if estudiante.id_sena_empresa else None,
            'id_certificado': estudiante.id_certificado.id if estudiante.id_certificado else None,
        }

        print(f'Data for estudiante {estudiante_id}: {data}')  # Imprime datos en la consola

        return JsonResponse(data)

    def get(self, request, *args, **kwargs):
        estudiante_id = kwargs.get('id')
        estudiante = get_object_or_404(Estudiante, id=estudiante_id)

        data = {
            'nombres': estudiante.nombres,
            'apellidos': estudiante.apellidos,
            'tipo_documento': estudiante.tipo_documento,
            'num_documento': estudiante.num_documento,
            'fecha_expedicion': estudiante.fecha_expedicion.strftime('%Y-%m-%d'),
            'lugar_expedicion': estudiante.lugar_expedicion,
            'nombre_tecnologo': estudiante.nombre_tecnologo,
            'ficha_tecnologo': estudiante.ficha_tecnologo,
            'id_rol_sena_empresa': estudiante.id_rol_sena_empresa.id if estudiante.id_rol_sena_empresa else None,
            'id_sena_empresa': estudiante.id_sena_empresa.id if estudiante.id_sena_empresa else None,
            'id_certificado': estudiante.id_certificado.id if estudiante.id_certificado else None,
        }

        return JsonResponse(data)   

#CRUD INSTRUCTOR    
def instructor(request):
    instructores = Instructor.objects.all()
    return render(request, 'instructor.html', {'instructores': instructores})

def crear_instructor_modal(request):
    if request.method == 'POST':
        form = InstructorForm(request.POST, request.FILES)
        if form.is_valid():
            nuevo_instructor = form.save()

            # Obtener la URL de la firma para incluir en la respuesta JSON
            firma_url = nuevo_instructor.firma.url if nuevo_instructor.firma else None

            instructores = Instructor.objects.all()
            data = [{   'nombres': instructor.nombres, 'apellidos': instructor.apellidos, 'ocupacion': instructor.ocupacion,
                        'cargo': instructor.cargo, 'tipo_documento': instructor.tipo_documento,
                        'numero_documento': instructor.numero_documento, 'fecha_expedicion': instructor.fecha_expedicion,
                        'lugar_expedicion': instructor.lugar_expedicion, 'telefono': instructor.telefono,
                        'firma': firma_url} for instructor in instructores]
            return JsonResponse({'success': True, 'instructores': data})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = InstructorForm()
    return render(request, 'crear_instructor_modal.html', {'form': form})

def eliminar_instructor_modal(request, id):
    instructor = get_object_or_404(Instructor, id=id)
    if request.method == 'POST':
        instructor.delete()
        # Especifica la URL de redirección después de eliminar el instructor
        return redirect('tasks:instructor')
    else:
        return JsonResponse({'success': False})




    #CRUD INSTRUCTOR

def certificado(request):  
    certificado = Certificado.objects.all()
    return render(request, 'certificado.html', {'certificado': certificado})


def generar_certificado_pdf(request):
    # Obtén los datos necesarios para el certificado (puedes pasarlo como parámetros o cargarlo desde la base de datos)
    datos_certificado = {
        'sena_empresa': 'LA ANGOSTURA',
        'aprendiz_nombre': 'Maritza Ávila Vargas',
        'aprendiz_identificacion': '26.512.623',
        'aprendiz_rol': 'Gestor de Talento Humano',
        'ficha_codigo': '2339723',
        'periodo_inicio': '5 de septiembre de 2022',
        'periodo_fin': '19 de diciembre de 2022',
        'funciones_aprendiz': 'Dentro de las principales funciones que desarrolló fueron...',
        'instructor_nombre': 'LOLA FERNANDA HERRERA HERNÁNDEZ',
        'instructor_identificacion': '52.829.681',
        'instructor_celular': '3204659454',
        'fecha_certificacion': '30 de septiembre de 2023',
    }

    # Renderiza el certificado utilizando una plantilla Django
    template = get_template('certificado.html')
    content = template.render(datos_certificado)

    # Crear un objeto de lienzo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="certificado.pdf"'
    p = canvas.Canvas(response, pagesize=letter)

    # Configurar el lienzo PDF con el contenido de la plantilla renderizada
    p.drawString(100, 500, content)

    # Guardar el lienzo PDF
    p.save()

    return response