from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Evento, Inscripcion

class InscripcionInline(admin.TabularInline):

    model = Inscripcion
    extra = 0
    readonly_fields = ('usuario', 'fecha_inscripcion')
    can_delete = False

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_hora', 'lugar', 'valor', 'plazas_totales', 'plazas_disponibles')
    list_filter = ('fecha_hora', 'lugar')
    search_fields = ('titulo', 'lugar')
    inlines = [InscripcionInline]

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'evento', 'fecha_inscripcion')
    list_filter = ('evento', 'fecha_inscripcion')