from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from .models import Solicitud
from .forms import SolicitudForm
from django.contrib import messages



def es_superusuario(user):
    return user.is_superuser


def index(request):
    return render(request, 'logins/index.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(email, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return redirect('/login')

    return render(request, 'logins/register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard')
    return render(request, 'logins/login.html')

def dashboard(request):
    users = User.objects.all()
    data = {'users':users}
    return render(request, 'logins/dashboard.html', data)

def logout_view(request):
    logout(request)
    return redirect('/')

def change(request, username=None):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        password = request.POST.get('password')
        user.set_password(password)
        user.save()
        return redirect('/dashboard/')
    else:
        data = {'username':username}
        return render(request, 'logins/change.html', data)
    
def ingresar_solicitud(request):
    if request.method == 'POST':
       
        nueva_solicitud = Solicitud(
            rut=request.POST.get('rut'),
            nombre=request.POST.get('nombre'),
            apellidos=request.POST.get('apellidos'),
            direccion=request.POST.get('direccion'),
            telefono=request.POST.get('telefono'),
            comuna=request.POST.get('comuna'),
            estado='pendiente'  
        )
        nueva_solicitud.save()
        return HttpResponseRedirect('/')  

    return render(request, 'web/ingresar_solicitud.html')

def buscar_solicitud(request):
    resultados = []
    query = request.GET.get("rut")
    if query:
        resultados = Solicitud.objects.filter(rut=query)

    return render(request, 'web/buscar_solicitud.html', {'resultados': resultados})

@login_required
@user_passes_test(es_superusuario)
def listar_solicitudes(request):
    solicitudes = Solicitud.objects.all()  
    return render(request, 'web/listar_solicitudes.html', {'solicitudes': solicitudes})

@login_required
@user_passes_test(es_superusuario)
def detalle_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, pk=solicitud_id)
    return render(request, 'web/detalle_solicitud.html', {'solicitud': solicitud})

@login_required
@user_passes_test(es_superusuario)
def cambiar_estado(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, pk=solicitud_id)
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in [estado[0] for estado in Solicitud.ESTADOS]:
            solicitud.estado = nuevo_estado
            solicitud.save()
            
            return redirect('listar_solicitudes')
    
    return render(request, 'web/cambiar_estado.html', {'solicitud': solicitud})


@login_required
@user_passes_test(es_superusuario)
def confirmar_eliminacion(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, pk=solicitud_id)
    if request.method == 'POST':
        solicitud.delete()
        return redirect('listar_solicitudes')
    
    return render(request, 'web/confirmar_eliminacion.html', {'solicitud': solicitud})


@login_required
@user_passes_test(es_superusuario)
def crear_usuarios(request):
    if request.method == 'POST':
        first_name = request.POST['first-name']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']
        is_superuser = 'superuser' in request.POST  

        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
        else:
            
            user = User.objects.create_user(email, email, password)
            user.first_name = first_name 
            user.save()
            
            if is_superuser:
                user.is_superuser = True
                user.save()
            
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('dashboard')  

    return render(request, 'web/crear_usuarios.html')
@login_required
@user_passes_test(es_superusuario)
def confirmar_eliminacion_usuario(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        user.delete()
        messages.success(request, f'El usuario {username} ha sido eliminado exitosamente.')
        return redirect('dashboard')
    else:
        return render(request, 'web/confirmar_eliminar_usuario.html', {'usuario': user})


@login_required
@user_passes_test(es_superusuario)
def editar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, pk=solicitud_id)

    if request.method == 'POST':
      
        solicitud.rut = request.POST.get('rut')
        solicitud.nombre = request.POST.get('nombre')
        solicitud.apellidos = request.POST.get('apellidos')
        solicitud.direccion = request.POST.get('direccion')
        solicitud.telefono = request.POST.get('telefono')
        solicitud.comuna = request.POST.get('comuna')

        

        solicitud.save()
        messages.success(request, 'Solicitud actualizada con éxito.')
        return redirect('detalle_solicitud', solicitud_id=solicitud.id)
    else:
        
        return render(request, 'web/editar_solicitud.html', {'solicitud': solicitud})

@login_required
@user_passes_test(es_superusuario)
def detalles_usuario(request, username):
    usuario = get_object_or_404(User, username=username)
    return render(request, 'web/detalles_usuario.html', {'usuario': usuario})

@login_required
@user_passes_test(es_superusuario)
def editar_usuario(request, username):
    user = get_object_or_404(User, username=username)

    if request.method == 'POST':
        first_name = request.POST.get('first-name')
        email = request.POST.get('email')
        is_superuser = request.POST.get('superuser') == 'on'

    
        user.first_name = first_name
        user.email = email
        user.is_superuser = is_superuser
        user.save()
        messages.success(request, f'El usuario {username} ha sido actualizado exitosamente.')

       
        return redirect('detalles_usuario', username=user.username)
    else:
       
        return render(request, 'web/editar_usuario.html', {'user': user})