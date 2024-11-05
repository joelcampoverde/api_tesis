from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Evento, Agenda, TipoEvento, Usuario
from datetime import datetime
from django.utils.dateparse import parse_datetime
import uuid

@api_view(['POST'])
def process_command(request):
    data = request.data
    command = data.get('command', '').lower()

    # Proceso de agregar un evento
    if "agregar" in command:
        descripcion = data.get("descripcion")
        fecha_inicio = data.get("fecha_inicio")
        fecha_fin = data.get("fecha_fin")
        modalidad = data.get("modalidad", "presencial")  # Modalidad predeterminada
        tipo_evento_id = data.get("tipo_evento_id")  # ID del tipo de evento, si se proporciona
        usuario_id = data.get("usuario_id")  # ID del usuario, necesario para crear la agenda

        # Validar datos obligatorios
        if not (descripcion and fecha_inicio and fecha_fin and usuario_id):
            return Response({"response": "Faltan datos. Asegúrate de incluir descripción, fecha de inicio, fecha de fin y usuario_id."}, status=status.HTTP_400_BAD_REQUEST)

        # Validar usuario
        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            return Response({"response": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Parsear fechas
        fecha_inicio = parse_datetime(fecha_inicio)
        fecha_fin = parse_datetime(fecha_fin)

        if not fecha_inicio or not fecha_fin or fecha_inicio >= fecha_fin:
            return Response({"response": "Fechas inválidas. Asegúrate de que la fecha de inicio es anterior a la fecha de fin y que las fechas tienen el formato correcto."}, status=status.HTTP_400_BAD_REQUEST)

        # Crear o obtener Agenda asociada al usuario
        agenda, created = Agenda.objects.get_or_create(usuario=usuario)

        # Si no se proporciona el tipo de evento, establecerlo en "Recordatorio"
        if not tipo_evento_id:
            tipo_evento, _ = TipoEvento.objects.get_or_create(descripcion="Recordatorio")
        else:
            try:
                tipo_evento = TipoEvento.objects.get(id=tipo_evento_id)
            except TipoEvento.DoesNotExist:
                return Response({"response": "Tipo de evento no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        # Crear nuevo evento con un ID único
        evento = Evento(
            id=str(uuid.uuid4()),
            agenda=agenda,
            tipo_evento=tipo_evento,
            descripcion=descripcion,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            modalidad=modalidad
        )
        evento.save()

        return Response({"response": f"Evento '{descripcion}' añadido con éxito."}, status=status.HTTP_201_CREATED)

    # Proceso para consultar eventos
    elif "consultar" in command:
        eventos = Evento.objects.all()
        if not eventos:
            return Response({"response": "No hay eventos pendientes."})

        eventos_pendientes = "\n".join([f"{e.descripcion} (Desde {e.fecha_inicio} hasta {e.fecha_fin})" for e in eventos])
        return Response({"response": f"Eventos pendientes:\n{eventos_pendientes}"})

    # Proceso para eliminar un evento
    elif "eliminar" in command:
        evento_descripcion = command.split(" ", 1)[1]  # Asume que el nombre del evento es la palabra después de "eliminar"
        evento = Evento.objects.filter(descripcion=evento_descripcion).first()

        if evento:
            evento.delete()
            return Response({"response": f"Evento '{evento_descripcion}' eliminado con éxito."})
        else:
            return Response({"response": f"No se encontró el evento '{evento_descripcion}'."}, status=status.HTTP_404_NOT_FOUND)

    # Si el comando no es reconocido
    return Response({"response": "Comando no reconocido. Intenta con agregar, consultar o eliminar."}, status=status.HTTP_400_BAD_REQUEST)
