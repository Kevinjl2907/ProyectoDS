from rest_framework import serializers

from base.models import *

from datetime import timedelta,date

class SedeSerializer(serializers.Serializer):
    idsede = serializers.IntegerField(read_only=True)
    codigosede = serializers.CharField()

    class Meta:
        managed = True
        db_table = 'Sede'

    def create(self, validated_data):
            return Sede.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.idsede = validated_data.get('idSede', instance.idsede)
        instance.codigosede = validated_data.get('codigosede', instance.codigosede)
        instance.save()
        return instance


class EstudianteSerializer(serializers.Serializer):
    carnet = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(max_length=45)
    nombreadicional = serializers.CharField(max_length=45) 
    apellido1 = serializers.CharField(max_length=45)
    apellido2 = serializers.CharField(max_length=45)
    sede = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Sede.objects.all())
    correotec = serializers.EmailField(max_length=50)  
    fedicion = serializers.DateTimeField(required=False)
    editor = serializers.CharField(required=False, max_length=120)
    fcreacion = serializers.DateTimeField()

    class Meta:
        managed = True
        db_table = 'Estudiante'

    def create(self, validated_data):
        return Estudiante.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.idEstDB = validated_data.get('idEstdb', instance.idestdb)
        instance.id = validated_data.get('id', instance.id)
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.nombreadicional = validated_data.get('nombreAdicional', instance.nombreadicional)
        instance.apellido1 = validated_data.get('apellido1', instance.apellido1)
        instance.apellido2 = validated_data.get('apellido2', instance.apellido2)
        instance.sede = validated_data.get('sede', instance.sede)
        instance.correotec = validated_data.get('correoTec', instance.correotec)
        instance.fedicion = validated_data.get('fedicion', instance.fedicion)
        instance.editor = validated_data.get('editor', instance.editor)
        instance.fcreacion = validated_data.get('fcreacion', instance.fcreacion)

        instance.save()
        return instance
    
class ListaEstudianteSerializer(serializers.Serializer):
    carnet = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(max_length=45)
    nombreadicional = serializers.CharField(max_length=45) 
    apellido1 = serializers.CharField(max_length=45)
    apellido2 = serializers.CharField(max_length=45)
    sede = serializers.SerializerMethodField('getSede')
    correotec = serializers.EmailField(max_length=50)
    telefono = serializers.IntegerField()

    class Meta:
        managed = False
        db_table = 'Estudiante'

    def create(self, validated_data):
        return Estudiante.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.nombreadicional = validated_data.get('nombreAdicional', instance.nombreadicional)
        instance.apellido1 = validated_data.get('apellido1', instance.apellido1)
        instance.apellido2 = validated_data.get('apellido2', instance.apellido2)
        instance.sede = validated_data.get('sede', instance.sede)
        instance.correotec = validated_data.get('correoTec', instance.correotec)

        instance.save()
        return instance
    
    def getSede(self,instance):
        return instance.sede.codigosede
    

class AsistenteadministrativoSerializer(serializers.Serializer):
    idasistente = serializers.IntegerField(read_only=True)
    auth = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=User.objects.all())
    nombre = serializers.CharField(max_length=45)
    apellido1 = serializers.CharField(max_length=45)
    apellido2 = serializers.CharField(max_length=45)
    sede = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Sede.objects.all())

    class Meta:
        managed = True
        db_table = 'AsistenteAdministrativo'

    def create(self, validated_data):
        return Asistenteadministrativo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.idasistente = validated_data.get('idAsistente', instance.idasistente)
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.auth = validated_data.get('auth', instance.auth)
        instance.apellido1 = validated_data.get('apellido1', instance.apellido1)
        instance.apellido2 = validated_data.get('apellido2', instance.apellido2)
        instance.sede = validated_data.get('sede', instance.sede)

        instance.save()
        return instance
    
    def getemail(self, instance):
        user = User.objects.get(username=instance.auth)
        return user.email
    

class RolSerializer(serializers.Serializer):
    idrol = serializers.IntegerField(read_only=True)
    desrol = serializers.CharField(max_length=45)

    class Meta:
        managed = True
        db_table = 'Rol'
    
    def create(self, validated_data):
        return Rol.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.idrol = validated_data.get('idRol', instance.idrol)
        instance.desrol = validated_data.get('desRrol', instance.desrol)

        instance.save()
        return instance
    

class ProfesorSerializer(serializers.Serializer):
    codigo = serializers.CharField(max_length=45)
    numprofesor = serializers.IntegerField()
    idsede = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Sede.objects.all())
    auth = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=User.objects.all())
    nombre = serializers.CharField(max_length=45)
    apellido1 = serializers.CharField(max_length=45)
    apellido2 = serializers.CharField(max_length=45)
    oficina = serializers.CharField(max_length=45) 
    teloficina = serializers.IntegerField() 
    telcelular = serializers.IntegerField() 
    fotografia = serializers.ImageField(required=False, allow_null=True)
    fcreacion = serializers.DateTimeField()
    fedicion = serializers.DateTimeField(required=False)

    class Meta:
        managed = True
        db_table = 'Profesor'
    
    def create(self, validated_data):
        return Profesor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.numprofesor = validated_data.get('numprofesor', instance.idprofesor)
        instance.idsede = validated_data.get('idSede', instance.idsede)
        instance.codigo = validated_data.get('codigo', instance.codigo)
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.auth = validated_data.get('auth', instance.auth)
        instance.apellido1 = validated_data.get('apellido1', instance.apellido1)
        instance.apellido2 = validated_data.get('apellido2', instance.apellido2)
        instance.oficina = validated_data.get('oficina', instance.oficina)
        instance.teloficina = validated_data.get('teloficina', instance.teloficina)
        instance.telcelular = validated_data.get('telcelular', instance.telcelular)
        instance.fotografia = validated_data.get('fotografia', instance.fotografia)
        instance.rol = validated_data.get('rol', instance.rol)
        instance.fcreacion = validated_data.get('fcreacion', instance.fcreacion)
        instance.fedicion = validated_data.get('fedicion', instance.fedicion)

        instance.save()
        return instance
    
    def getemail(self, instance):
        user = User.objects.get(username=instance.auth)
        return user.email
    
class ProfesorEquipoSerializer(serializers.Serializer):
    codigo = serializers.CharField(max_length=45)
    numprofesor = serializers.IntegerField()
    sede = serializers.SerializerMethodField('getSede')
    correo = serializers.SerializerMethodField('getCorreo')
    nombre = serializers.CharField(max_length=45)
    apellido1 = serializers.CharField(max_length=45)
    apellido2 = serializers.CharField(max_length=45)
    rol = serializers.SerializerMethodField('getRol')
    oficina = serializers.CharField(max_length=45)
    teloficina = serializers.IntegerField()
    telcelular = serializers.IntegerField()
    fotografia = serializers.ImageField()
    fedicion = serializers.DateTimeField(required=False)
    class Meta:
        managed = False
        db_table = 'Profesor'
    
    def getSede(self,instance):
        return instance.idsede.codigosede
    
    def getRol(self,instance):
        if(Docentes.objects.filter(idprofesor=instance).count() <= 0 ):
            return 'NaN'
        return Docentes.objects.get(idprofesor=instance).rol.desrol

    def getCorreo(self,instance):
        return instance.auth.email
    
class ResponsablesSerializer(serializers.Serializer):
    nombre = serializers.SerializerMethodField('getFNombre')
    class Meta:
        managed = False
        db_table = 'Profesor'
    
    def getSede(self,instance):
        return instance.idsede.codigosede
    
    def getRol(self,instance):
        if(Docentes.objects.filter(idprofesor=instance).count() <= 0 ):
            return 'NaN'
        return Docentes.objects.get(idprofesor=instance).rol.desrol

    def getCorreo(self,instance):
        return instance.auth.email

    def getFNombre(self,instance):
        return "{} {} {}".format(instance.nombre,instance.apellido1,instance.apellido2)
    

class DocentesSerializer(serializers.Serializer):
    idlistadocentes = serializers.IntegerField(read_only=True)
    idequipotrabajo = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Equipotrabajo.objects.all())
    idprofesor = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Profesor.objects.all())
    rol = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Rol.objects.all())

    class Meta:
        managed = True
        db_table = 'Docentes'

    def create(self, validated_data):
        return Docentes.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.idlistadocentes = validated_data.get('idListaDocentes', instance.idListaDocentes)
        instance.idequipotrabajo = validated_data.get('idEquipotrabajo', instance.idequipotrabajo)
        instance.idprofesor = validated_data.get('idProfesor', instance.idprofesor)
        instance.esrepresentante = validated_data.get('esRepresentante', instance.esrepresentante)

        instance.save()
        return instance
    

class EquipoTrabajoSerializer(serializers.Serializer):
    idequipotrabajo = serializers.IntegerField(read_only=True)
    coordinador = serializers.IntegerField(required=False)
    docentes = ProfesorSerializer(many=True, read_only=True)
    fedicion = serializers.DateTimeField(required=False)
    editor = serializers.CharField(required=False, max_length=120)

    class Meta:
        managed = True
        db_table = 'EquipoTrabajo'

    def create(self, validated_data):
        return Equipotrabajo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.idequipotabajo = validated_data.get('idEquipotabajo', instance.idequipotabajo)
        instance.coordinador = validated_data.get('coordinador', instance.coordinador)
        instance.docentes.set(validated_data.get('docentes', instance.docentes.all()))
        instance.fedicion = validated_data.get('fedicion', instance.fedicion)
        instance.editor = validated_data.get('editor', instance.editor)
        
        docentes = validated_data.get('docentes')
        if docentes:
            instance.docentes.set(docentes)
      
        instance.save()
        return instance

class ProfesEquipoTrabajoSerializer(serializers.Serializer):
    coordinador = ProfesorEquipoSerializer(many=False, read_only=True)
    docentes = ProfesorEquipoSerializer(many=True, read_only=True)

    class Meta:
        managed = False
        db_table = 'EquipoTrabajo'

    def create(self, validated_data):
        return Equipotrabajo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.coordinador = validated_data.get('coordinador', instance.coordinador)
        instance.docentes.set(validated_data.get('docentes', instance.docentes.all()))
        
        docentes = validated_data.get('docentes')
        if docentes:
            instance.docentes.set(docentes)
      
        instance.save()
        return instance

class ProfesEquipoTrabajoSerializer(serializers.Serializer):
    docentes = ProfesorEquipoSerializer(many=True, read_only=True)

    class Meta:
        managed = False
        db_table = 'EquipoTrabajo'


class TipoActividadSerializer(serializers.Serializer):
    idtipoactividad = serializers.IntegerField(read_only=True)
    destipoactividad = serializers.CharField()

    class Meta:
        managed = True
        db_table = 'TipoActividad'

    def create(self, validated_data):
        return Tipoactividad.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.idtipoactividad = validated_data.get('idTipoActividad', instance.idtipoactividad)
        instance.destipoactividad = validated_data.get('desTipoActividad', instance.destipoactividad)
       
        instance.save()
        return instance
    

class EstadoActividadSerializer(serializers.Serializer):
    idestado = serializers.IntegerField(read_only=True)
    desestado = serializers.CharField(max_length=45)

    class Meta:
        managed = True
        db_table = 'EstadoActividad'
    
    def create(self, validated_data):
        return Estadoactividad.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.idestado = validated_data.get('idEstado', instance.idrol)
        instance.desestado = validated_data.get('desestado', instance.desrol)

        instance.save()
        return instance
    
    
class ComentarioSerializer(serializers.Serializer):
        idcomentario = serializers.IntegerField(read_only=True)
        contenido = serializers.CharField(max_length=250)
        fecha = serializers.DateTimeField()
        autor = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Profesor.objects.all())
        actividad = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Actividad.objects.all())

        class Meta:
                managed = True
                db_table = 'Comentario'

        def create(self, validated_data):
            return Comentario.objects.create(**validated_data)
        
        def update(self, instance, validated_data):
            instance.idcomentario = validated_data.get('idComentario', instance.idcomentario)     
            instance.contenido = validated_data.get('contenido', instance.contenido)
            instance.fecha = validated_data.get('fecha', instance.fecha)
            instance.autor_id = validated_data.get('autor', instance.autor_id)
            instance.actividad_id = validated_data.get('actividad', instance.actividad_id)
            
            instance.save()
            return instance

        def getAutor(self, instance):
            return instance.autor.codigo

class ComentarioChatSerializer(serializers.Serializer):
        contenido = serializers.CharField(max_length=250)
        fecha = serializers.DateTimeField()
        autor =  serializers.SerializerMethodField('getAutor')
        actividad = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Actividad.objects.all())

        class Meta:
                managed = True
                db_table = 'Comentario'

        def getAutor(self, instance):
            return { 
                "nombre": "{} {} {}".format(instance.autor.nombre,
                                    instance.autor.apellido1,
                                    instance.autor.apellido2),
                "foto": instance.autor.fotografia.url if str(instance.autor.fotografia) != '' else ''
            }
        
        def jsonFecha(self,instance):
            return "2015-16-19 07:00:00"


class ActividadSerializer(serializers.Serializer):
    idactividad = serializers.IntegerField(read_only=True)
    semana = serializers.IntegerField()
    tipo = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Tipoactividad.objects.all())
    planTrabajo = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Plantrabajo.objects.all())
    nombre = serializers.CharField(max_length=45)
    fecha = serializers.DateTimeField()
    fechaPublicacion = serializers.DateTimeField()
    diasrecordatorios = serializers.IntegerField()
    esvirtual = serializers.IntegerField() 
    enlace = serializers.CharField(required=False,max_length=100)
    afiche = serializers.ImageField(required=False)
    estado = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Estadoactividad.objects.all())
    responsables = ProfesorSerializer(many=True, required= False)
    #responsables = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=Profesor.objects.all(), required=False)
    comentarios = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=Comentario.objects.all(), required=False)
    observacion = serializers.CharField(required=False, max_length=150)
    fedicion = serializers.DateTimeField(required=False)
    editor = ProfesorSerializer(required=False)
    
    class Meta:
        managed = True
        db_table = 'Actividad'

    def create(self, validated_data):
        return Actividad.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.idactividad = validated_data.get('idActividad', instance.idactividad)
        instance.semana = validated_data.get('semana', instance.semana)
        instance.tipo = validated_data.get('tipo', instance.tipo)
        instance.planTrabajo = validated_data.get('planTrabajo', instance.planTrabajo)
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.fecha = validated_data.get('fecha', instance.fecha)
        instance.fechaPublicacion = validated_data.get('fechaPublicacion', instance.fechaPublicacion)
        instance.diasrecordatorios = validated_data.get('diasrecordatorios', instance.diasrecordatorios)
        instance.esvirtual = validated_data.get('esvirtual', instance.esvirtual)
        instance.enlace = validated_data.get('enlace', instance.enlace)
        instance.afiche = validated_data.get('afiche', instance.afiche)
        instance.estado = validated_data.get('estado', instance.estado)
        instance.observacion = validated_data.get('observacion', instance.observacion)
        instance.fedicion = validated_data.get('fedicion', instance.fedicion)
        instance.editor = validated_data.get('editor', instance.editor)
                
        responsables = validated_data.get('responsables')
        if responsables:
            instance.responsables.set(responsables)
            
        comentarios = validated_data.get('comentarios')
        if comentarios:
            instance.comentarios.set(comentarios)
        
        instance.save()
        return instance
    
class ListarActividadSerializer(serializers.Serializer):
    idactividad = serializers.IntegerField(read_only=True)
    semana = serializers.IntegerField()
    planTrabajo = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Plantrabajo.objects.all())
    tipo = serializers.SerializerMethodField('getTipo')
    nombre = serializers.CharField(max_length=45)
    fecha = serializers.DateTimeField()
    fechaPublicacion = serializers.DateTimeField()  
    diasrecordatorios = serializers.IntegerField()
    esvirtual = serializers.BooleanField() 
    enlace = serializers.CharField(required=False,max_length=100)
    afiche = serializers.ImageField(required=False)
    estado = serializers.SerializerMethodField('getEstado')
    responsables = ProfesorEquipoSerializer(many=True, read_only=True)

    class Meta:
        managed = True
        db_table = 'Actividad'
    
    def getTipo(self, instance):
        return instance.tipo.destipoactividad

    def getEstado(self, instance):
        return instance.estado.desestado
    
class ListarTodasActividadSerializer(serializers.Serializer):
    semana = serializers.IntegerField()
    planTrabajo = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Plantrabajo.objects.all())
    tipo = serializers.SerializerMethodField('getTipo')
    nombre = serializers.CharField(max_length=45)
    fecha = serializers.DateTimeField()
    fechaPublicacion = serializers.DateTimeField()  
    diasrecordatorios = serializers.IntegerField()
    esvirtual = serializers.BooleanField() 
    enlace = serializers.CharField(required=False,max_length=100)
    afiche = serializers.ImageField(required=False)
    estado = serializers.SerializerMethodField('getEstado')
    responsables = serializers.SerializerMethodField('getResponsables')

    class Meta:
        managed = True
        db_table = 'Actividad'
    
    def getTipo(self, instance):
        return instance.tipo.destipoactividad

    def getEstado(self, instance):
        return instance.estado.desestado
    
    def getResponsables(self,instance):
        returnList = []
        for responsable in instance.responsables.all():
            returnList.append("{} {} {}".format(responsable.nombre,
                                    responsable.apellido1,
                                    responsable.apellido2))
        return returnList

class ChatActividadSerializer(serializers.Serializer):
    idactividad = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(max_length=45)
    comentarios = serializers.SerializerMethodField('getComentarios')

    class Meta:
        managed = True
        db_table = 'Actividad'
    
    def getComentarios(self, instance):
        return ComentarioChatSerializer(Comentario.objects.filter(actividad=instance.idactividad).order_by('fecha'),many=True).data


class PlanTrabajoSerializer(serializers.Serializer):
    semestre = serializers.CharField(max_length=8)
    semanainicial = serializers.DateField()  
    semanafinal = serializers.DateField()
    semanas = serializers.SerializerMethodField('getSemanas')

    class Meta:
        managed = True
        db_table = 'PlanTrabajo'

    def create(self, validated_data):
        return Plantrabajo.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.idplantrabajo = validated_data.get('idPLanTrabajo', instance.idplantrabajo)
        instance.id = validated_data.get('id', instance.id)
        instance.semanainicial = validated_data.get('semanainicial', instance.semanainicial)
        instance.semanafinal = validated_data.get('semanafinal', instance.semanafinal)
        actividades_data = validated_data.get('actividades', [])
        
        for actividad_data in actividades_data:
            Actividad.objects.create(plan_trabajo=instance, **actividad_data)
        
        instance.save()
        return instance

    def getSemanas(self,instance):
        vacaciones = Semanasvacaciones.objects.filter(semestre=instance.semestre).values_list("semanavacacional",flat=True)
        listaSemanas = []
        datetoappend = instance.semanainicial
        while len(listaSemanas) < 16:
            datetoappend = datetoappend+timedelta(days=7)
            while True:
                if datetoappend not in vacaciones:
                    break
                datetoappend = datetoappend+timedelta(days=7)
            listaSemanas.append(str(datetoappend) + " CST")
        return listaSemanas

class PlanFullSerializer(serializers.Serializer):
    semestre = serializers.CharField(max_length=8)
    semanainicial = serializers.DateField()  
    semanafinal = serializers.DateField()
    semanas = serializers.SerializerMethodField('getSemanas')
    actividades = serializers.SerializerMethodField('getActividades')

    class Meta:
        managed = True
        db_table = 'PlanTrabajo'

    def create(self, validated_data):
        return Plantrabajo.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.idplantrabajo = validated_data.get('idPLanTrabajo', instance.idplantrabajo)
        instance.id = validated_data.get('id', instance.id)
        instance.semanainicial = validated_data.get('semanainicial', instance.semanainicial)
        instance.semanafinal = validated_data.get('semanafinal', instance.semanafinal)
        actividades_data = validated_data.get('actividades', [])
        
        for actividad_data in actividades_data:
            Actividad.objects.create(plan_trabajo=instance, **actividad_data)
        
        instance.save()
        return instance
    
    def getActividades(self,instance):
        return ListarTodasActividadSerializer(Actividad.objects.filter(planTrabajo=instance),many=True, read_only=True).data

    def getSemanas(self,instance):
        vacaciones = Semanasvacaciones.objects.filter(semestre=instance.semestre).values_list("semanavacacional",flat=True)
        return list(vacaciones)
    
    
class SemanasVacacionesSerializer(serializers.Serializer):
    idsemanasvacaciones = serializers.IntegerField(read_only=True)
    semanavacacional = serializers.DateField()  
    idplantrabajo = serializers.PrimaryKeyRelatedField(many=False, read_only=False, queryset=Plantrabajo.objects.all())

    class Meta:
        managed = True
        db_table = 'SemanasVacaciones'

    def create(self, validated_data):
        return Semanasvacaciones.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.idsemanasvacaciones = validated_data.get('idSemanasVacaciones', instance.idsemanasvacaciones)
        instance.semanavacacional = validated_data.get('semanavacacional', instance.semanavacacional)
        instance.idplantrabajo = validated_data.get('idplantrabajo', instance.idplantrabajo)

        instance.save()
        return instance




"""--------------------------------------------------------------------------------------------------------------------------------------------------------------------
Parte Andres
--------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
class NotificacionSerializer(serializers.Serializer):
    idnotificacion = serializers.AutoField(db_column='idNotificacion', primary_key=True)  # Field name made lowercase.
    idreceptor_id = serializers.IntegerField()
    idemisor_id = serializers.IntegerField()
    fechahora = serializers.DateTimeField()
    contenido = serializers.CharField(max_length=1000)
    leida = serializers.BooleanField(db_column='leida')

    class Meta:
        managed = True
        db_table = 'Notificacion'


class MensajeSerializer(serializers.Serializer):
    idmensaje = serializers.AutoField(db_column='idNotificacion', primary_key=True)  # Field name made lowercase.
    idemisor = serializers.IntegerField()
    fechahora = serializers.DateTimeField()
    contenido = serializers.CharField(max_length=1000)
    leida = serializers.BooleanField(db_column='leida')

    class Meta:
        managed = True
        db_table = 'Notificacion'