from .SingletonDAO import SingletonDAO

class AdminProfesores():

    # ---------------------------- Profe Guia ----------------------------
    def listaEstudiantes(self):
        return SingletonDAO.getInstance().listaEstudiantes()
    
    def obtenerDetalleEquipo(self):
        return SingletonDAO.getInstance().obtenerDetalleEquipo()

    def obtenerDetalleProfes(self):
        return SingletonDAO.getInstance().obtenerDetalleProfes()

    def modificarInfoEstudiante(self, request):
        return SingletonDAO.getInstance().modificarInfoEstudiante(request)
    
    # ---------------------------- Profe Coord ----------------------------