# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
import Controllers.ObserverNotificacion as O

class Sede(models.Model):
    idsede = models.AutoField(db_column='idSede', primary_key=True)  # Field name made lowercase.
    codigosede = models.CharField(db_column='codigoSede', max_length=2)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Sede'


"""--------------------------------------------------------------------------------------------------------------------------------------------------------------------
Parte Andres
--------------------------------------------------------------------------------------------------------------------------------------------------------------------"""

class Estudiante(models.Model, O.Observer):
    carnet = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=45)
    nombreadicional = models.CharField(db_column='nombreAdicional', max_length=45)  # Field name made lowercase.
    apellido1 = models.CharField(max_length=45)
    apellido2 = models.CharField(max_length=45)
    sede = models.ForeignKey('Sede', models.DO_NOTHING, db_column='sede')
    telefono = models.IntegerField(null=True)
    correotec = models.CharField(db_column='correoTec', max_length=50)  # Field name made lowercase.
    fedicion = models.DateTimeField(blank=True, null=True)
    editor = models.CharField(max_length=120, blank=True, null=True)
    fcreacion = models.DateTimeField()

    # Metodos de la interfaz Observer

    """
    @author: Andres
    @dev: Notifica que hubo un cambio, Se debe discutir con la gente de front end como desplegarlo
    @param: None
    @returns: None
    """
    def update(self):
        # Hablar con Rayforth o Andrey que trigger ocupan para saber que el front end debe actualizar
        print("Recibiste una nueva notificacion")

    """
    @author: Andres
    @dev: Obtiene un Integer del id asociado, en este caso el carnet
    @param: None
    @returns: Integer del id asociado, en este caso el carnet
    """
    def getId(self):
        return self.carnet

    """
    @author: Andres
    @dev: Obtiene un Integer del id asociado, en este caso el carnet
    @param: None
    @returns: Integer del id asociado, en este caso el carnet
    """
    def getSede(self):
        return self.sede

    """
    @author: Andres
    @dev: Indica si el usuario es estudiante o no
    @param: None
    @returns: True
    """
    def esEstudiante(self):
        return True

    class Meta:
        managed = True
        db_table = 'Estudiante'



class Asistenteadministrativo(models.Model):
    idasistente = models.AutoField(db_column='idAsistente', primary_key=True)  # Field name made lowercase.
    auth = models.OneToOneField(User,on_delete=models.CASCADE)
    nombre = models.CharField(max_length=45)
    apellido1 = models.CharField(max_length=45)
    apellido2 = models.CharField(max_length=45)
    sede = models.ForeignKey('Sede', models.DO_NOTHING, db_column='sede')

    """
    @author: Andres
    @dev: Obtiene un Integer del id asociado, en este caso el carnet
    @param: None
    @returns: Integer del id asociado, en este caso el carnet
    """
    def getSede(self):
        return self.sede

    """
    @author: Andres
    @dev: Indica si el usuario es estudiante o no
    @param: None
    @returns: False
    """
    def esEstudiante(self):
        return False

    class Meta:
        managed = True
        db_table = 'AsistenteAdministrativo'


"""--------------------------------------------------------------------------------------------------------------------------------------------------------------------
Termina Parte Andres
Pero vuelve a seguir mas abajo
--------------------------------------------------------------------------------------------------------------------------------------------------------------------"""


class Rol(models.Model):
    idrol = models.AutoField(db_column='idRol', primary_key=True)  # Field name made lowercase.
    desrol = models.CharField(db_column='desRol', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Rol'



"""--------------------------------------------------------------------------------------------------------------------------------------------------------------------
Parte Andres
--------------------------------------------------------------------------------------------------------------------------------------------------------------------"""

class Profesor(models.Model, O.Observer):
    codigo = models.CharField(max_length=45, primary_key=True)
    numprofesor = models.IntegerField(db_column='numprofesor')  # Field name made lowercase.
    idsede = models.ForeignKey('Sede', models.DO_NOTHING, db_column='sede')
    auth = models.OneToOneField(User,on_delete=models.CASCADE)
    nombre = models.CharField(max_length=45)
    apellido1 = models.CharField(max_length=45)
    apellido2 = models.CharField(max_length=45)
    oficina = models.CharField(max_length=45)
    teloficina = models.IntegerField(db_column='telOficina')  # Field name made lowercase.
    telcelular = models.IntegerField(db_column='telCelular')  # Field name made lowercase.
    fotografia = models.ImageField(upload_to="profes/", blank=True, null=True)
    fcreacion = models.DateTimeField()
    fedicion = models.DateTimeField(blank=True, null=True)

    # Metodos de la interfaz Observer

    """
    @author: Andres
    @dev: Notifica que hubo un cambio, Se debe discutir con la gente de front end como desplegarlo
    @param: None
    @returns: None
    """
    def update(self):
        # Hablar con Rayforth o Andrey que trigger ocupan para saber que el front end debe actualizar
        print("Recibiste una nueva notificacion")

    """
    @author: Andres
    @dev: Obtiene un Integer del id asociado, en este caso el carnet
    @param: None
    @returns: Integer del id asociado, en este caso el carnet
    """
    def getId(self):
        return self.codigo

    """
    @author: Andres
    @dev: Obtiene un Integer del id asociado, en este caso el carnet
    @param: None
    @returns: Integer del id asociado, en este caso el carnet
    """
    def getSede(self):
        return self.idsede

    """
    @author: Andres
    @dev: Indica si el usuario es estudiante o no
    @param: None
    @returns: False
    """
    def esEstudiante(self):
        return False

    class Meta:
        managed = True
        db_table = 'Profesor'



"""--------------------------------------------------------------------------------------------------------------------------------------------------------------------
Termina Parte Andres
Pero vuelve a seguir mas abajo
--------------------------------------------------------------------------------------------------------------------------------------------------------------------"""


class FotoProfesor(models.Model):
    idfoto = models.AutoField(primary_key=True)
    idprofesor = models.ForeignKey(Profesor,models.DO_NOTHING)
    foto = models.ImageField(upload_to="fotos/") # <- Esto indica que tenemos un campo para fotos

    class Meta:
        managed = True
        db_table = 'FotoProfesor'


class Docentes(models.Model):
    idlistadocentes = models.AutoField(db_column='idListaDocentes', primary_key=True)  # Field name made lowercase.
    idequipotrabajo = models.ForeignKey('Equipotrabajo', models.DO_NOTHING, db_column='idEquipoTrabajo',related_name='+')  # Field name made lowercase.
    idprofesor = models.ForeignKey('Profesor', models.DO_NOTHING, db_column='idProfesor')  # Field name made lowercase.
    rol = models.ForeignKey('Rol', models.DO_NOTHING, db_column='rol')
    
    class Meta:
        managed = True
        db_table = 'Docentes'


class Equipotrabajo(models.Model):
    idequipotrabajo = models.AutoField(db_column='idEquipoTrabajo', primary_key=True)  # Field name made lowercase.
    docentes = models.ManyToManyField(Profesor,through=Docentes)
    fedicion = models.DateTimeField(blank=True, null=True)
    editor = models.ForeignKey('Asistenteadministrativo', models.DO_NOTHING, db_column='idEditor', null=True) 

    class Meta:
        managed = True
        db_table = 'EquipoTrabajo'


class Tipoactividad(models.Model):
    idtipoactividad = models.AutoField(db_column='idTipoActividad', primary_key=True)  # Field name made lowercase.
    destipoactividad = models.CharField(db_column='desTipoActividad', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'TipoActividad'


class Estadoactividad(models.Model):
    idestado = models.AutoField(db_column='idEstado', primary_key=True)  # Field name made lowercase.
    desestado = models.CharField(max_length=45)

    class Meta:
        managed = True
        db_table = 'EstadoActividad'
        
        
class Actividad(models.Model):
    idactividad = models.AutoField(db_column='idActividad', primary_key=True)  # Field name made lowercase.
    semana = models.IntegerField()
    planTrabajo = models.ForeignKey('Plantrabajo',models.DO_NOTHING)
    tipo = models.ForeignKey('Tipoactividad', models.DO_NOTHING, db_column='tipo')
    nombre = models.CharField(max_length=45)
    fecha = models.DateTimeField()
    fechaPublicacion = models.DateTimeField()  # Field name made lowercase.
    diasrecordatorios = models.IntegerField(db_column='diasRecordatorios')  # Field name made lowercase.
    esvirtual = models.BooleanField(db_column='esVirtual')  # Field name made lowercase.
    enlace = models.CharField(max_length=100, blank=True, null=True)
    afiche = models.ImageField(upload_to="afiches/")
    estado = models.ForeignKey('Estadoactividad', models.DO_NOTHING, db_column='estado')
    responsables = models.ManyToManyField(Profesor,db_table='Responsable')
    enlaceevidencia = models.CharField(max_length=200, blank=True, null=True)
    observacion = models.CharField(max_length=300, blank=True, null=True)
    fedicion = models.DateTimeField(blank=True, null=True)
    editor = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'Actividad'
        
        
class Comentario(models.Model):
    idcomentario = models.AutoField(db_column='idComentario', primary_key=True)  # Field name made lowercase.
    contenido = models.CharField(max_length=250)
    fecha = models.DateTimeField()
    autor = models.ForeignKey('Profesor', models.DO_NOTHING, db_column='autor')
    actividad = models.ForeignKey(Actividad, models.DO_NOTHING, db_column='actividad', related_name="+")

    class Meta:
        managed = True
        db_table = 'Comentario'

class Plantrabajo(models.Model):
    semestre = models.CharField(max_length=8,primary_key=True)
    semanainicial = models.DateField(db_column='semanaInicial')  # Field name made lowercase.
    semanafinal = models.DateField()
    actividades = models.ManyToManyField(Actividad,db_table='ActividadesPlanTrabajo')

    class Meta:
        managed = True
        db_table = 'PlanTrabajo'

class Semanasvacaciones(models.Model):
    idsemanasvacaciones = models.AutoField(db_column='idSemanasVacaciones', primary_key=True)  # Field name made lowercase.
    semanavacacional = models.DateField(db_column='semanaVacacional')  # Field name made lowercase.
    semestre = models.ForeignKey(Plantrabajo, models.DO_NOTHING, db_column='idPlanTrabajo')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'SemanasVacaciones'

class Evidencias(models.Model):
    idevidencia = models.AutoField(primary_key=True)
    idactividad = models.ForeignKey(Actividad,models.DO_NOTHING)
    imagen = models.ImageField(upload_to="evidencias/")

    class Meta:
        managed = True
        db_table = 'Evidencias'

"""--------------------------------------------------------------------------------------------------------------------------------------------------------------------
Parte Andres
--------------------------------------------------------------------------------------------------------------------------------------------------------------------"""
    
class Notificacion(models.Model):
    idnotificacion = models.AutoField(db_column='idNotificacion', primary_key=True)  # Field name made lowercase.
    idreceptor_id = models.IntegerField()
    idemisor_id = models.IntegerField()
    fechahora = models.DateTimeField()
    contenido = models.CharField(max_length=1000)
    leida = models.BooleanField(db_column='leida')
    
    class Meta:
        managed = True
        db_table = 'Notificacion'



class Mensaje(models.Model):
    idmensaje = models.AutoField(db_column='idNotificacion', primary_key=True)  # Field name made lowercase.
    idemisor = models.IntegerField()
    idgrupo = models.IntegerField()
    fechahora = models.DateTimeField()
    contenido = models.CharField(max_length=1000)

    class Meta:
        managed = True
        db_table = 'Notificacion'