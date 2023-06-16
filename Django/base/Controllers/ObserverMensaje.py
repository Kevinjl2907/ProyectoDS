"""--------------------------------------------------------------------------------------------------------------------------------------------------------------------
Parte Andres

Este archivo es para el punto 3 de mensajeria
--------------------------------------------------------------------------------------------------------------------------------------------------------------------"""

import ObserverNotificacion as O
import SingletonDAO as SingletonDAO


class ChatPublisher(O.Publisher):
    idGrupo = 0  # Id del grupo
    _observers = []  # All elements subscribed
    # Add a new subscriber
    def attach(self, observer: O.Observer) -> None:
        if observer.esEstudiante() and observer.getSede() != SingletonDAO.getInstance().getSedeUsuario(idemisor):
            # No se pueden agregar estudiantes de otras sedes
            print("Estudiante de otra sede, no se puede agregar al grupo")
        else:
            self._observers.append(observer)

    # Remove a subscriber
    def detach(self, observer: O.Observer) -> None:
        self._observers.remove(observer)

    # The subscription management methods.
    def notify(self, idemisor, contenido, fechahora, idgrupo) -> None:
        # Notifica observer con obs
        for observer in self._observers:
            SingletonDAO.getInstance().insertarNotificacion(idemisor, contenido, fechahora, idgrupo)
            observer.update()


