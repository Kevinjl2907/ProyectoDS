from django.utils import timezone
from datetime import timedelta,datetime
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
import mysql.connector

from base.models import Asistenteadministrativo
from base.models import Profesor
from base.models import Plantrabajo
from base.models import Equipotrabajo
from base.models import Actividad
from base.models import Docentes
from base.models import Estudiante
from base.models import Sede
from base.models import Rol 
from base.models import Tipoactividad
from base.models import Semanasvacaciones
from base.models import Estadoactividad
from base.models import Evidencias
from base.models import Comentario
from base.models import Notificacion
from base.models import Mensaje


from API.settings import DATABASES

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from base.serializers import ProfesorSerializer
from base.serializers import PlanTrabajoSerializer
from base.serializers import PlanFullSerializer
from base.serializers import ProfesEquipoTrabajoSerializer
from base.serializers import ActividadSerializer
from base.serializers import DocentesSerializer
from base.serializers import ListaEstudianteSerializer
from base.serializers import ListarActividadSerializer
from base.serializers import ListarTodasActividadSerializer
from base.serializers import ChatActividadSerializer
from base.serializers import TipoActividadSerializer
from base.serializers import ProfesorEquipoSerializer
from base.serializers import SedeSerializer
from base.serializers import RolSerializer
from base.serializers import Tipoactividad
from base.serializers import NotificacionSerializer
from base.serializers import MensajeSerializer


class SingletonDAO:
    instance = None
    
    def __init__(self):
        pass
    
    @staticmethod
    def getInstance():
        if (SingletonDAO.instance == None):
            SingletonDAO.instance = SingletonDAO()
        return SingletonDAO.instance
    
    
    def registrarProfesor(self, reqData, foto):
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
        # Primero, se necesita crear el user del profesor
        correo = reqData["correo"]
        try:
            nuevoUser = User.objects.create(username=correo,email=correo,password=12345678,first_name=reqData['nombre'],last_name=reqData['apellido1'],is_active=False,date_joined=timezone.now())
        except IntegrityError:
            return {"response":"Ya existe un profesor con este correo"}
        
        authid = nuevoUser.id
        
        idsede = Sede.objects.get(codigosede=reqData['codigosede']).idsede
        # Obtener id del profe (siguiente numero en cantidad de profes de dicha sede)
        
        conexion = mysql.connector.connect(
            host=DATABASES["default"]['HOST'],
            user=DATABASES["default"]['USER'],
            password=DATABASES["default"]['PASSWORD'],
            database=DATABASES["default"]['NAME']
        )
        cursor = conexion.cursor()
        
        sqlHayProfes = "SELECT COUNT(*) FROM Profesor"
        cursor.execute(sqlHayProfes)
        cantProfessql = cursor.fetchone()
        cantProfes = cantProfessql[0]
        
        if cantProfes >= 1: # Caso de que ya hubieran profes de esa sede anteriormente
            sqlProfeReciente = "SELECT numprofesor FROM Profesor WHERE sede = %s ORDER BY numprofesor DESC LIMIT 1"
            cursor.execute(sqlProfeReciente, (idsede,))
            
            profeMasReciente = cursor.fetchone()

            try:
                idProfeMasReciente = profeMasReciente[0]
            except TypeError:
                idProfeMasReciente = 0
            
            numprofe = idProfeMasReciente + 1
                
            cursor.close()
            conexion.close()
        
        elif cantProfes == 0: # Caso de ser el primer profe de dicha sede
            idProfeMasReciente = 1
            numprofe = 1
            cursor.close()
            conexion.close()
        
        # Armar codigo del profesor
        codigoSede = Sede.objects.get(idsede=idsede).codigosede
        
        if idProfeMasReciente >= 10:
            codigoProfe = codigoSede + '-' + str(numprofe)
        else:
            codigoProfe = codigoSede + '-0' + str(numprofe)
        
        infoProfe = {
            "fcreacion": timezone.now(),
            "numprofesor": numprofe,
            "idsede": idsede,
            "codigo": codigoProfe,
            "nombre": reqData["nombre"],
            "apellido1": reqData["apellido1"],
            "apellido2": reqData["apellido2"],
            "teloficina": reqData["teloficina"],
            "telcelular": reqData["telcelular"],
            "oficina": reqData["oficina"],
            "auth": authid,
            "fotografia": foto,
            "fedicion":timezone.now()
        }
            
        profeSerializer = ProfesorSerializer(data=infoProfe)
        if profeSerializer.is_valid():
            profeSerializer.save()
            cursor.close()
            conexion.close()
            return {"response":"successful"}
        else:
            cursor.close()
            conexion.close()
            return {"Error": profeSerializer.errors}
    
        
    def registrarNuevoIntegranteAlEquipo(self, request):
        """
        Formato request:
        {
            idasistente: int
            codigo: string
            rol: string
        }
        """
        reqData = request.data
        idasistente = reqData['idasistente']
        codigoProfe = reqData["codigo"]
        roldescripcion = reqData["rol"]
        
        profesor = Profesor.objects.get(pk=codigoProfe)
        elrolid = Rol.objects.get(desrol=roldescripcion).idrol
        
        sedeCartago = Sede.objects.get(codigosede='CA')

        # Obtener la asistente que esta realizando la transaccion
        try:
            asistente = Asistenteadministrativo.objects.get(pk=idasistente)
        except (ValueError, Asistenteadministrativo.DoesNotExist):
                return {"error":"Asistente not found"}
        
        if asistente.sede.idsede != sedeCartago.idsede and roldescripcion == 'Coordinador':
            return {"response":"El asistente debe ser de Cartago"}

        conexion = mysql.connector.connect(
            host=DATABASES["default"]['HOST'],
            user=DATABASES["default"]['USER'],
            password=DATABASES["default"]['PASSWORD'],
            database=DATABASES["default"]['NAME']
        )
        cursor = conexion.cursor()
        sqlIdEquipo = "SELECT * FROM EquipoTrabajo ORDER BY idEquipoTrabajo DESC LIMIT 1"
        cursor.execute(sqlIdEquipo)
        equipo = cursor.fetchone()
        
        if equipo is not None:
            equipoId = equipo[0]   
            elEquipo = Equipotrabajo.objects.get(pk=equipoId)
            elEquipo.fedicion = timezone.now()
            elEquipo.editor = asistente
            elEquipo.save()
        else:
            nuevoEquipo = Equipotrabajo.objects.create(fedicion=timezone.now(), editor=asistente)
            equipoId = nuevoEquipo.idequipotrabajo
        
        # Verificar que no se haya alcanzado el maximo de integrantes
        sqlMaxIntegrantes = "SELECT COUNT(*) AS cantProfes FROM Docentes WHERE idEquipoTrabajo = %s"
        cursor.execute(sqlMaxIntegrantes, (equipoId,))
        cantProfes = cursor.fetchone()
        numeroDeProfes = cantProfes[0]
        
        if numeroDeProfes == 5:
            return {"response":"Se ha llegado al maximo de integrantes del equipo"}
        
        # Obtener el id del rol de Coordinador para verificar si ya hay un coordinador
        rolCoordinador = Rol.objects.get(desrol='Coordinador').idrol
        
        if elrolid == rolCoordinador:
            sqlHayCoordinador = "SELECT COUNT(*) AS cantCoordinador FROM Docentes WHERE rol = %s"
            cursor.execute(sqlHayCoordinador, (rolCoordinador,))
            cantCoordinador = cursor.fetchone()
            numeroDeCoordinador = cantCoordinador[0]
            
            if numeroDeCoordinador > 0: # Caso de que ya exista un coordinador en el equipo
                # Obtener el coordinador actual y actualizarlo a profe guia
                coordinadorActual_docentes = Docentes.objects.get(rol=rolCoordinador)
                coordinadorActual_docentes.rol = Rol.objects.get(desrol='Representante')
                coordinadorActual_docentes.save()
        
        # Verificar que no se repitan representantes de misma sede
        sqlRepresentantes = "SELECT codigo FROM Profesor WHERE codigo IN (SELECT idProfesor FROM Docentes WHERE idEquipoTrabajo = %s)"
        cursor.execute(sqlRepresentantes, (equipoId,))
        rows = cursor.fetchall()
   
        for profe in rows:
            idProfesor = profe[0]  # Access the idProfesor value
            esteProfeSede = Profesor.objects.get(pk=idProfesor).idsede
            
            if esteProfeSede == profesor.idsede:
                return {"response":"Ya existe un representante para esta sede"}
        
        infoDocentes = {
            "idequipotrabajo":equipoId,
            "idprofesor":codigoProfe,
            "rol":elrolid
        }

        cursor.close()
        conexion.close()
            
        serializer = DocentesSerializer(data=infoDocentes)
        if serializer.is_valid():
           serializer.save()
           # Activar cuenta del profesor
           correo = ProfesorSerializer(profesor).getemail(profesor)
           user = User.objects.get(username=correo)
           user.is_active = True
           user.save()
           
           return {"response":"successful"}
        return {"response":serializer.errors}
                
    
    def cambiarInfoMiembroEquipo(self, reqData, foto):
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
        El campo de codigo y idasistente son obligatorios
        """
        profePk = reqData["codigo"]
        
        # Obtener el profesor que se va a modficar
        try:
            profe = Profesor.objects.get(pk=profePk)
        except (ValueError, Profesor.DoesNotExist):
            return {"error":"Profesor not found"}
     
        profe.fedicion = timezone.now()
        
        # Verificar si se desea modificar la foto
        if foto is not None:
            profe.fotografia = foto
        
        # Buscar cuales atributos se desean modficiar
        for attribute in reqData:
            match attribute:
                case "codigo":
                    pass
                case "idasistente":
                    pass
                case "nombre":
                    profe.nombre = reqData[attribute]
                    profe.save()
                    usernameProf = ProfesorSerializer(profe).getemail(profe)
                    userProfe = User.objects.get(username=usernameProf)
                    userProfe.first_name = profe.nombre
                    userProfe.save()
                case "apellido1":
                    profe.apellido1 = reqData[attribute]
                    profe.save()
                    usernameProf = ProfesorSerializer(profe).getemail(profe)
                    userProfe = User.objects.get(username=usernameProf)
                    userProfe.last_name = profe.apellido1
                    userProfe.save()
                case "apellido2":
                    profe.apellido2 = reqData[attribute]
                case "teloficina":
                    profe.teloficina = reqData[attribute]
                case "telcelular":
                    profe.telcelular = reqData[attribute]
                case "oficina":
                    profe.oficina = reqData[attribute]
                case "correo":
                    nuevoEmail = reqData[attribute]
                    oldEmail = ProfesorSerializer(profe).getemail(profe)
                    if(User.objects.filter(email=nuevoEmail).count() > 0 and nuevoEmail != oldEmail):
                        return {"error":"Ya existe un profesor con este correo"}
                    userProfe = User.objects.get(username=oldEmail)
                    userProfe.email = nuevoEmail
                    userProfe.username = nuevoEmail
                    userProfe.save()
                case _:
                    return {"error":"Attribute doesn't exist"}
        profe.save()
        
        # Obtener la asistente que esta realizando la transaccion
        asistente = None
        if('idasistente' in reqData and reqData['idasistente']!=None):
            try:
                asistente = Asistenteadministrativo.objects.get(pk=reqData['idasistente'])
            except (ValueError, Asistenteadministrativo.DoesNotExist):
                    return {"error":"Asistente not found"}
        
        conexion = mysql.connector.connect(
            host=DATABASES["default"]['HOST'],
            user=DATABASES["default"]['USER'],
            password=DATABASES["default"]['PASSWORD'],
            database=DATABASES["default"]['NAME']
        )
        cursor = conexion.cursor()
        sqlIdEquipo = "SELECT * FROM EquipoTrabajo ORDER BY idEquipoTrabajo DESC LIMIT 1"
        cursor.execute(sqlIdEquipo)
        equipo = cursor.fetchone()
            
        equipoId = equipo[0]   
        elEquipo = Equipotrabajo.objects.get(pk=equipoId)
        elEquipo.fedicion = timezone.now()
        if asistente != None:
            elEquipo.editor = asistente
        elEquipo.save()

        return {"response":"successful"}
    
    
    def definirCoordinador(self, request):
        """
        Formato request:
        {
            idasistente: int,
            codigoProfesor: string,
        }
        """
        reqData = request.data
        
        try:
            asistente = Asistenteadministrativo.objects.get(pk=reqData['idasistente'])
        except (ValueError, Asistenteadministrativo.DoesNotExist):
                return {"error":"Asistente not found"}
        
        sedeCartago = Sede.objects.get(codigosede='CA')
        rolCoordinador = Rol.objects.get(desrol='Coordinador')
        
        # Obtener el id del equipo de trabajo 
        conexion = mysql.connector.connect(
            host=DATABASES["default"]['HOST'],
            user=DATABASES["default"]['USER'],
            password=DATABASES["default"]['PASSWORD'],
            database=DATABASES["default"]['NAME']
        )
        cursor = conexion.cursor()
        sqlIdEquipo = "SELECT * FROM EquipoTrabajo ORDER BY idEquipoTrabajo DESC LIMIT 1"
        cursor.execute(sqlIdEquipo)
        equipo = cursor.fetchone()
        idEquipo = equipo[0]  
        
        # verificar que la asistente sea de Cartago
        if asistente.sede.idsede == sedeCartago.idsede:
            # Obtener al nuevo coordinador
            try:
                nuevoCoordinador = Docentes.objects.get(idprofesor=reqData['codigoProfesor'])  
            except (ValueError, Docentes.DoesNotExist):
                return {"error":"Profesor not found"}
                 
            docentes = Docentes.objects.filter(idequipotrabajo=idEquipo)
            # Revisar si ya existe algun Coordinador para actualizar su rol
            for profesor in docentes:
                if profesor.rol == rolCoordinador:
                    viejoCoordinador = Docentes.objects.get(idprofesor=profesor.idprofesor)
                    viejoCoordinador.rol = Rol.objects.get(desrol='Representante')
                    viejoCoordinador.save()
            
            # Asignarle el rol de coordinador al nuevo coordinador
            nuevoCoordinador = Docentes.objects.get(idprofesor=reqData['codigoProfesor'])  
            nuevoCoordinador.rol = rolCoordinador
            nuevoCoordinador.save()
            
            # Actualizar quien editó al equipo y cuándo lo hizo
            elEquipo = Equipotrabajo.objects.get(pk=idEquipo)
            elEquipo.fedicion = timezone.now()
            elEquipo.editor = asistente
            elEquipo.save()
            
            cursor.close()
            conexion.close()
            return {"response":"successful"}
                
        else:
            cursor.close()
            conexion.close()
            return {"response":"El asistente debe ser de Cartago"}
                
    
    def darDeBajaAProfesor(self, request):
        """
        Formato request:
        {
            idasistente: int,
            codigoProfesor: string,
        }
        """
        reqData = request.data
        
        # Obtener al asistente que realizara la transaccion
        try:
            asistente = Asistenteadministrativo.objects.get(pk=reqData['idasistente'])
        except (ValueError, Asistenteadministrativo.DoesNotExist):
                return {"error":"Asistente not found"}
            
        # Se elimina al profe del equipo, pero no de la lista de profesores existentes
        try:
            # Obtener el id del equipo de trabajo 
            conexion = mysql.connector.connect(
                host=DATABASES["default"]['HOST'],
                user=DATABASES["default"]['USER'],
                password=DATABASES["default"]['PASSWORD'],
                database=DATABASES["default"]['NAME']
            )
            cursor = conexion.cursor()
            sqlIdEquipo = "SELECT * FROM EquipoTrabajo ORDER BY idEquipoTrabajo DESC LIMIT 1"
            cursor.execute(sqlIdEquipo)
            equipo = cursor.fetchone()
            idEquipo = equipo[0]  
            
            # Actualizar quien editó al equipo y cuándo lo hizo
            elEquipo = Equipotrabajo.objects.get(pk=idEquipo)
            elEquipo.fedicion = timezone.now()
            elEquipo.editor = asistente
            elEquipo.save()
            
            cursor.close()
            conexion.close()
            
            profeDarBaja = Docentes.objects.get(idprofesor=reqData['codigoProfesor'])
            profeDarBaja.idprofesor.auth.is_active = False
            profeDarBaja.idprofesor.auth.save()
            profeDarBaja.delete()
            
        except (ValueError, Docentes.DoesNotExist):
            return {"error":"Profesor not found"}
        
        return {"response":"successful"}
        
    
    def obtenerDetalleProfesor(self, request):
        """
        Formato request:
        {
            codigoProfesor: string,
        }
        """
        reqData = request.data
        # Verificar que el profesor exista
        try:
            profe = Profesor.objects.get(pk=reqData['codigoProfesor'])  
            profeSerializer = ProfesorSerializer(profe)
        except (ValueError, Profesor.DoesNotExist):
            return {"error":"Profesor not found"}
        
        info = {
            "foto": profe.fotografia,
            "codigo": reqData['codigoProfesor'],
            "nombre": profe.nombre,
            "apellido1": profe.apellido1,
            "apellido2": profe.apellido2,
            "teloficina": profe.teloficina,
            "telcelular": profe.telcelular,
            "oficina": profe.oficina,
            "correo": profeSerializer.getemail(profe)
        }
        return {"reponse":info}
    
    
    def obtenerDetalleActividad(self, request):
        """
        Formato request:
        {
            idactividad: int,
        }
        """
        reqData = request.data
       
        try:
            actividad = Actividad.objects.get(pk=reqData['idactividad'])
        except (ValueError, Actividad.DoesNotExist):
            return {"error":"Actividad not found"}
        
        if actividad.esvirtual == 0:
            modalidad = "Presencial"
        else:
            modalidad = "Virtual"
        
        info = {
            "nombre": actividad.nombre,
            "fecha": actividad.fecha,
            "tipo": Tipoactividad.objects.get(pk=actividad.tipo.idtipoactividad).destipoactividad,
            "modalidad": modalidad,
            "estado": Estadoactividad.objects.get(pk=actividad.estado.idestado).desestado,
            "responsables": ActividadSerializer(actividad).data['responsables']
        }
        
        return {"response": info}
    
    
    def obtenerPlanTrabajo(self, request):
        """
        Formato request:
        {
            idplantrabajo: int
        }
        """
        reqData = request.data
       
        try:
            plan = Plantrabajo.objects.get(pk=reqData['idplantrabajo'])
        except (ValueError, Plantrabajo.DoesNotExist):
            return {"error":"Plan de trabajo not found"}
        
        actividades = Actividad.objects.filter(planTrabajo=plan.idplantrabajo)
        infoProximasActividades = list()
        
        for act in actividades:
            idactividad = act.idactividad
            nombre = act.nombre
            fechaactividad = str(act.fecha.date())
            horaactividad = str(act.fecha.time())
            
            jsonActividad = {
                "idactividad": idactividad,
                "nombre": nombre,
                "fecha": fechaactividad,
                "hora": horaactividad
            }
        
            infoProximasActividades.append(jsonActividad)
       
        return {"response": list(infoProximasActividades)}

        
    def suministrarEstudiantes(self,estudiantes,sede):
        estudiantesModel = []
        for estudiante in estudiantes:
            try:
                estudiantesModel.append(
                    Estudiante(
                        carnet = estudiante[0],
                        nombre = estudiante[1],
                        apellido1 = estudiante[2],
                        apellido2 = estudiante[3],
                        nombreadicional = estudiante[4],
                        sede =sede,
                        correotec = estudiante[5],
                        telefono = estudiante[6],
                        fcreacion = timezone.now()
                    )
                )
            except:
                return {"response":"unsuccessful"}
        try:
            Estudiante.objects.bulk_create(estudiantesModel)
        except:
            return {"response":"unsuccessful"}
        return {"response":"successful"}

    def listaEstudiantes(self):
        # Query que dice que quiero todos los estudiantes
        query = Estudiante.objects.all()

        # Se deserializa la query (la variable query ahorita es un objeto de tipo QuerySet)
        deserialized = ListaEstudianteSerializer(query,many=True)

        # serialized ahorita es una lista con estudiantes deserializados (son un diccionario/json)
        # pero una lista no es un json como tal, pero si le agregamos a una llave una lista se convierte
        # en un json
        jsonToReturn= {
            "estudiantes" : deserialized.data
        }

        # Simplemente para imprimir la lista
        #print(json.dumps(deserialized.data))

        # Se retorna el json
        return jsonToReturn
    
    def obtenerDetalleEquipo(self):
        if(Equipotrabajo.objects.all().count() <= 0):
            return {"response":"unsuccessful"}
        deserialized = ProfesEquipoTrabajoSerializer(Equipotrabajo.objects.all()[0])
        response = deserialized.data
        return {'equipoTrabajo' : response['docentes']}
    
    def obtenerDetalleProfes(self):
        response = ProfesorEquipoSerializer(Profesor.objects.filter(auth__is_active=False),many=True)
        return {'profes' : response.data}
    
    def modificarInfoEstudiante(self,request):
        estudiante = None
        try:
            estudiante = Estudiante.objects.get(pk=request.data["carnet"])
        except (ValueError, Estudiante.DoesNotExist):
            return {"response":"unsuccessful","error":"Estudiante not found"}
        for attribute in request.data["editar"]:
            match attribute:
                case "nombre":
                    estudiante.nombre = request.data["editar"][attribute]
                case "apellido1":
                    estudiante.apellido1 = request.data["editar"][attribute]
                case "apellido2":
                    estudiante.apellido2 = request.data["editar"][attribute]
                case "nombreadicional":
                    estudiante.nombreadicional = request.data["editar"][attribute]
                case "sede":
                    sede = None
                    try:
                        sede =Sede.objects.get(codigosede=request.data["editar"][attribute])
                    except (ValueError, Estudiante.DoesNotExist):
                        return {"response":"unsuccessful","error":"Sede not found"}
                    estudiante.sede = sede
                case "telefono":
                    estudiante.telefono = request.data["editar"][attribute]
                case "correo":
                    estudiante.correotec = request.data["editar"][attribute]
                case _:
                    return {"response":"unsuccessful","error":"Attribute doesnt exist"}
        estudiante.save()

        return {"response":"successful"}
    
    def agregarPlanTrabajo(self,jsonPlanTrabajo):
        if(not isinstance(jsonPlanTrabajo['vacaciones'],list)):
            return {"response":"unsuccessful"}
        amountOfWeeks = 15 + len(jsonPlanTrabajo['vacaciones'])
        try:
            semanainicial = datetime.strptime(jsonPlanTrabajo["semanainicial"].split("T")[0],'%Y-%m-%d') 
            semanafinal = datetime.strptime(jsonPlanTrabajo["semanafinal"].split("T")[0],'%Y-%m-%d')
        except ValueError:
            return {"response":"dateFormat"}

        if(((semanainicial+timedelta(weeks=amountOfWeeks)-semanafinal)).days != 0):
            return {"response":"weeksError"}
        
        plan = Plantrabajo(
            semestre = jsonPlanTrabajo['semestre'],
            semanainicial = semanainicial,
            semanafinal = semanafinal
        )

        try:
            plan.full_clean()
        except ValidationError:
            return {"response":"planError"}

        semanaslist = []
        for semana in jsonPlanTrabajo['vacaciones']:
            try:
                semanaslist.append(Semanasvacaciones(
                    semanavacacional = semana.split("T")[0],
                    semestre = plan
                ))
            except ValueError:
                return {"response":"dateFormat"}
            
        plan.save()
        Semanasvacaciones.objects.bulk_create(semanaslist)
        
        return {"response":"successful"}
    
    def agregarActividad(self,afiche,jsonRequest):
        fecha = datetime.strptime(jsonRequest["fecha"],'%Y-%m-%dT%H:%M:%S.%fZ')
        fechaPub = datetime.strptime(jsonRequest["fechaPublicacion"],'%Y-%m-%dT%H:%M:%S.%fZ')
        if(jsonRequest["diasRecordatorios"] is None):
            return {"response":"unsuccessful"}
        if(fecha-fechaPub < timedelta(days=1)):
            return {"response":"datesError"}
        if((fecha-fechaPub).days < jsonRequest["diasRecordatorios"]):
            return {"response":"reminderError"}
        try:    
            actividad =Actividad.objects.create(
                semana=jsonRequest["semana"],
                planTrabajo=Plantrabajo.objects.get(pk=jsonRequest["planTrabajo"]),
                tipo=Tipoactividad.objects.get(destipoactividad=jsonRequest["tipo"]),
                nombre=jsonRequest["nombre"],
                fecha=jsonRequest["fecha"][:-1],
                fechaPublicacion=jsonRequest["fechaPublicacion"][:-1],
                diasrecordatorios=jsonRequest["diasRecordatorios"],
                esvirtual=jsonRequest["esvirtual"],
                enlace=None if 'enlace' not in jsonRequest else jsonRequest["enlace"],
                afiche=afiche,
                estado=Estadoactividad.objects.get(desestado="planeada")
            )
        except:
            return {"response":"unsuccessful"}
        for responsable in jsonRequest["responsables"]:
            actividad.responsables.add(responsable)
        return {"response":"successful"}
    
    def modificarActividad(self,afiche,jsonRequest):
        if(not Actividad.objects.filter(idactividad=jsonRequest['idactividad']).exists()):
            return {"response":"existError"}
        
        actividad = Actividad.objects.get(pk=jsonRequest['idactividad'])
        
        if actividad.estado.desestado == 'cancelada' or \
           actividad.estado.desestado == 'realizada' :
            return {"response":"estadoError"}

        if not actividad.esvirtual and 'enlace' in jsonRequest:
            return {"response":"enlaceError"}

        if afiche is not None:
            actividad.afiche = afiche

        actividad.fedicion = timezone.now()
        for attribute in jsonRequest:
            match attribute:
                case "semana":
                    actividad.semana = jsonRequest["semana"]
                case "planTrabajo":
                    planTrabajo = None
                    try:
                        planTrabajo = Plantrabajo.objects.get(pk=jsonRequest["planTrabajo"])
                    except (ValueError, Plantrabajo.DoesNotExist):
                        return {"response":"tipoError"}
                    actividad.planTrabajo = planTrabajo
                case "tipo":
                    tipo = None
                    try:
                        tipo = Tipoactividad.objects.get(destipoactividad=jsonRequest["tipo"])
                    except (ValueError, Tipoactividad.DoesNotExist):
                        return {"response":"tipoError"}
                    actividad.tipo = tipo
                case "nombre":
                    actividad.nombre = jsonRequest["nombre"]
                case "fecha":
                    actividad.fecha = jsonRequest["fecha"][:-1]
                case "fechaPublication":
                    actividad.fechaPublicacion = jsonRequest["fechaPublication"][:-1]
                case "diasRecordatorios":
                    actividad.diasrecordatorios = jsonRequest["diasRecordatorios"]
                case "esvirtual":
                    actividad.esvirtual = jsonRequest["esvirtual"]
                case "enlace":
                    actividad.enlace = jsonRequest["enlace"]
        
        
        if 'responsables' in jsonRequest:
            for responsable in jsonRequest["responsables"]:
                if not Profesor.objects.filter(pk=responsable).exists():
                    return {'response':'responsableError'}
            try:
                for responsable in jsonRequest["responsables"]:
                    actividad.responsables.add(responsable)
            except:
                return {'response':'responsableError'}
                 

        try:
            actividad.save()
        except:
            return {'response':'unsuccessful'}

        return {"response":"successful"}

    def borrarActividad(self,request):
        if(not Actividad.objects.filter(idactividad=request['idactividad']).exists()):
            return {"response":"existError"}
        actividad = Actividad.objects.get(idactividad=request['idactividad'])
        Comentario.objects.filter(actividad=actividad).delete()
        actividad.delete()        

        return {"response":"successful"}
    
    def obtenerActividades(self,plan):
        return {"actividades":ListarActividadSerializer(Actividad.objects.filter(planTrabajo=plan),many=True).data}
    
    def obtenerAActividades(self):
        return {"actividades":ListarTodasActividadSerializer(Actividad.objects.all(),many=True).data}
    
    def obtenerTipoAct(self):
        return {"tipos":TipoActividadSerializer(Tipoactividad.objects.all(),many=True).data}
    
    def obtenerComentarios(self,plan):
        return {"actividades":ChatActividadSerializer(Actividad.objects.filter(planTrabajo=plan),many=True).data}

    def enviarComentarios(self,jsonRequest):
        if(not Actividad.objects.filter(idactividad=jsonRequest['idactividad']).exists()):
            return {"response":"existError"}
        actividad = Actividad.objects.get(pk=jsonRequest['idactividad'])
        Comentario(
            contenido=jsonRequest['comentario']['contenido'],
            autor=jsonRequest['comentario']['autor'],
            fecha=jsonRequest['comentario']['fecha'],
            actividad=actividad
        ).save()
        return {"response":"success"}

    def realizarActividad(self,jsonRequest,filelist):
        if(not Actividad.objects.filter(idactividad=jsonRequest['idactividad']).exists()):
            return {"response":"existError"}
        actividad = Actividad.objects.get(pk=jsonRequest['idactividad'])

        if actividad.estado.desestado == 'cancelada':
            return {"response":"estadoError"}

        if 'enlaceevidencia' in jsonRequest:
            actividad.enlaceevidencia = jsonRequest['enlaceevidencia']

        actividad.estado=Estadoactividad.objects.get(desestado="realizada")

        evidenciaslist=[]
        for imgfile in filelist:
            evidenciaslist.append(Evidencias(
                idactividad = actividad,
                imagen = imgfile
            ))

        try:
            Evidencias.objects.bulk_create(evidenciaslist)
        except:
            return {"response":"unsuccessful"}
        actividad.save()

        return {"response":"successful"}
    
    def cancelarActividad(self,idactividad,justificacion):
        if(not Actividad.objects.filter(idactividad=idactividad).exists()):
            return {"response":"existError"}
        actividad = Actividad.objects.get(pk=idactividad)
        if actividad.estado.desestado == 'realizada':
            return {"response":"estadoError"}
        actividad.estado=Estadoactividad.objects.get(desestado="cancelada")
        actividad.observacion = justificacion
        actividad.save()
        return {"response":"successful"}
    
    def publicarActividad(self,idactividad):
        if(not Actividad.objects.filter(idactividad=idactividad).exists()):
            return {"response":"existError"}
        actividad = Actividad.objects.get(pk=idactividad)
        if actividad.estado.desestado == 'cancelada' or \
           actividad.estado.desestado == 'realizada':
            return {"response":"estadoError"}
        actividad.estado=Estadoactividad.objects.get(desestado="notificada")
        actividad.save()
        return {"response":"successful"}

    def obtenerPlanesTrabajo(self):
        planes=PlanTrabajoSerializer(Plantrabajo.objects.all(),many=True)
        return {"planes" : planes.data}
    
    def obtenerPlanesCompletos(self):
        planes=PlanFullSerializer(Plantrabajo.objects.all(),many=True)
        return {"planes" : planes.data}
    
    def obtenerSedes(self):
        return {"sedes" : SedeSerializer(Sede.objects.all(),many=True).data}
    
    def obtenerRoles(self):
        return {"roles" : RolSerializer(Rol.objects.all(),many=True).data}

    """--------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Parte Andres
    --------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
    
    """
    @author: Andres
    @dev: Metodo del DAO que inserta una notificacion en la base de datos
    @param: _idemisor, integer con el id del usuario que genero la notificacion
            _contenido, string con el texto de la notificacion
            _fechahora, datetime del momento en el que se creo la notificacion
            _idreceptor, integer con el id de la persona que recibe la notificacion
    @returns: None
    """
    def insertarNotificacion(self, _idemisor, _contenido, _fechahora, _idreceptor):
        try:    
            notificacion = Notificacion.objects.create(
                    idreceptor_id = _idreceptor,
                    idemisor_id = _idemisor,
                    fechahora = _fechahora,
                    contenido = _contenido,
                    leida = False
                )
        except:
            return {"response":"unsuccessful"}

        return {"response":"successful"}


    """
    @author: Andres
    @dev: Metodo del DAO que borra en la base de datos todas las notificaciones asociadas a un usuario
    @param: _idreceptor, integer con el id de la persona que quiere eliminar todas las notificaciones
    @returns: None
    """
    def vaciarBuzon(self, idreceptor, request):
        if(not Notificacion.objects.filter(idreceptor=request['idreceptor']).exists()):
            return {"response":"existError"}
        notificacion = Notificacion.objects.get(idnotificacion=request['idnotificacion'])
        notificacion.delete()

    """
    @author: Andres
    @dev: Metodo del DAO retorna una notificacion en especifico de la base de datos
    @param: idnotificacion, integer con el id de la notificacion que se desea consultar
    @returns: Informacion de la notificacion consultada
    """
    def obtenerNotificacion(self, notificacion):
        return {"notificacion": NotificacionSerializer(Notificacion.objects.filter(notificacion=notificacion),many=True).data}

    """
    @author: Andres
    @dev: Metodo del DAO que actualiza en la base de datos el estado de una notificacion a leida
    @param: idnotificacion, integer con el id de la notificacion que se desea consultar
    @returns: None
    """
    def ponerComoLeida(self, idnotificacion):
        if (not Notificacion.objects.filter(idnotificacion=idnotificacion).exists()):
            return {"response": "existError"}
        notificacion = Notificacion.objects.get(pk=idnotificacion)
        notificacion.leida = True
        notificacion.save()
        return {"response": "successful"}

    """
    @author: Andres
    @dev: Metodo del DAO que actualiza en la base de datos el estado de una notificacion a NO leida
    @param: idnotificacion, integer con el id de la notificacion que se desea consultar
    @returns: None
    """
    def ponerComoNoLeida(self, idnotificacion):
        if (not Notificacion.objects.filter(idnotificacion=idnotificacion).exists()):
            return {"response": "existError"}
        notificacion = Notificacion.objects.get(pk=idnotificacion)
        notificacion.leida = False
        notificacion.save()
        return {"response": "successful"}


    """
    @author: Andres
    @dev: Metodo del DAO que retorna todas las notificaciones asociadas a un usuario. Trae de la base de datos. Este es para el frontend
    @param: idreceptor, integer con el id del usuario que quiere ver todas sus notificaciones
    @returns: Notificaciones de ese usuario
    """
    def obtenerTodasNotificaciones(self, idreceptor):
        notificaciones = NotificacionSerializer(Notificacion.objects.filter(idreceptor=idreceptor), many=True)
        return {"notificiones": notificaciones.data}


    # Mensajes --------------------------------------------------------------------------------------------------------------------------------------------------------------------

    """
    @author: Andres
    @dev: Metodo del DAO que inserta una notificacion en la base de datos
    @param: _idemisor, integer con el id del usuario que genero la notificacion
            _contenido, string con el texto de la notificacion
            _fechahora, datetime del momento en el que se creo la notificacion
            _idreceptor, integer con el id de la persona que recibe la notificacion
    @returns: None
    """
    def crearMensaje(self, _idreceptor, _contenido, _fechahora, _idgrupo):
        try:
            mensaje = Notificacion.objects.create(
                    idreceptor_id = _idreceptor,
                    fechahora = _fechahora,
                    contenido = _contenido,
                    idgrupo_id = _idgrupo
                )
        except:
            return {"response":"unsuccessful"}

        return {"response":"successful"}

    """
    @author: Andres
    @dev: Metodo del DAO que retorna todas las notificaciones asociadas a un usuario. Trae de la base de datos. Este es para el frontend
    @param: idreceptor, integer con el id del usuario que quiere ver todas sus notificaciones
    @returns: Notificaciones de ese usuario
    """
    def obtenerTodosMensajes(self, idgrupo):
        mensajes = MensajeSerializer(Mensaje.objects.filter(idgrupo=idgrupo), many=True)
        return {"mensajes": mensajes.data}

    """
    Parte activar actividades --------------------------------------------------------------------------------------------------------------------------------------------------------------------
    @author: Andres
    @dev: Metodo del DAO que pone en la base de datos el estado de una actividad en activar
    @param: actividad
    @returns: None
    """
    def activarActividad(self,actividad):
        actividad.estado=Estadoactividad.objects.get(desestado="activar")
        actividad.save()
        return {"response":"successful"}

# Prueba para ver si esta insertando bien en la base de datos
SingletonDAO.getInstance().insertarNotificacion(1, "Primer notificacion", datetime.datetime.now(), 2020127158)