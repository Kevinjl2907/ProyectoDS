from base.models import Tipoactividad
from base.serializers import TipoActividadSerializer

class TipoActSerializer:

    def returnTipo(self):
        tipoAct = Tipoactividad.objects.create(destipoactividad='Orientadora')
        serializer = TipoActividadSerializer(tipoAct)
        return serializer.data