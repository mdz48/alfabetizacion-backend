from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Count
from .models import Categoria, Juego, Pregunta, Respuesta, ProgresoUsuario

def home(request):
    categorias = Categoria.objects.all()
    juegos_destacados = Juego.objects.filter(activo=True).order_by('?')[:4]
    return render(request, 'alfabetizacion/home.html', {
        'categorias': categorias,
        'juegos_destacados': juegos_destacados
    })

def categorias_list(request):
    tipo = request.GET.get('tipo', None)
    nivel = request.GET.get('nivel', None)
    aleatorio = request.GET.get('aleatorio', False)
    
    categorias = Categoria.objects.annotate(num_juegos=Count('juegos')).all()
    
    # Si se solicitó el tipo alfabeto, redirigir al juego de alfabeto
    if tipo == 'alfabeto':
        return redirect('alfabetizacion:juego_alfabeto')
    
    # Filtrar categorías según los parámetros
    if tipo:
        # Lógica para filtrar por tipo
        pass
    
    if nivel:
        # Lógica para filtrar por nivel
        pass
    
    if aleatorio:
        # Lógica para seleccionar un juego aleatorio
        juego_aleatorio = Juego.objects.filter(activo=True).order_by('?').first()
        if juego_aleatorio:
            return redirect('alfabetizacion:jugar', juego_id=juego_aleatorio.id)
    
    return render(request, 'alfabetizacion/categorias.html', {'categorias': categorias})

def categoria_detail(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    juegos = Juego.objects.filter(categoria=categoria, activo=True)
    return render(request, 'alfabetizacion/categoria_detail.html', {
        'categoria': categoria,
        'juegos': juegos
    })

def juego_detail(request, pk):
    juego = get_object_or_404(Juego, pk=pk, activo=True)
    return render(request, 'alfabetizacion/juego_detail.html', {'juego': juego})

def jugar(request, juego_id):
    juego = get_object_or_404(Juego, pk=juego_id, activo=True)
    preguntas = Pregunta.objects.filter(juego=juego).prefetch_related('respuestas')
    
    return render(request, 'alfabetizacion/jugar.html', {
        'juego': juego,
        'preguntas': preguntas,
    })

def juego_alfabeto(request):
    """Vista para el juego de aprendizaje del alfabeto"""
    nivel = request.GET.get('nivel', 'facil')  # Default to 'facil' if no level is specified
    
    # Validate that the level is one of the allowed values
    if nivel not in ['facil', 'medio', 'dificil']:
        nivel = 'facil'
    
    context = {
        'nivel': nivel,
        'titulo_nivel': {
            'facil': 'Fácil',
            'medio': 'Medio',
            'dificil': 'Difícil'
        }[nivel]
    }
    
    return render(request, 'alfabetizacion/juego_alfabeto.html', context)

@login_required
def guardar_progreso(request, juego_id):
    if request.method == 'POST' and request.is_ajax():
        juego = get_object_or_404(Juego, pk=juego_id)
        puntuacion = request.POST.get('puntuacion', 0)
        completado = request.POST.get('completado', False) == 'true'
        
        progreso, created = ProgresoUsuario.objects.get_or_create(
            usuario=request.user,
            juego=juego,
            defaults={'puntuacion': puntuacion, 'completado': completado}
        )
        
        if not created:
            # Actualizar si la nueva puntuación es mejor
            if int(puntuacion) > progreso.puntuacion:
                progreso.puntuacion = puntuacion
                progreso.completado = completado
                progreso.save()
                
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False}, status=400)

@login_required
def perfil(request):
    progresos = ProgresoUsuario.objects.filter(usuario=request.user).select_related('juego')
    return render(request, 'alfabetizacion/perfil.html', {'progresos': progresos})
