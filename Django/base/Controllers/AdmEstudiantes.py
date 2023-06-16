from .SingletonDAO import SingletonDAO


class AdminEstudiante():


    
    def obtenerDetalleProfesor(self, request):
        return SingletonDAO.getInstance().obtenerDetalleProfesor(request)
    
    def obtenerPlanTrabajo(self, request):
        return SingletonDAO.getInstance().obtenerPlanTrabajo(request)
    
    def obtenerDetalleActividad(self, request):
        return SingletonDAO.getInstance().obtenerDetalleActividad(request)
    
 
    def modificarInfoEstudiante(self, request):
        return SingletonDAO.getInstance().modificarInfoEstudiante(request)

