"""--------------------------------------------------------------------------------------------------------------------------------------------------------------------
Parte Andres

Este archivo es para el punto 1 de notificaciones
--------------------------------------------------------------------------------------------------------------------------------------------------------------------"""

from abc import ABC, abstractmethod
import SingletonDAO as SingletonDAO

# The Publisher interface declares a set of methods for managing subscribers.
class Observer(ABC):
    """
    @author: Andres
    @dev: Metodo que retorne el id asociado en la base de datos. Necesario para poder hacer los WHERE id = _id
    @param: None
    @returns: Id del usuario
    """
    @abstractmethod
    def getId(self):
        pass

    """
    @author: Andres
    @dev: Metodo que retorne la sede a la que pertenece ese usuario. Necesario para mensajeria, ya que solo se puede interactuar con
     estudiantes de la misma sede
    @param: None
    @returns: Sede del usuario
    """
    @abstractmethod
    def getSede(self):
        pass

    """
   @author: Andres
   @dev: Metodo que retorna si el usuario es estudiante o no. Necesario para mensajeria, ya que los estudiantes tienen funcionalidades limitadas
   @param: None
   @returns: True si es estudiante, False si no lo es
   """
    @abstractmethod
    def esEstudiante(self):
        pass

    @abstractmethod
    def update(self):
        pass



# The Publisher interface declares a set of methods for managing subscribers.
class Publisher(ABC):
    @abstractmethod
    def attach(self, observer):
        pass

    @abstractmethod
    def detach(self, observer):
        pass

    @abstractmethod
    def notify(self):
        pass


class ConcretePublisher(Publisher):
    _observers = []  # All elements subscribed
    _instance = None  # Singleton instance

    # Singleton method
    @staticmethod
    def get_instance():
        if not ConcretePublisher._instance:
            ConcretePublisher._instance = ConcretePublisher()
        return ConcretePublisher._instance
    
    # Add a new subscriber
    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    # Remove a subscriber
    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    
    # The subscription management methods.
    def notify(self, idemisor, contenido, fechahora) -> None:
        for observer in self._observers:
            SingletonDAO.getInstance().insertarNotificacion(idemisor, contenido, fechahora, observer.getId())
            observer.update()


