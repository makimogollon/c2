from django.db import models

# Create your models here.

class Evento(models.Model):
    titulo = models.CharField(max_length=200) 
    fecha_hora = models.DateTimeField()       
    lugar = models.CharField(max_length=100)  
    imagen = models.ImageField(upload_to='event_images/') 
    valor = models.DecimalField(max_digits=6, decimal_places=2)
    plazas_totales = models.IntegerField()
    plazas_disponibles = models.IntegerField()

    def __str__(self):
        return self.titulo


class Inscripcion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) 
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE) 
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'evento')
        
    def __str__(self):
        return f"{self.usuario.username} inscrito en {self.evento.titulo}"