from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import RolSenaEmpresa, SenaEmpresa, Task
from .forms import RolSenaEmpresaForm, SenaEmpresaForm, TaskForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404



# Create your views here.
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
#################################prueba################333      
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
            return redirect('tasks:tasks')
        
#########proceso CRUD de roles SENA EMPRESA###########
def rol(request):
    # Recuperar todos los registros de la base de datos
    roles = RolSenaEmpresa.objects.all()
    return render(request, 'rol.html', {'roles': roles})

def ver_rol(request, id):
    rol = RolSenaEmpresa.objects.get(id=id)
    return render(request, 'ver_rol.html', {'rol': rol})

#modales 
#crear rol
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

#editar rol
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

#eliminar rol
def eliminar_rol_modal(request, id):
    rol = get_object_or_404(RolSenaEmpresa, id=id)
    if request.method == 'POST':
        rol.delete()
        # Especifica la URL de redirección después de eliminar el rol
        return redirect('tasks:rol')
    else:
        return JsonResponse({'success': False})
    

#########VISTA SENA EMPRESA###########
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
            return redirect('tasks:senaempresa')
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = SenaEmpresaForm()
    return render(request, 'crear_sena_empresa_modal.html', {'form': form})

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
            form = SenaEmpresaForm(request.POST, instance=sena_empresa)
            if form.is_valid():
                form.save()
                return  redirect('tasks:senaempresa')
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
        else:
            form = SenaEmpresaForm(instance=sena_empresa)

        return render(request, 'tasks/senaempresa.html', {'form': form, 'sena_empresa': sena_empresa})
    except Exception as e:
        print(f"Error en la vista editar_sena_empresa_modal: {e}")
        return JsonResponse({'error': str(e)}, status=500)   
    
    