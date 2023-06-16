from rest_framework.views import APIView
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from datetime import datetime
from django.utils import timezone

from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
import json

from .Controllers.AdminProfesores import AdminProfesores
from .Controllers.EquipoGuiaTestSerializer import EquipoGuiaTestSerializer
from .Controllers.ActividadTestSerializer import ActividadTestSerializer
from .Controllers.TipoActSerializer import TipoActSerializer
from .Controllers.PlanTrabajoTest import PlanTrabajoTest
from .Controllers.EstudianteTest import EstudianteTest

from .Controllers.SingletonDAO import SingletonDAO
from .Controllers.SuperAdm import SuperAdm

from .Controllers import llenarbasedatos

import json

# Create your views here.

# ------------      PRUEBAS   ------------------
class Test(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):

    miClase = AdminProfesores()

    def get(self, request):
        registro= self.miClase.pruebaSede()
        mytestJson = {
            "response": [registro,registro,registro,registro]
        }

        return JsonResponse(mytestJson)

class EquipoGuia(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):

    miClase = EquipoGuiaTestSerializer()

    def get(self, request):
        
        return JsonResponse(self.miClase.returnEquipoGuia(), safe=False)
    

class ActividadTestSerializer(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):

    miClase = ActividadTestSerializer()

    def get(self, request):
        
        return JsonResponse(self.miClase.returnActividad())
    

class TipoActSerializer(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):

    miClase = TipoActSerializer()

    def get(self, request):
        
        return JsonResponse(self.miClase.returnTipo())
    

class PlanTrabajoTest(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):

    miClase = PlanTrabajoTest()

    def get(self, request):
        
        return JsonResponse(self.miClase.returnPlan())
    

class EstudianteTest(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):

    miClase = EstudianteTest()

    def get(self, request):
        
        return JsonResponse(self.miClase.returnEstudiante())
    

class pruebitasPa(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):

    def get(self, request):
        
        #SingletonDAO.getInstance().obtenerDetalleEquipo()

        return JsonResponse(SuperAdm.getInstance().obtenerDetalleEquipo())

class Llenado(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):

    def get(self, request):
        llenarbasedatos.llenarTodo()
        return JsonResponse({"response":"success"})

# ---------------------- Profesor Guia -------------------------------
class ListaEstudiantes(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return JsonResponse(SuperAdm.getInstance().listaEstudiantes())
    
class DetalleEquipo(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):
    
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return JsonResponse(SuperAdm.getInstance().obtenerDetalleEquipo())
    
class DetalleProfes(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):
    
    #permission_classes = (IsAuthenticated,)

    def get(self, request):
        return JsonResponse(SuperAdm.getInstance().obtenerDetalleProfes())
    
class ObtenerSedes(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):
    
    #permission_classes = (IsAuthenticated,)

    def get(self, request):
        return JsonResponse(SuperAdm.getInstance().obtenerSedes())
    
class ObtenerRoles(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):
    
    #permission_classes = (IsAuthenticated,)

    def get(self, request):
        return JsonResponse(SuperAdm.getInstance().obtenerRoles())
    
class ModificarEstudiante(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):

    permission_classes = (IsAuthenticated,)

    """
    Formato request:
    {
        "id": "unid",
        "editar" : {
            "nombre" : "unnombre", #(opcional)
            "apellido1" : "unapellido", #(opcional)
            "apellido2" : "unapellido", #(opcional)
            "nombreadicional" : "unnombre", #(opcional)
            "sede" : "unasede", #(opcional)
            "telefono" : "1239802" #(opcional)
        }
    }
    """

    def post(self, request):
        if("carnet" not in request.data or "editar" not in request.data):
            return JsonResponse({"response" : "unsuccessful"})
        return JsonResponse(SuperAdm.getInstance().modificarInfoEstudiante(request))

# --------------------- Profe coordinador ----------------------------
class CrearPlanTrabajo(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):

    #permission_classes = (IsAuthenticated,)

    """
    Formato request:
    {
        "semestre":"2021 S1",
        "semanainicial":"2023-05-01T00:00:00.000Z",
        "semanafinal":"2023-08-21T00:00:00.000Z",
        "vacaciones":[
            "2023-05-22T00:00:00.000Z",
            "2023-05-29T00:00:00.000Z",
            "2023-06-05T00:00:00.000Z"
        ]
    }
    """

    def post(self, request):
        print(request.data)
        llaves = ["semestre","semanainicial","semanafinal","vacaciones"]
        for llave in llaves:
            if llave not in request.data:
                return JsonResponse({"response" : "unsuccessful"})
        
        return JsonResponse(SuperAdm.getInstance().agregarPlanTrabajo(request))

class PlanesTrabajoDisponibles(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):

    #permission_classes = (IsAuthenticated,)

    def get(self, request):        
        return JsonResponse(SuperAdm.getInstance().obtenerPlanesTrabajo())
    
class PlanesTrabajoCompleto(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):

    #permission_classes = (IsAuthenticated,)

    def get(self, request):        
        return JsonResponse(SuperAdm.getInstance().obtenerPlanesCompletos())

class AgregarActividad(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):

    #permission_classes = (IsAuthenticated,)

    """
    Formato request:
    {
        'json': {
            "semana": 1,
            "planTrabajo":"2021 S1",
            "tipo" : "Orientadora",
            "nombre" : "DOP - Procastinacion",
            "fecha" : "2023-05-06T07:00:00.000Z",
            "fechaPublicacion" : "2023-05-02T07:00:00.000Z",
            "diasRecordatorios" : 1,
            "esvirtual" : "false",
            "responsables" : [1,2,3]
        },
        'afiche': jpg image
    }
    """

    def post(self, request):
        if('json' not in request.data or 'afiche' not in request.data):
            return JsonResponse({"response" : "unsuccessful"})
        return JsonResponse(SuperAdm.getInstance()
                                    .agregarActividad(request.data['afiche'],
                                                      json.loads(request.data['json'])))
    
class ModificarActividad(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):

    #permission_classes = (IsAuthenticated,)

    """
    Formato request:
    {
        'json': {
            "idactividad":1,
            "semana": 1,
            "planTrabajo":"2021 S1",
            "tipo" : "Orientadora",
            "nombre" : "DOP - Procastinacion",
            "fecha" : "2021-05-06 07:00:00",
            "fechaPublicacion" : "2021-05-02 07:00:00",
            "diasRecordatorios" : 1,
            "esvirtual" : "false",
            "responsables" : [1,2,3]
        },
        'afiche': jpg image

    }
    """

    def post(self, request):
        if('json' not in request.data and 'afiche' not in request.data):
            return JsonResponse({"response" : "unsuccessful"})
        elif('json' not in request.data):
            return JsonResponse({"response" : "unsuccessful"})
        elif('afiche' not in request.data):
            return JsonResponse(SuperAdm.getInstance()
                                        .modificarActividad(None,
                                                        json.loads(request.data['json'])))
        else:
            return JsonResponse(SuperAdm.getInstance()
                                    .modificarActividad(request.data['afiche'],
                                                      json.loads(request.data['json'])))
        
class BorrarActividad(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):

    #permission_classes = (IsAuthenticated,)

    """
    Formato request:
    {
        'idactividad': 'unid'
    }
    """

    def post(self, request):
        if('idactividad' not in request.data):
            print("borrar")
            return JsonResponse({'response':'unsuccessful'})
        return JsonResponse(SuperAdm.getInstance().borrarActividad(request.data))

class ObtenerActividades(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):

    #permission_classes = (IsAuthenticated,)

    """
    Formato request:
    {
        'planTrabajo': 'unid'
    }
    """

    def post(self, request):
        if('planTrabajo' not in request.data):
            return JsonResponse({'response':'unsuccessful'})
        return JsonResponse(SuperAdm.getInstance().obtenerActividades(request.data['planTrabajo']))
    
class ObtenerAActividades(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):

    #permission_classes = (IsAuthenticated,)

    def get(self, request):
        return JsonResponse(SuperAdm.getInstance().obtenerAActividades())

class ObtenerTipoAct(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):

    #permission_classes = (IsAuthenticated,)

    """
    Formato request:
    {
        'planTrabajo': 'unid'
    }
    """

    def get(self, request):
        return JsonResponse(SuperAdm.getInstance().obtenerTipoAct())

class ObtenerComentarios(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):

    #permission_classes = (IsAuthenticated,)

    """
    Formato request:
    {
        'planTrabajo': 'unid'
    }
    """

    def post(self, request):
        if('planTrabajo' not in request.data):
            return JsonResponse({'response':'unsuccessful'})
        return JsonResponse(SuperAdm.getInstance().obtenerComentarios(request.data['planTrabajo']))#"2021 S1"))

class EnviarComentarios(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):

    permission_classes = (IsAuthenticated,)

    """
    Formato request:
    {
        idactividad : "unid",
        comentario: {
            contenido: "unmensaje",
            fecha: "unafecha"
        }
    }
    """

    def post(self, request):
        if('idactividad' not in request.data or 
           'comentario' not in request.data):
            return JsonResponse({'response':'unsuccessful'})
        request.data['comentario']['autor'] = Token.objects.get(pk=request.auth).user.profesor

        return JsonResponse(SuperAdm.getInstance().enviarComentarios(request.data))

class RealizarActividad(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):

    #permission_classes = (IsAuthenticated,)

    """
    Formato request:
    {
        'json' : {
            'idactividad': 'unid'
            'enlace': 'unenlace'
        },
        'file1' : jpg image,
        'file1' : jpg image
        ...
        'file1' : jpg image
    }
    
    """

    def post(self, request):
        if 'json' not in request.data:
            return JsonResponse({'response':'unsuccessful'})
       
        return JsonResponse(SuperAdm.getInstance().realizarActividad(request))

class CancelarActividad(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):

    #permission_classes = (IsAuthenticated,)

    """
    Formato request:
    {
        'idactividad': 'unid'
        'justificacion': 'unajustificacion'
    }
    """

    def post(self, request):
        if 'idactividad' not in request.data or 'justificacion' not in request.data:
            return JsonResponse({'response':'unsuccessful'})
       
        return JsonResponse(SuperAdm.getInstance().cancelarActividad(request.data['idactividad'],request.data['justificacion']))

class PublicarActividad(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):

    #permission_classes = (IsAuthenticated,)

    """
    Formato request:
    {
        'idactividad': 'unid'
    }
    """

    def post(self, request):
        if 'idactividad' not in request.data:
            return JsonResponse({'response':'unsuccessful'})
       
        return JsonResponse(SuperAdm.getInstance().publicarActividad(request.data['idactividad']))

class GetProfileImage(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):

    permission_classes = (IsAuthenticated,)

    """
    Formato request:
    {
        'idactividad': 'unid'
    }
    """

    def get(self, request):
        user = Token.objects.get(pk=request.auth).user
        if(not hasattr(user,'profesor')):
            return JsonResponse({"imgUrl":''})
        imgUrl = user.profesor.fotografia.url if str(user.profesor.fotografia) != '' else ''
        return JsonResponse({"imgUrl":imgUrl})

# ----------------- Asistente Administrativo -------------------------
class AARegistrarProfesor(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):
    
    """
    Formato request:
    {
        "json": {
            "codigosede": String,
            "nombre": String,
            "apellido1": String,
            "apellido2": String,
            "teloficina": int,
            "telcelular": int,
            "oficina": String,
            "correo":String
        },
        "foto": archivo jpg
    }
    """
    superAdm = SuperAdm.getInstance()

    def post(self, request): 
        if "json" in request.data:
            jsonInfo = json.loads(request.data['json'])
            if ("nombre" not in jsonInfo or
            "apellido1" not in jsonInfo or
            "apellido2" not in jsonInfo or
            "teloficina" not in jsonInfo or
            "telcelular" not in jsonInfo or
            "oficina" not in jsonInfo or
            "codigosede" not in jsonInfo or
            "correo" not in jsonInfo):
                    return JsonResponse({"response" : "unsuccessful"})
        else:
            return JsonResponse({"response" : "unsuccessful"})
        
        if 'foto' in request.data:
            return JsonResponse(self.superAdm.registrarProfesor(jsonInfo
                                                                ,request.data['foto']))
        else:
            return JsonResponse(self.superAdm.registrarProfesor(jsonInfo
                                                                ,None))

class AARegistrarNuevoIntegrante(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):
    
    """
    Formato request:
    {
        idasistente: int,
        codigo: string,
        rol: string
    }
    """

    superAdm = SuperAdm.getInstance()

    def post(self, request): 
        if("codigo" not in request.data or
           "rol" not in request.data or
           "idasistente" not in request.data):
            return JsonResponse({"response" : "unsuccessful"})
        return JsonResponse(self.superAdm.registrarNuevosIntegranteAlEquipo(request))
    
class CargarExcel(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if('file' not in request.data):
            return JsonResponse({"response":"unsuccess"})
        user = Token.objects.get(pk=request.auth).user
        sede = None
        if hasattr(user,'asistenteadministrativo'):
            sede = user.asistenteadministrativo.sede
        elif hasattr(user,'profesor'):
            sede = user.profesor.sede

        return JsonResponse(SuperAdm.getInstance().suministrarEstudiantes(request.FILES.get("file").file,sede))

class AACambiarInfoMiembroEquipo(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):
     
    """
    Formato request:
    {   
        "json": {
            codigo: String,
            teloficina: int,
            telcelular: int,
            nombre: String,
            apellido1: String,
            apellido2: String,
            oficina: String,
            correo: String,
            idasistente: int
        },
        "foto": archivo jpg
    }
    Opcionalmente el archivo con la foto
    El campo de codigo y idasistente son obligatorios (idasistente ya no lo es por motivos)
    """

    superAdm = SuperAdm.getInstance()
    
    def post(self, request): 
        if "json" in request.data:
            jsonInfo = json.loads(request.data['json'])
            #return JsonResponse({"response" : jsonInfo})
            if("codigo" not in jsonInfo or
               "idasistente" not in jsonInfo):
                    return JsonResponse({"response" : "unsuccessful1"})
        else:
            return JsonResponse({"response" : "unsuccessful2"})
            
        if 'foto' in request.data:
            return JsonResponse(self.superAdm.cambiarInfoMiembroEquipo(jsonInfo
                                                                ,request.data['foto']))
        else:
            return JsonResponse(self.superAdm.cambiarInfoMiembroEquipo(jsonInfo
                                                                ,None))
    

class AADefinirCoordinador(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):
    
    """
    Formato request:
    {
        idasistente: int,
        codigoProfesor: string,
    }
    """

    superAdm = SuperAdm.getInstance()

    def post(self, request): 
        if("idasistente" not in request.data or
           "codigoProfesor" not in request.data):
            return JsonResponse({"response" : "unsuccessful"})
        return JsonResponse(self.superAdm.definirCoordinador(request))


class AADarDeBajaAProfesor(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):
    
    """
    Formato request:
    {
        idasistente: int,
        codigoProfesor: string,
    }
    """

    superAdm = SuperAdm.getInstance()

    def post(self, request): 
        if("idasistente" not in request.data or
            "codigoProfesor" not in request.data):
            return JsonResponse({"response" : "unsuccessful"})
        return JsonResponse(self.superAdm.darDeBajaAProfesor(request))
    

class AAObtenerDetalleProfesor(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):
    
    """
    Formato request:
    {
        codigoProfesor: string,
    }
    """

    superAdm = SuperAdm.getInstance()

    def get(self, request): 
        if("codigoProfesor" not in request.data):
            return JsonResponse({"response" : "unsuccessful"})
        return JsonResponse(self.superAdm.obtenerDetalleProfesor(request))
    

class AAObtenerPlanTrabajo(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):
    
    """
    Formato request:
    {
        idplantrabajo: int,
    }
    """

    superAdm = SuperAdm.getInstance()

    def get(self, request): 
        if("idplantrabajo" not in request.data):
            return JsonResponse({"response" : "unsuccessful"})
        return JsonResponse(self.superAdm.obtenerPlanTrabajo(request))
    
    
class AAObtenerDetalleActividad(
    APIView, 
    UpdateModelMixin,
    DestroyModelMixin):
    
    """
    Formato request:
    {
        idactividad: int,
    }
    """

    superAdm = SuperAdm.getInstance()

    def get(self, request): 
        if("idactividad" not in request.data):
            return JsonResponse({"response" : "unsuccessful"})
        return JsonResponse(self.superAdm.obtenerDetalleActividad(request))
