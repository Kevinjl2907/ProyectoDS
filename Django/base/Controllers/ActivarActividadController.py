"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Parte Andres
Esto corresponde al punto 4 de activacion de actividades
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
from ..models import Actividad
import SingletonDAO as SingletonDAO
import ObserverNotificacion as O

from datetime import datetime

"""
@autor: Andres
@dev: Genera una fecha a partir de los parametros
@param: anio, integer con el año de la fecha
        mes, integer con el mes de la fecha
        dia, integer con el dia de la fecha
@returns: datetime con la fecha generada
"""
def generarFechaFicticia(anio, mes, dia):
    return datetime(year=anio, month=mes, day=dia)


"""
@autor: Andres
@dev: Si se llega a la fecha ficticia de activacion de la actividad, se activa la actividad y se notifica a los usuarios
@param: actividad, objeto de tipo Actividad, corresponde a la actividad que se va a activar
        fechaSimulada, datetime con la fecha ficticia que se esta simulando
        fechasRecordatorio, list con las fechas de recordatorio de la actividad
@returns: None
"""
def activarActividad(actividad: Actividad, fechaSimulada: datetime, fechasRecordatorio: list):
    if actividad.fechaPublicacion == fechaSimulada:
        SingletonDAO.getInstance().activarActividad(actividad) # Pone la actividad como activa
        O.ConcretePublisher.get_instance().notify(actividad.editor, "Profesor, se ha activado la actividad correctamente", actividad.fechaPublicacion)  # Notifica al profesor
        O.ConcretePublisher.get_instance().notify(actividad.editor, "Comunidad, se activo una nueva actividad", actividad.fechaPublicacion)  # Notifica a la comunidad
        # Pone fechas de recordatorio
        for fecha in fechasRecordatorio:
            recordarActividad(actividad, fecha)

"""
@autor: Andres
@dev: Si se llega a la fecha ficticia de recordatorio de la actividad, lanza notificaciones de recordatorio a los usuarios
@param: actividad, objeto de tipo Actividad, corresponde a la actividad que se va a recordar
        fechaRecordatorio, datetime con la fecha de recordatorio de la actividad
        fechaSimulada, datetime con la fecha ficticia que se esta simulando
@returns: None
"""
def recordarActividad(actividad: Actividad, fechaRecordatorio: datetime, fechaSimulada = datetime.now()):
    if fechaSimulada == fechaRecordatorio:
        nombreActividad = actividad.nombre
        fecha = actividad.fecha

        mensajeProfesor = "Profesor, recuerde que la actividad " + nombreActividad + " se debe entregar el " + fecha.strftime("%d/%m/%Y")
        mensajeComunidad = "Comunidad, recuerden que la actividad " + nombreActividad + ", no falten el " + fecha.strftime("%d/%m/%Y")
        O.ConcretePublisher.get_instance().notify(actividad.editor, mensajeProfesor, actividad.fechaPublicacion)  # Notifica al profesor
        O.ConcretePublisher.get_instance().notify(actividad.editor, mensajeComunidad, actividad.fechaPublicacion)  # Notifica a la comunidad

