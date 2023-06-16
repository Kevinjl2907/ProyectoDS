from base.models import Profesor
from base.models import Rol 
from base.models import Equipotrabajo
from base.models import Actividad
from base.models import Tipoactividad
from base.models import Comentario
from base.serializers import ActividadSerializer
from django.utils import timezone

class ActividadTestSerializer():
    
    def returnActividad(self):
        rolcito = Rol.objects.create(desrol='Profesor Guia')
       
        profeCoord = Profesor.objects.create(
                nombre="ProfesorCoord",
                rol = rolcito,
                codigo = "CA00",
                correo = "uncorreo@undominio.com",
                teloficina = 23442340+0,
                telcelular = 87999000+0,
                fcreacion = timezone.now()
            )
        
        responsables = Equipotrabajo.objects.create(coordinador=profeCoord)
        for i in range(3):
            profe = Profesor.objects.create(
                nombre="Profesor" + str(i),
                rol = rolcito,
                codigo = "CA" + str(i),
                correo = "uncorreo@undominio.com",
                teloficina = 23442340+i,
                telcelular = 87999000+i,
                fcreacion = timezone.now()
            )
            responsables.docentes.add(profe)
        
        profelimon1 = Profesor.objects.create(
            nombre="Profesor" + str(1),
            rol = rolcito,
            codigo = "LI" + str(1),
            correo = "uncorreo@undominio.com",
            teloficina = 23442340+1,
            telcelular = 87999000+1,
            fcreacion = timezone.now()
        )

        profelimon2 = Profesor.objects.create(
            nombre="Profesor" + str(2),
            rol = rolcito,
            codigo = "LI" + str(2),
            correo = "uncorreo@undominio.com",
            teloficina = 23442340+2,
            telcelular = 87999000+2,
            fcreacion = timezone.now()
        )

        tipoAct = Tipoactividad.objects.create(destipoactividad='Orientadoras')
        actividad1 = Actividad.objects.create(
            semana=1,
            tipo = tipoAct,
            nombre='Como sobrevivir a la U',
            fecha=timezone.now(),
            diaaviso=timezone.now(),
            diasrecordatorios=1,
            esvirtual=0,
            estado=0
        )

        actividad1.responsables.add(profelimon1) 
        actividad1.responsables.add(profelimon2) 
        actividad1.save()

        actividadSerializer = ActividadSerializer(actividad1)
        return actividadSerializer.data


    def returnComentario(self):
        unTipoActividad = Tipoactividad.objects.create(destipoactividad="recreativa")

        unaActividad = Actividad.objects.create(semana=3,
                                                tipo=unTipoActividad,
                                                nombre="Actividadcita",
                                                fecha=timezone.now(),
                                                diaaviso=timezone.now(),
                                                diasrecordatorios=5,
                                                esvirtual=False,
                                                afiche="asdsad",
                                                estado=0
                                                )

        rolcito = Rol.objects.create(desrol='Profesor Guia')

        profe = Profesor.objects.create(
                nombre="ProfesorCoord",
                rol = rolcito,
                codigo = "CA00",
                correo = "uncorreo@undominio.com",
                teloficina = 23442340+0,
                telcelular = 87999000+0,
                fcreacion = timezone.now()
            )
        
        unComentario = Comentario.objects.create(
            contenido="hola buenos dias",
            fecha=timezone.now(),
            autor=profe,
            actividad=unaActividad
        )
        
        return ({"response" : "good"})