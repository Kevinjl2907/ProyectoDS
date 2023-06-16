"""--------------------------------------------------------------------------------------------------------------------------------------------------------------------
Parte Andres
--------------------------------------------------------------------------------------------------------------------------------------------------------------------"""

import datetime
import ObserverMensaje as O
import SingletonDAO

class controllerMensaje:
    grupos = []  # Lista de grupos(objetos de tipo o.ChatPublisher)

    """
    @author: Andres
    @dev: Crea un nuevo grupo de chat y agrega automaticamente al usuario que lo creo al grupo
    @param: idemisor, integer con el id del usuario que creo el grupo
    @returns: None
    """
    def crearGrupo(self, idemisor):
        grupo = O.ChatPublisher()  # Crea un grupo
        grupo.idGrupo = len(self.grupos)  # Le asigna un id
        self.grupos.append(grupo)  # Lo agrega a la lista de grupos
        self.unirseGrupo(idemisor, grupo.idGrupo)  # Agrega al usuario que lo creo al grupo

    """
    @author: Andres
    @dev: A un grupo le añade un usuario
    @param: idusuario, integer con el id del usuario que se va a unir al grupo
            idgrupo, integer con el id del grupo al que se quiere unir
    @returns: None
    """
    def unirseGrupo(self, idusuario, idgrupo):
        self.grupos[idgrupo].attach(idusuario)

    """
    @author: Andres
    @dev: A un grupo le saca un usuario
    @param: idusuario, integer con el id del usuario que se va a salir grupo
            idgrupo, integer con el id del grupo del que se quiere salir
    @returns: None
    """
    def salirseGrupo(self, idusuario, idgrupo):
        self.grupos[idgrupo].detach(idusuario)

    """
    @author: Andres
    @dev: A un grupo le saca un usuario
    @param: idusuario, integer con el id del usuario que se va a salir grupo
            idgrupo, integer con el id del grupo del que se quiere salir
    @returns: None
    """
    def crearMensaje(self, idemisor, contenido, idgrupo):
        fechahora = datetime.datetime.now()  # Saca la hora a la que se creo el mensaje
        self().grupos[idgrupo].notify(idemisor, contenido, fechahora, idgrupo)  # Manda el mensaje a todos los usuarios del grupo
