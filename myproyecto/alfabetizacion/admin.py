from django.contrib import admin
from .models import Categoria, Juego, Pregunta, Respuesta, ProgresoUsuario

class RespuestaInline(admin.TabularInline):
    model = Respuesta
    extra = 4

class PreguntaAdmin(admin.ModelAdmin):
    inlines = [RespuestaInline]
    list_display = ('texto', 'juego')
    search_fields = ('texto', 'juego__titulo')
    list_filter = ('juego',)

class PreguntaInline(admin.TabularInline):
    model = Pregunta
    extra = 3

class JuegoAdmin(admin.ModelAdmin):
    inlines = [PreguntaInline]
    list_display = ('titulo', 'categoria', 'nivel', 'activo')
    list_filter = ('categoria', 'nivel', 'activo')
    search_fields = ('titulo', 'descripcion')

class ProgresoUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'juego', 'puntuacion', 'completado', 'fecha_ultimo_juego')
    list_filter = ('completado', 'juego')
    search_fields = ('usuario__username', 'juego__titulo')

admin.site.register(Categoria)
admin.site.register(Juego, JuegoAdmin)
admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(ProgresoUsuario, ProgresoUsuarioAdmin)
