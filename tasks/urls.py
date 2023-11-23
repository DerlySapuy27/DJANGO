from django.urls import path

from tasks import views

app_name = 'tasks'  # Establece el espacio de nombres de la aplicación

urlpatterns = [
    path('tasks/', views.tasks, name='tasks'),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('tasks/', views.tasks, name='tasks'),  # Asegúrate de que el nombre sea 'tasks'
    path('tasks/create/', views.create_task, name='create_task'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    
    ##Rutas del CRUD roles
    
    path('rol/', views.rol, name='rol'),
    path('roles/crear_modal/', views.crear_rol_modal, name='crear_rol_modal'),
    path('roles/<int:id>/', views.ver_rol, name='ver_rol'),
    path('roles/editar_modal/<int:id>/', views.editar_rol_modal, name='editar_rol_modal'),
    path('roles/eliminar_modal/<int:id>/', views.eliminar_rol_modal, name='eliminar_rol_modal'),

    ##Rutas Sena Empresa
    path('senaempresa/', views.senaempresa, name='senaempresa'),
    path('sena_empresas/crear_modal/', views.crear_sena_empresa_modal, name='crear_sena_empresa_modal'),
    path('sena_empresas/<int:id>/', views.senaempresa, name='ver_sena_empresa'),
    path('sena_empresas/eliminar_modal/<int:id>/', views.eliminar_sena_empresa_modal, name='eliminar_sena_empresa_modal'),
    path('sena_empresas/editar_modal/<int:id>/', views.editar_sena_empresa_modal, name='editar_sena_empresa_modal'),

]
