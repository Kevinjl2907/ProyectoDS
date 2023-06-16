from base.models import Profesor
from base.models import Rol 
from base.models import Equipotrabajo
from base.models import Actividad
from base.models import Tipoactividad
from base.models import Plantrabajo
from base.serializers import PlanTrabajoSerializer
from django.utils import timezone
import datetime

class PlanTrabajoTest():
    
    def returnPlan(self):
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

        actividad2 = Actividad.objects.create(
            semana=2,
            tipo = tipoAct,
            nombre='Como orgamizar el tiempo',
            fecha=timezone.now(),
            diaaviso=timezone.now(),
            diasrecordatorios=1,
            esvirtual=0,
            estado=0
        )

        actividad2.responsables.add(profelimon1) 
        actividad2.responsables.add(profelimon2) 
        actividad2.save()

        plan = Plantrabajo.objects.create(
            id=1,
            semanainicial=datetime.date(2023, 2, 4),
            semanafinal=datetime.date(2023, 6, 22),
        )

        plan.actividades.add(actividad1)
        plan.actividades.add(actividad2)
        plan.save()

        planSerializer = PlanTrabajoSerializer(plan)
        return planSerializer.data