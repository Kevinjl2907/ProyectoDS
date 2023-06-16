from .SingletonDAO import SingletonDAO
from .ExcelUtil import importTable

class AdminAsistente():

    def registrarProfesor(self, request, foto):
        return SingletonDAO.getInstance().registrarProfesor(request, foto)
    
    def registrarNuevoIntegranteAlEquipo(self, request):
        return SingletonDAO.getInstance().registrarNuevoIntegranteAlEquipo(request)
    
    def cambiarInfoMiembroEquipo(self, request, foto):
        return SingletonDAO.getInstance().cambiarInfoMiembroEquipo(request, foto)
    
    def definirCoordinador(self, request):
        return SingletonDAO.getInstance().definirCoordinador(request)
    
    def darDeBajaAProfesor(self, request):
        return SingletonDAO.getInstance().darDeBajaAProfesor(request)
    
    def obtenerDetalleProfesor(self, request):
        return SingletonDAO.getInstance().obtenerDetalleProfesor(request)
    
    def obtenerPlanTrabajo(self, request):
        return SingletonDAO.getInstance().obtenerPlanTrabajo(request)
    
    def obtenerDetalleActividad(self, request):
        return SingletonDAO.getInstance().obtenerDetalleActividad(request)
    
    def suministrarEstudiantes(self,excel,sede):
        listaEstudiantes = importTable(excel)
        if(listaEstudiantes[0][0] != 'carnet' and
           listaEstudiantes[0][1] !=  'nombre' and
           listaEstudiantes[0][2] !=  'apellido1' and
           listaEstudiantes[0][3] !=  'apellido2' and
           listaEstudiantes[0][4] !=  'nombreadicional' and
           listaEstudiantes[0][5] !=  'correo' and
           listaEstudiantes[0][6] !=  'celular'):
            return {"response":"unsuccessful"}
        return SingletonDAO.getInstance().suministrarEstudiantes(listaEstudiantes[1:],sede)