from .SingletonDAO import SingletonDAO
from datetime import datetime
import json

class AdminPlanTrabajo:

    def agregarPlanTrabajo(self,jsonPlanTrabajo):
        return SingletonDAO.getInstance().agregarPlanTrabajo(jsonPlanTrabajo)
    
    def agregarActividad(self,afiche,jsonRequest):
        if jsonRequest['esvirtual'] and 'enlace' not in jsonRequest:
            return {'response':'enlaceError'}
        return SingletonDAO.getInstance().agregarActividad(afiche,jsonRequest)
    
    def modificarActividad(self,afiche,jsonRequest):
        if 'esvirtual' in jsonRequest and jsonRequest['esvirtual'] and 'enlace' not in jsonRequest:
            return {'response':'enlaceError'}
        if 'esvirtual' in jsonRequest and not jsonRequest['esvirtual'] and 'enlace' in jsonRequest:
            return {'response':'enlaceError'}
        return SingletonDAO.getInstance().modificarActividad(afiche,jsonRequest)

    def borrarActividad(self,request):
        return SingletonDAO.getInstance().borrarActividad(request)
    
    def obtenerActividades(self,plan):
        return SingletonDAO.getInstance().obtenerActividades(plan)
    
    def obtenerAActividades(self):
        return SingletonDAO.getInstance().obtenerAActividades()
    
    def obtenerTipoAct(self):
        return SingletonDAO.getInstance().obtenerTipoAct()
    
    def obtenerComentarios(self,plan):
        return SingletonDAO.getInstance().obtenerComentarios(plan)
    
    def enviarComentarios(self,request):
        newJson = request
        date = datetime.fromtimestamp((newJson["comentario"]["fecha"]/1000.00))
        newJson["comentario"]["fecha"] = date
        return SingletonDAO.getInstance().enviarComentarios(newJson)

    def realizarActividad(self,request):
        jsonRequest = json.loads(request.data['json'].read())
        if 'idactividad' not in jsonRequest:
            return {'response':'unsuccessful'}
        filelist = []
        for key in request.data:
            if key == 'json':
                continue
            filelist.append(request.data[key])
        return SingletonDAO.getInstance().realizarActividad(jsonRequest,filelist)
    
    def cancelarActividad(self,idactividad,justificacion):
        return SingletonDAO.getInstance().cancelarActividad(idactividad,justificacion)
    
    def publicarActividad(self,idactividad):
        return SingletonDAO.getInstance().publicarActividad(idactividad)
    
    def obtenerPlanesTrabajo(self):
        return SingletonDAO.getInstance().obtenerPlanesTrabajo()
    
    def obtenerPlanesCompletos(self):
        return SingletonDAO.getInstance().obtenerPlanesCompletos()