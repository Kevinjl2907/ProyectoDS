from django.contrib.auth.models import User
from django.utils import timezone
import mysql.connector


from base.models import Profesor
from base.models import Rol 
from base.models import Sede
from base.models import Estudiante
from base.models import Equipotrabajo
from base.models import Asistenteadministrativo
from base.models import Actividad
from base.models import Plantrabajo

from base.serializers import ProfesorSerializer
from base.serializers import EstudianteSerializer
from base.serializers import EquipoTrabajoSerializer
from base.serializers import SedeSerializer
from base.serializers import AsistenteadministrativoSerializer
from base.serializers import RolSerializer
from base.serializers import DocentesSerializer
from base.serializers import TipoActividadSerializer
from base.serializers import ComentarioSerializer
from base.serializers import ActividadSerializer
from base.serializers import EstadoActividadSerializer
from base.serializers import PlanTrabajoSerializer
from base.serializers import SemanasVacacionesSerializer

from django.utils import timezone

class EquipoGuiaTestSerializer():

    def returnEquipoGuia(self):
        # json = {
        #     "codigo":"SC2",
        #     "auth": 2,
        #     "nombre":"Pablo",
        #     "apellido1":"Campos",
        #     "apellido2":"Esquivel",
        #     "oficina":"SC2",
        #     "teloficina":22222,
        #     "telcelular":86953636,
        #     "rol":1,
        #     "fcreacion":"2023-05-17T16:02:54"
        # }
       
        # serializer = ProfesorSerializer(data=json)
        # if serializer.is_valid():
        #    serializer.save()
        #    return serializer.data
        # return serializer.errors
        
        # json = {
        #     "codigosede": "CA"
        # }
       
        # serializer = SedeSerializer(data=json)
        # if serializer.is_valid():
        #    serializer.save()
        #    return serializer.data
        # return serializer.errors
        json = {
            "codigosede": "SJ"
        }
       
        serializer = SedeSerializer(data=json)
        if serializer.is_valid():
           serializer.save()
        #    return serializer.data
        # return serializer.errors
        json = {
            "codigosede": "LI"
        }
       
        serializer = SedeSerializer(data=json)
        if serializer.is_valid():
           serializer.save()
        #    return serializer.data
        # return serializer.errors
        json = {
            "codigosede": "SC"
        }
       
        serializer = SedeSerializer(data=json)
        if serializer.is_valid():
           serializer.save()
        #    return serializer.data
        # return serializer.errors
        
        json = {
            "codigosede": "AL"
        }
       
        serializer = SedeSerializer(data=json)
        if serializer.is_valid():
           serializer.save()
           return serializer.data
        return serializer.errors
        
        # json = {
        #     "nombre":"Ana",
        #     "auth":3,
        #     "apellido1":"Fajardo",
        #     "apellido2":"Castillo",
        #     "sede":2
        # }
       
        # serializer = AsistenteadministrativoSerializer(data=json)
        # if serializer.is_valid():
        #    serializer.save()
        #    return serializer.data
        # return serializer.errors
        
        # json = {
        #     "desrol":"Coordinador"
        # }
       
        # serializer = RolSerializer(data=json)
        # if serializer.is_valid():
        #    serializer.save()
        # #    return serializer.data
        # # return serializer.errors
        
        # json = {
        #     "desrol":"Guia"
        # }
       
        # serializer = RolSerializer(data=json)
        # if serializer.is_valid():
        #    serializer.save()
        #    return serializer.data
        # return serializer.errors
        
        # asistente = Asistenteadministrativo.objects.get(pk=1)
        # json = {
        #     "editor": asistente,
        # }
       
        # serializer = EquipoTrabajoSerializer(data=json)
        # if serializer.is_valid():
        #    serializer.save()
        #    return serializer.data
        # return serializer.errors
        
        # json = {
        #     'idequipotrabajo':6, 
        #     'idprofesor': 13, 
        #     'esrepresentante': True
        # }
       
        # serializer = DocentesSerializer(data=json)
        # if serializer.is_valid():
        #    serializer.save()
        #    return serializer.data
        # return serializer.errors
        
        # json = {
        #     "destipoactividad": "Motivacionales"
        # }
       
        # serializer = TipoActividadSerializer(data=json)
        # if serializer.is_valid():
        #    serializer.save()
        #    return serializer.data
        # return serializer.errors
        
        # equipo = Equipotrabajo.objects.get(pk=6)
        # seriEquipo = EquipoTrabajoSerializer(equipo)
        # return seriEquipo.data
        
        # json = {
        #     "contenido":"Muy bien esta actividad!",
        #     "fecha":"2023-05-14T14:02:02",
        #     "autor":13,
        #     "actividad":1
        # }
       
        # serializer = ComentarioSerializer(data=json)
        # if serializer.is_valid():
        #    serializer.save()
        #    return serializer.data
        # return serializer.errors
        
        # json = {
        #     "desestado": "Planeada"
        # }
        
        # serializer = EstadoActividadSerializer(data=json)
        # if serializer.is_valid():
        #    serializer.save()
        #    return serializer.data
        # return serializer.errors
    
        # json = {
        #     "id":1,
        #     "semanainicial":"2023-02-15",
        #     "semanafinal":"2023-06-22",
        # }
       
        # serializer = PlanTrabajoSerializer(data=json)
        # if serializer.is_valid():
        #    serializer.save()
        #    return serializer.data
        # return serializer.errors
        
        # json = {
        #     "semana":4,
        #     "tipo":1,
        #     "planTrabajo":1,
        #     "nombre":"Que es la vida universitaria pt2",
        #     "fecha":"2023-03-10T12:00:00",
        #     "fechaPublicacion":"2023-03-09T12:00:00",
        #     "diasrecordatorios":2,
        #     "esvirtual":0,
        #     "estado":1,
        #     "diasrecordatorios":2,
        # }
       
        # serializer = ActividadSerializer(data=json)
    
        # if serializer.is_valid():
        #    serializer.save()
           
        #    act = Actividad.objects.get(pk=3)
        #    profe = Profesor.objects.get(codigo='CA-01')
        #    act.responsables.add(profe)
        #    act.save()
           
        #    return serializer.data
        # return serializer.errors

        # json = {
        #     "contenido":"Que linda actividad",
        #     "fecha":"2023-02-12T08:02:03",
        #     "autor": 13,
        #     "actividad": 2
        # }
       
        # serializer = ComentarioSerializer(data=json)
        # if serializer.is_valid():
        #    serializer.save()
        #    return serializer.data
        # return serializer.errors
        
        # actividad = Actividad.objects.get(pk=2)
        # profe = Profesor.objects.get(pk=12)
        # actividad.responsables.add(profe)
        # seriAct = ActividadSerializer(actividad)
        # return seriAct.data
   
        # plan = Plantrabajo.objects.get(pk=1)
        # actividad = Actividad.objects.get(pk=2)
        # plan.actividades.add(actividad)
        # seriPlan = PlanTrabajoSerializer(plan)
        # return seriPlan.data
        
        # json = {
        #     "semanavacacional":"2023-05-01",
        #     "idplantrabajo":1
        # }
        
        # serializer = SemanasVacacionesSerializer(data=json)
        # if serializer.is_valid():
        #    serializer.save()
        #    return serializer.data
        # return serializer.errors
        
        # json = {
        #     "id":202103,
        #     "nombre":"Carlos",
        #     "nombreadicional":"Manuel",
        #     "apellido1":"Li",
        #     "apellido2":"Hernandez",
        #     "sede":1,
        #     "correotec":"carlos@estudiantec.cr",
        #     "fcreacion":"2023-05-14"
        # }
     
        # serializer = EstudianteSerializer(data=json)
        # if serializer.is_valid():
        #    serializer.save()
        #    return serializer.data
        # return serializer.errors
        
        # -------------------- CREAR ASISTENTE -------------
        # json1 = {
        #     "nombre":"Belinda",
        #     "auth":1,
        #     "apellido1":"Gomez",
        #     "apellido2":"Gomez",
        #     "sede":1
        # }
        
        # correo = "gomez@itcr.co.cr"
        
        # nuevoUser = User.objects.create(username=correo,email=correo,password=12345678,first_name=json1['nombre'],last_name=json1['apellido1'],date_joined=timezone.now())
       
        # serializer = AsistenteadministrativoSerializer(data=json1)
        # if serializer.is_valid():
        #    serializer.save()
        #    return serializer.data
        # return serializer.errors
    
        # ----------- OBTENER EMAIL ---------------------
        # profe = Profesor.objects.get(pk=1)
        # serializer = ProfesorSerializer(profe)
        #email = serializer.getemail(profe)
        
        # return serializer.data
        
   
        # equipo = Equipotrabajo.objects.get(pk=1)
        # serializer = EquipoTrabajoSerializer(equipo)
        # return serializer.data
        
        # ------------ Crear profesor -----------------------
        
        # json = {
        #     "codigo":"SC2",
        #     "auth": 8,
        #     "nombre":"Pablo",
        #     "apellido1":"Campos",
        #     "apellido2":"Esquivel",
        #     "oficina":"SC2",
        #     "teloficina":22222,
        #     "telcelular":86953636,
        #     "rol":1,
        #     "fcreacion":"2023-05-17T16:02:54"
        # }
        
        # correo = "campos@itcr.co.cr"
        
        # user = User.objects.create_user(username=correo,
        #                          email=correo,
        #                          password='12345678',
        #                          first_name=json['nombre'],
        #                          last_name=json['apellido1'],
        #                          )
        
        # serializer = ProfesorSerializer(data=json)
        # if serializer.is_valid():
        #    serializer.save()
        #    return serializer.data
        # return serializer.errors
        
        # ---------- PRUEBA REGISTRO PROFE CON NUEVO CODIGO ---------
        
        # Obtener id del profe (siguiente numero en cantidad de profes de dicha sede)
        # reqData = {
        #             "codigosede": "CA",
        #             "nombre": "Alex",
        #             "apellido1": "Aguirre",
        #             "apellido2": "Ugalde",
        #             "teloficina": 11112222,
        #             "telcelular": 83127171,
        #             "oficina": "B-06",
        #             "fotografia": "foto",
        #             "correo":"aguirre@itcr.co.cr"
        #         }
        
        # conexion = mysql.connector.connect(
        # host='137.184.90.27',
        # user='testing',
        # password='proyectodiseno',
        # database='proyectoDisenoDb'
        # )
        # cursor = conexion.cursor()
        
        # sqlHayProfes = "SELECT COUNT(*) FROM Profesor"
        # cursor.execute(sqlHayProfes)
        # cantProfessql = cursor.fetchone()
        # cantProfes = cantProfessql[0]
        
        # idsede = Sede.objects.get(codigosede=reqData['codigosede']).idsede
         
        # if cantProfes >= 1: # Caso de que ya hubieran profes de esa sede anteriormente
        #     sqlProfeReciente = "SELECT idProfesor FROM Profesor WHERE idsede = %s ORDER BY idProfesor DESC LIMIT 1"
        
        #     cursor.execute(sqlProfeReciente, (idsede,))
        #     profeMasReciente = cursor.fetchone()
        #     idProfeMasReciente = profeMasReciente['idProfesor']
            
        #     idNuevoProfe = idProfeMasReciente + 1
            
        #     cursor.close()
        #     conexion.close()
        
        # elif cantProfes == 0: # Caso de ser el primer profe de dicha sede
        #     idNuevoProfe = 1
        #     cursor.close()
        #     conexion.close()
        
        # # Armar codigo del profesor
        # codigoSede = Sede.objects.get(idsede=idsede).codigosede
        
        # if cantProfes >= 10:
        #     codigoProfe = codigoSede + '-' + str(idNuevoProfe)
        # else:
        #     codigoProfe = codigoSede + '-0' + str(idNuevoProfe)
        
        # if "fotografia" not in reqData:
        #     foto = "None"
        # else:
        #     foto = reqData['fotografia']
        
        # authid = 20
        # infoProfe = {
        #     "fcreacion": timezone.now(),
        #     "idprofesor": idNuevoProfe,
        #     "idsede": idsede,
        #     "codigo": codigoProfe,
        #     "nombre": reqData["nombre"],
        #     "apellido1": reqData["apellido1"],
        #     "apellido2": reqData["apellido2"],
        #     "teloficina": reqData["teloficina"],
        #     "telcelular": reqData["telcelular"],
        #     "oficina": reqData["oficina"],
        #     "auth": authid,
        #     "fotografia": foto
        # }

        # profeSerializer = ProfesorSerializer(data=infoProfe)
        # if profeSerializer.is_valid():
        #     profeSerializer.save()
        #     return {"Response":"successful"}
        # else:
        #     return {"Error": profeSerializer.errors}