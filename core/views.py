from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Evento, Inscripcion
from django.contrib import messages

def home(request):

    eventos = Evento.objects.all().order_by('fecha_hora')
    context = {'eventos': eventos}

    return render(request, 'core/index.html', context)


@login_required
def inscribir_evento(request, evento_id):
    try:
        evento = Evento.objects.get(id=evento_id)
        
        with transaction.atomic():
            if evento.plazas_disponibles > 0:

                #crear inscripcion
                Inscripcion.objects.create(usuario=request.user, evento=evento)
                
                #actualiza plazas
                evento.plazas_disponibles -= 1
                evento.save()
                
                messages.success(request, f"¡Te has inscrito exitosamente en {evento.titulo}!")
            else:
                messages.error(request, "Lo sentimos, no quedan plazas disponibles.")
                
    except Evento.DoesNotExist:
        messages.error(request, "El evento no existe.")
    except IntegrityError:
        messages.warning(request, "Ya estás inscrito en este evento.")
        
    return redirect('home')


@login_required
def mis_eventos(request):

    mis_inscripciones = Inscripcion.objects.filter(usuario=request.user)
    context = {'mis_inscripciones': mis_inscripciones}
    return render(request, 'core/mis_eventos.html', context)

@login_required
def anular_inscripcion(request, inscripcion_id):
    try:
        inscripcion = Inscripcion.objects.get(id=inscripcion_id, usuario=request.user)
        evento = inscripcion.evento
        
        with transaction.atomic():
            inscripcion.delete()

            evento.plazas_disponibles += 1
            evento.save()
            
            messages.success(request, f"Se ha anulado tu registro en {evento.titulo}.")
            
    except Inscripcion.DoesNotExist:
        messages.error(request, "La inscripción no existe o no te pertenece.")
        
    return redirect('mis_eventos')