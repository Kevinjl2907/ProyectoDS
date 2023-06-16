from base.models import Asistenteadministrativo
from base.models import Profesor
from base.models import Plantrabajo
from base.models import Equipotrabajo
from base.models import Actividad
from base.models import Estudiante

from base.serializers import AsistenteadministrativoSerializer
from base.serializers import ProfesorSerializer
from base.serializers import PlanTrabajoSerializer
from base.serializers import EquipoTrabajoSerializer
from base.serializers import ActividadSerializer

from .SingletonDAO import SingletonDAO
from .AdminAsistente import AdminAsistente
from .AdminProfesores import AdminProfesores
from .AdminPlanTrabajo import AdminPlanTrabajo
from .AdmEstudiantes import AdminEstudiante
class SuperAdm:
    admAsistente = AdminAsistente()
    admProfesores = AdminProfesores()
    admPlanTrabajo = AdminPlanTrabajo()
    admEstudiante = AdminEstudiante()
    instance = None
    
    def __init__(self):
        self.admAsistente = AdminAsistente()
        self.admProfesores = AdminProfesores()
        self.admPlanTrabajo = AdminPlanTrabajo()
        self.admEstudiante= AdminEstudiante()
    
    @staticmethod
    def getInstance():
        if (SuperAdm.instance == None):
            SuperAdm.instance = SuperAdm()
        return SuperAdm.instance

#----------------------------------------------------------------------------------------------------------------------
#FUNCIONES DEL ASISTENTE
    def registrarProfesor(self, request, foto):
        return self.admAsistente.registrarProfesor(request, foto)
    
    def registrarNuevosIntegranteAlEquipo(self, request):
        return self.admAsistente.registrarNuevoIntegranteAlEquipo(request)
    
    def cambiarInfoMiembroEquipo(self, request, foto):
        return self.admAsistente.cambiarInfoMiembroEquipo(request, foto)
    
    def definirCoordinador(self, request):
        return self.admAsistente.definirCoordinador(request)
    
    def darDeBajaAProfesor(self, request):
        return self.admAsistente.darDeBajaAProfesor(request)
    
    def obtenerDetalleProfesor(self, request):
        return self.admAsistente.obtenerDetalleProfesor(request)
    
    def obtenerDetalleActividad(self, request):
        return self.admAsistente.obtenerDetalleActividad(request)

    def obtenerPlanTrabajo(self, request):
        return self.admAsistente.obtenerPlanTrabajo(request)
    
    def suministrarEstudiantes(self,excel,sede):
        return self.admAsistente.suministrarEstudiantes(excel,sede)


#----------------------------------------------------------------------------------------------------------------------
#FUNCIONES DEL PROFESOR

    def listaEstudiantes(self):
        return self.admProfesores.listaEstudiantes()
    
    def obtenerDetalleEquipo(self):
        return self.admProfesores.obtenerDetalleEquipo()
    
    def obtenerDetalleProfes(self):
        return self.admProfesores.obtenerDetalleProfes()
    
    def obtenerSedes(self):
        return SingletonDAO.getInstance().obtenerSedes()
    
    def obtenerRoles(self):
        return SingletonDAO.getInstance().obtenerRoles()
    
    def modificarInfoEstudiante(self, request):
        return self.admProfesores.modificarInfoEstudiante(request)
    


#----------------------------------------------------------------------------------------------------------------------
#FUNCIONES DEL PLAN DE TRABAJO
    def agregarPlanTrabajo(self,request):
        return self.admPlanTrabajo.agregarPlanTrabajo(request.data)
    
    def agregarActividad(self,afiche,jsonRequest):
        return self.admPlanTrabajo.agregarActividad(afiche,jsonRequest)

    def modificarActividad(self,afiche,jsonRequest):
        return self.admPlanTrabajo.modificarActividad(afiche,jsonRequest)
    
    def borrarActividad(self,request):
        return self.admPlanTrabajo.borrarActividad(request)
    
    def obtenerActividades(self,plan):
        return self.admPlanTrabajo.obtenerActividades(plan)
    
    def obtenerAActividades(self):
        return self.admPlanTrabajo.obtenerAActividades()
    
    def obtenerTipoAct(self):
        return self.admPlanTrabajo.obtenerTipoAct()
    
    def obtenerComentarios(self,plan):
        return self.admPlanTrabajo.obtenerComentarios(plan)
    
    def enviarComentarios(self,request):
        return self.admPlanTrabajo.enviarComentarios(request)

    def realizarActividad(self,request):
        return self.admPlanTrabajo.realizarActividad(request)
    
    def cancelarActividad(self,idactividad,justificacion):
        return self.admPlanTrabajo.cancelarActividad(idactividad,justificacion)
    
    def publicarActividad(self,idactividad):
        return self.admPlanTrabajo.publicarActividad(idactividad)
    
    def obtenerPlanesTrabajo(self):
        return self.admPlanTrabajo.obtenerPlanesTrabajo()
    
    def obtenerPlanesCompletos(self):
        return self.admPlanTrabajo.obtenerPlanesCompletos()
    


#----------------------------------------------------------------------------------------------------------------------
#FUNCIONES DEL ESTUDIANTE

    def obtenerPlanesTrabajo(self):
        return self.admEstudiante.obtenerPlanesTrabajo()
    
    def obtenerPlanesCompletos(self):
        return self.admEstudiante.obtenerPlanesCompletos()
    
    def obtenerDetalleProfesor(self, request):
        return self.admEstudiante.obtenerDetalleProfesor(request)
    
    def obtenerDetalleActividad(self, request):
        return self.admEstudiante.obtenerDetalleActividad(request)

    def obtenerPlanTrabajo(self, request):
        return self.admEstudiante.obtenerPlanTrabajo(request)
  
    def modificarInfoEstudiante(self, request):
        return self.admEstudiante.modificarInfoEstudiante(request)
    
