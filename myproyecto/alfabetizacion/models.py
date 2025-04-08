from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='categorias/', null=True, blank=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Categorías"

class Juego(models.Model):
    NIVEL_CHOICES = [
        ('facil', 'Fácil'),
        ('medio', 'Medio'),
        ('dificil', 'Difícil'),
    ]
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='juegos')
    nivel = models.CharField(max_length=10, choices=NIVEL_CHOICES, default='facil')
    imagen = models.ImageField(upload_to='juegos/', null=True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.titulo

class Pregunta(models.Model):
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE, related_name='preguntas')
    texto = models.CharField(max_length=255)
    imagen = models.ImageField(upload_to='preguntas/', null=True, blank=True)
    audio = models.FileField(upload_to='audio/', null=True, blank=True)
    
    def __str__(self):
        return self.texto[:50]

class Respuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='respuestas')
    texto = models.CharField(max_length=255)
    es_correcta = models.BooleanField(default=False)
    imagen = models.ImageField(upload_to='respuestas/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.texto} - {'Correcta' if self.es_correcta else 'Incorrecta'}"

class ProgresoUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progresos')
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    completado = models.BooleanField(default=False)
    puntuacion = models.IntegerField(default=0)
    fecha_ultimo_juego = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('usuario', 'juego')
        
    def __str__(self):
        return f"{self.usuario.username} - {self.juego.titulo}"
