from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistroUsuarioForm, PublicacionForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse, Http404
from .models import UsuarioPersonalizado, Publicacion

def inicio(request):
    # Mostrar todas las publicaciones en la página de inicio
    publicaciones = Publicacion.objects.all().select_related('usuario')
    return render(request, 'inicio.html', {'publicaciones': publicaciones})

def login_view(request):
    return render(request, 'login.html')

@login_required
def perfil(request):
    # Agregar formulario de publicación en el perfil
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.usuario = request.user
            
            # Guardar la imagen si se proporcionó
            if 'imagen' in request.FILES:
                imagen_file = request.FILES['imagen']
                publicacion.imagen_name = imagen_file.name
                publicacion.imagen_type = imagen_file.content_type
                publicacion.imagen = imagen_file.read()
                
            publicacion.save()
            messages.success(request, '¡Publicación creada con éxito!')
            return redirect('perfil')
    else:
        form = PublicacionForm()
    
    # Obtener las publicaciones del usuario para mostrarlas en su perfil
    publicaciones_usuario = Publicacion.objects.filter(usuario=request.user)
    
    return render(request, 'perfil.html', {
        'form': form,
        'publicaciones': publicaciones_usuario
    })

def custom_logout(request):
    logout(request)
    return redirect('inicio')

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Cuenta creada para {user.username}!')
            return redirect('login')
        else:
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

def publicacion_imagen(request, publicacion_id):
    """Vista para servir la imagen de una publicación"""
    try:
        publicacion = Publicacion.objects.get(id=publicacion_id)
        if publicacion.imagen and publicacion.imagen_type:
            return HttpResponse(
                publicacion.imagen,
                content_type=publicacion.imagen_type
            )
    except Publicacion.DoesNotExist:
        pass
    
    # Devolver respuesta 404 si no hay imagen o la publicación no existe
    raise Http404("Imagen no encontrada")