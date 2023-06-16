"""--------------------------------------------------------------------------------------------------------------------------------------------------------------------
Parte Andres
--------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
    
import datetime
import ObserverNotificacion as O
import SingletonDAO


"""
@author: Andres
@dev: Metodo que genera una notificacion y la asocia a todos los suscriptores
@param: _idemisor, integer con el id del usuario que genero la notificacion
    _contenido, string con el texto de la notificacion
@returns: None
"""
def generarNotificacion(idemisor, contenido):
    fechahora = datetime.datetime.now()  # Saca la hora a la que se creo la notificacion
    O.ConcretePublisher.get_instance().notify(idemisor, contenido, fechahora)  # Notifica a todos los suscriptores

"""
@author: Andres
@dev: Metodo que pasa una notificacion a leida o no leida y viceversa. Los cambios se reflejan en la base de datos
@param: idnotificacion, integer con el id de la notificacion que se quiere cambiar
@returns: None
"""
def ponerLeidaNoLeida(idnotificacion):
    notificacion = SingletonDAO.getInstance().obtenerNotficacion(idnotificacion)  # Obtiene la notificacion

    # Segun el estado que tenga, lo pasa al contrario. Leida -> No leida y viceversa
    if notificacion.leida == True:
        SingletonDAO.getInstance().ponerComoNoLeida(idnotificacion)
    else:
        SingletonDAO.getInstance().ponerComoLeida(idnotificacion)

"""
@author: Andres
@dev: Metodo borra todas las notificaciones asociadas a un usuario. Los cambios se reflejan en la base de datos
@param: idreceptor, integer con el id del usuario que quiere eliminar todas sus notificaciones
@returns: None
"""
def vaciarBuzon(idreceptor):
    SingletonDAO.getInstance().vaciarBuzon(idreceptor)


"""
@author: Andres
@dev: Metodo que retorna todas las notificaciones asociadas a un usuario. Trae de la base de datos
@param: idreceptor, integer con el id del usuario que quiere ver todas sus notificaciones
@returns: Notificaciones de ese usuario
"""
def obtenerTodasNotificaciones(idreceptor):
    return SingletonDAO.getInstance().obtenerTodasNotificaciones(idreceptor)  # Trae del DAO





# --------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Prueba para ver que si suscriba bien

# Crea un estudiante
from base.models import Estudiante
estudiante1 = Estudiante.objects.create(
            carnet = 2020127158,
            nombre = "Andres",
            nombreadicional = "anmaro",
            apellido1 = "Masis",
            apellido2 = "Rojas",
            sede = None,
            telefono = 60717600,
            correotec = "anmasis@estudiantec.cr",
            fedicion = timezone.now(),
            editor = None,
            fcreacion = timezone.now()
        )

# Lo suscribe al servicio de notificaciones
O.ConcretePublisher.get_instance().subscirbe(estudiante1)
O.ConcretePublisher.get_instance().notify()