"""---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Parte Andres
Esto corresponde al punto 4 de cancelacion de actividades
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
from ..models import Actividad
import SingletonDAO as SingletonDAO
import ObserverNotificacion as O

from datetime import datetime

"""
@autor: Andres
@dev: Cancela una actividad y se notifica a los usuarios
@param: actividad, objeto de tipo Actividad, corresponde a la actividad que se va a cancelar
@returns: None
"""
def cancelarActividad(actividad: Actividad):
    SingletonDAO.getInstance().cancelarActividad(actividad.idactividad, "La actividad ha sido cancelada por el profesor")  # Cancela la actividad

    nombreActividad = actividad.nombre
    fecha = actividad.fecha
    mensajeProfesor = "Profesor, recuerde que la actividad " + nombreActividad + " se debe entregar el " + fecha.strftime(
        "%d/%m/%Y")
    mensajeComunidad = "Comunidad, recuerden que la actividad " + nombreActividad + ", no falten el " + fecha.strftime(
        "%d/%m/%Y")
    O.ConcretePublisher.get_instance().notify(actividad.editor, mensajeProfesor, actividad.fechaPublicacion)  # Notifica al profesor
    O.ConcretePublisher.get_instance().notify(actividad.editor, mensajeComunidad, actividad.fechaPublicacion)  # Notifica a la comunidad