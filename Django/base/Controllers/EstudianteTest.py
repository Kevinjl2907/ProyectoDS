from base.models import Estudiante
from base.models import Sede
from base.serializers import EstudianteSerializer
from django.utils import timezone

"""
id = serializers.IntegerField()
nombre = serializers.CharField(max_length=45)
nombreadicional = serializers.CharField(max_length=45) 
apellido1 = serializers.CharField(max_length=45)
apellido2 = serializers.CharField(max_length=45)
sede = SedeSerializer()
correotec = serializers.EmailField(max_length=50)  
fedicion = serializers.DateTimeField()
editor = serializers.CharField(max_length=120)
fcreacion = serializers.DateTimeField()
"""

class EstudianteTest():
    
    def returnEstudiante(self):

        lasede = Sede.objects.create(codigosede='CA')

        estudiante = Estudiante.objects.create(
            id=202312023,
            nombre='Carlos',
            nombreadicional='Manuel',
            apellido1='Li',
            apellido2='Hernandez',
            correotec='@estudiantec.cr',
            sede=lasede,
            fcreacion=timezone.now()
        )

        estudianteSerializer = EstudianteSerializer(estudiante)
        return estudianteSerializer.data
       
      