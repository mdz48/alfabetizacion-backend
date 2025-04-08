from django.urls import path
from . import views

app_name = 'alfabetizacion'

urlpatterns = [
    path('', views.home, name='home'),
    path('categorias/', views.categorias_list, name='categorias'),
    path('categoria/<int:pk>/', views.categoria_detail, name='categoria_detail'),
    path('juego/<int:pk>/', views.juego_detail, name='juego_detail'),
    path('jugar/<int:juego_id>/', views.jugar, name='jugar'),
    path('guardar-progreso/<int:juego_id>/', views.guardar_progreso, name='guardar_progreso'),
    path('perfil/', views.perfil, name='perfil'),
    path('juego-alfabeto/', views.juego_alfabeto, name='juego_alfabeto'),
]
