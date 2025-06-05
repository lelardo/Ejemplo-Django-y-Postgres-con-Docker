from django.shortcuts import render, redirect
from .forms import RegistroUsuarioForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse, Http404
from .models import UsuarioPersonalizado

def inicio(request):
    return render(request, 'inicio.html')

def login_view(request):
    return render(request, 'login.html')

@login_required
def perfil(request):
    return render(request, 'perfil.html')

def custom_logout(request):
    logout(request)
    return redirect('inicio')

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Cuenta creada para {user.username}!')
            return redirect('login')  # Asegúrate de que esta URL existe
        else:
            # Depurar errores
            print(f"Errores en el formulario: {form.errors}")
            messages.error(request, 'Por favor corrige los errores abajo.')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registro.html', {'form': form})

def profile_picture(request, user_id):
    """Vista para servir la imagen de perfil desde la base de datos"""
    try:
        user = UsuarioPersonalizado.objects.get(id=user_id)
        if user.profile_picture and user.profile_picture_type:
            return HttpResponse(
                user.profile_picture,
                content_type=user.profile_picture_type
            )
    except UsuarioPersonalizado.DoesNotExist:
        pass
    
    # Devolver respuesta 404 si no hay imagen o el usuario no existe
    raise Http404("Imagen no encontrada")