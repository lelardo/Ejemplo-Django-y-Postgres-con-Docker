from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', inicio, name='inicio'),
    path('registro/', registrar_usuario, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', success_url='/perfil/'), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('perfil/', perfil, name='perfil'),
    path('profile-picture/<int:user_id>/', profile_picture, name='profile_picture'),
    path('publicacion-imagen/<int:publicacion_id>/', publicacion_imagen, name='publicacion_imagen'),
]
