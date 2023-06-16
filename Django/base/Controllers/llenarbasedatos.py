from base.models import *
from django.utils import timezone
from random import randint
from datetime import datetime

def sede():
    if(Sede.objects.count() > 0):
        return
    Sede.objects.create(
            codigosede='CA'
        )
    Sede.objects.create(
            codigosede='LI'
        )
    Sede.objects.create(
            codigosede='SJ'
        )
    Sede.objects.create(
            codigosede='AL'
        )

def rol():
    if(Rol.objects.count() > 0):
        return
    Rol.objects.create(
        desrol='Coordinador'
    )

    Rol.objects.create(
        desrol='Representante'
    )
def profesores():
    if(Profesor.objects.count()>0):
        return
    for i in range(1,20):
        sede = Sede.objects.all()[randint(0,3)]

        authe = User.objects.create_user(
            username="correoprof"+str(i)+"@gmail.com",
            email="correoprof"+str(i)+"@gmail.com",
            password="11111111"
        )

        Profesor.objects.create(
            codigo=sede.codigosede+str(i+1),
            numprofesor = i,
            idsede=sede,
            auth=authe,
            nombre="Prof"+str(i),
            apellido1="apellido1#"+str(i),
            apellido2="apellido2#"+str(i),
            oficina="II-"+str(i),
            fcreacion=timezone.now(),
            teloficina=83249329+i,
            telcelular=83249329+i,
        )
        

def equipoTrabajo():
    if(Equipotrabajo.objects.count() > 0):
        return

    sede = Sede.objects.all()[randint(0,3)]

    coord = Rol.objects.get(
        desrol='Coordinador'
    )

    guia = Rol.objects.get(
        desrol='Representante'
    )

    authe = User.objects.create_user(
            username="soyuncorreo"+str(0)+"@gmail.com",
            email="soyuncorreo"+str(0)+"@gmail.com",
            password="11111111"
        )

    profcoord= Profesor.objects.create(
        codigo=sede.codigosede+str(0),
        numprofesor = 0,
        idsede=sede,
        auth=authe,
        nombre="Profe0",
        apellido1="apellido1#0",
        apellido2="apellido2#0",
        oficina="II-"+str(0),
        fcreacion=timezone.now(),
        teloficina=83249329+0,
        telcelular=83249329+0,
    )
        
    equipo = Equipotrabajo.objects.create()
    profes = Profesor.objects.exclude(codigo=profcoord.codigo)
    equipo.docentes.add(profcoord,through_defaults={'rol':coord})
    for profe in profes:
        equipo.docentes.add(profe,through_defaults={'rol':guia})



def estudiantes():
    if(Estudiante.objects.count()>0):
        return
    # Codigo para añadir muchos estudiantes
    for i in range(20):
        sede = Sede.objects.all()[randint(0,3)]
        Estudiante.objects.create(
            carnet=2021046131+i,
            nombre="Est"+str(i),
            apellido1="apellido1#"+str(i),
            apellido2="apellido2#"+str(i),
            sede=sede,
            fcreacion=timezone.now(),
            telefono=83249329+i,
            correotec="soyuncorreo"+str(i)+"@gmail.com"
        )

def asistenteCuenta():
    if Asistenteadministrativo.objects.count() > 0:
        return
    authe = User.objects.create_user(
            username="asistente",
            email="kevin123@gmail.com",
            password="kevin123"
        )
    Asistenteadministrativo.objects.create(
        auth=authe,
        nombre= "Yo",
        apellido1 = "ap1",
        apellido2 = "ap1",
        sede = Sede.objects.get(codigosede="CA")
    )
    authe = User.objects.create_user(
            username="asistente2",
            email="kevin123@gmail.com",
            password="kevin123"
        )
    Asistenteadministrativo.objects.create(
        auth=authe,
        nombre= "Yo2",
        apellido1 = "ap12",
        apellido2 = "ap12",
        sede = Sede.objects.get(codigosede="SJ")
    )

def planTrabajo():
    if Plantrabajo.objects.count() > 0:
        return
    plan = Plantrabajo.objects.create(
            semestre = "2022 S1",
            semanainicial = datetime.strptime("2023-05-01",'%Y-%m-%d'),
            semanafinal = datetime.strptime("2023-08-21",'%Y-%m-%d')
        )
    Semanasvacaciones.objects.create(
        semanavacacional = datetime.strptime("2023-05-20",'%Y-%m-%d'),
        semestre = plan
    )

    plan = Plantrabajo.objects.create(
            semestre = "2022 S2",
            semanainicial = datetime.strptime("2023-05-01",'%Y-%m-%d'),
            semanafinal = datetime.strptime("2023-08-21",'%Y-%m-%d')
        )
    
    plan = Plantrabajo.objects.create(
            semestre = "2023 S1",
            semanainicial = datetime.strptime("2023-05-01",'%Y-%m-%d'),
            semanafinal = datetime.strptime("2023-08-21",'%Y-%m-%d')
        )

def tipoActividad():
    if Tipoactividad.objects.count() > 0:
        return
    Tipoactividad.objects.create(
        destipoactividad='orientadora'
    )

def estadoActividad():
    if Estadoactividad.objects.count() > 0:
        return
    Estadoactividad.objects.create(
        desestado='planeada'
    )
    Estadoactividad.objects.create(
        desestado='notificada'
    )
    Estadoactividad.objects.create(
        desestado='realizada'
    )
    Estadoactividad.objects.create(
        desestado='cancelada'
    )

def actividades():
    if Actividad.objects.count() > 0:
        return
    actividad =Actividad(
        semana=1,
        planTrabajo=Plantrabajo.objects.all()[:1][0],
        tipo=Tipoactividad.objects.get(destipoactividad='orientadora'),
        nombre="DOP - Procastinacion",
        fecha=datetime.strptime("2021-05-06 07:00:00",'%Y-%m-%d %H:%M:%S'),
        fechaPublicacion=datetime.strptime("2021-05-02 07:00:00",'%Y-%m-%d %H:%M:%S'),
        diasrecordatorios=1,
        esvirtual=False,
        enlace=None,
        estado=Estadoactividad.objects.get(desestado="planeada")
    )
    actividad.save()
    for responsable in Profesor.objects.all()[:3]:
        actividad.responsables.add(responsable)

    actividad =Actividad(
        semana=2,
        planTrabajo=Plantrabajo.objects.all()[:1][0],
        tipo=Tipoactividad.objects.get(destipoactividad='orientadora'),
        nombre="DOP - Gestion de tiempo",
        fecha=datetime.strptime("2021-05-06 07:00:00",'%Y-%m-%d %H:%M:%S'),
        fechaPublicacion=datetime.strptime("2021-05-02 07:00:00",'%Y-%m-%d %H:%M:%S'),
        diasrecordatorios=1,
        esvirtual=False,
        enlace=None,
        estado=Estadoactividad.objects.get(desestado="planeada")
    )
    actividad.save()
    for responsable in Profesor.objects.all()[:3]:
        actividad.responsables.add(responsable)

    actividad =Actividad(
        semana=2,
        planTrabajo=Plantrabajo.objects.all()[:1][0],
        tipo=Tipoactividad.objects.get(destipoactividad='orientadora'),
        nombre="DOP - Control de emociones",
        fecha=datetime.strptime("2021-05-06 07:00:00",'%Y-%m-%d %H:%M:%S'),
        fechaPublicacion=datetime.strptime("2021-05-02 07:00:00",'%Y-%m-%d %H:%M:%S'),
        diasrecordatorios=1,
        esvirtual=False,
        enlace=None,
        estado=Estadoactividad.objects.get(desestado="planeada")
    )
    actividad.save()
    for responsable in Profesor.objects.all()[:3]:
        actividad.responsables.add(responsable)

def comentarios():
    if Comentario.objects.count() > 0:
        return
    act1 = Actividad.objects.all()[0]
    act2 = Actividad.objects.all()[1]
    act3 = Actividad.objects.all()[2]
    profe1 = Profesor.objects.all()[randint(0,10)]
    profe2 = Profesor.objects.all()[randint(0,10)]

    Comentario(
        contenido="Actividad interesante prof1",
        fecha=datetime.strptime("2021-05-06 07:00:00",'%Y-%m-%d %H:%M:%S'),
        autor=profe1,
        actividad=act1
    ).save()

    Comentario(
        contenido="Actividad interesante prof2",
        fecha=datetime.strptime("2021-05-06 08:00:00",'%Y-%m-%d %H:%M:%S'),
        autor=profe2,
        actividad=act1
    ).save()

    Comentario(
        contenido="Interesante actividad prof1",
        fecha=datetime.strptime("2021-05-06 08:00:00",'%Y-%m-%d %H:%M:%S'),
        autor=profe1,
        actividad=act2
    ).save()

    Comentario(
        contenido="Interesante actividad prof2",
        fecha=datetime.strptime("2021-05-06 07:00:00",'%Y-%m-%d %H:%M:%S'),
        autor=profe2,
        actividad=act2
    ).save()

    Comentario(
        contenido="Simple comentario pa",
        fecha=datetime.strptime("2021-05-06 07:00:00",'%Y-%m-%d %H:%M:%S'),
        autor=profe2,
        actividad=act3
    ).save()

def llenarTodo():
    sede()
    rol()
    estudiantes()
    profesores()
    asistenteCuenta()
    equipoTrabajo()
    planTrabajo()
    tipoActividad()
    estadoActividad()
    actividades()
    comentarios()
    print("hecho")