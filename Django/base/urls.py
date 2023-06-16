from django.urls import path

from . import views

urlpatterns = [
    path("test/",views.Test.as_view()),
    path("equipoGuia/",views.EquipoGuia.as_view()),
    path("actividad/",views.ActividadTestSerializer.as_view()),
    path("tipo/",views.TipoActSerializer.as_view()),
    path("plan/",views.PlanTrabajoTest.as_view()),
    path("estudiante/",views.EstudianteTest.as_view()),
    path("pruebas/",views.pruebitasPa.as_view()),    
    path("llenarBase/",views.Llenado.as_view()),    
    
    path("ListaEstudiantes/",views.ListaEstudiantes.as_view()),
    path("DetalleEquipo/",views.DetalleEquipo.as_view()),
    path("DetalleProfes/",views.DetalleProfes.as_view()),
    path("ObtenerSedes/",views.ObtenerSedes.as_view()),
    path("ObtenerRoles/",views.ObtenerRoles.as_view()),
    path("ModificarEstudiante/",views.ModificarEstudiante.as_view()),
    path("CrearPlanTrabajo/",views.CrearPlanTrabajo.as_view()),
    path("PlanesTrabajoDisponibles/",views.PlanesTrabajoDisponibles.as_view()),
    path("PlanesTrabajoCompletos/",views.PlanesTrabajoCompleto.as_view()),
    path("AgregarActividad/",views.AgregarActividad.as_view()),
    path("ModificarActividad/",views.ModificarActividad.as_view()),
    path("BorrarActividad/",views.BorrarActividad.as_view()),
    path("ObtenerActividades/",views.ObtenerActividades.as_view()),
    path("ObtenerAActividades/",views.ObtenerAActividades.as_view()),
    path("ObtenerTipoAct/",views.ObtenerTipoAct.as_view()),
    path("RealizarActividad/",views.RealizarActividad.as_view()),
    path("CancelarActividad/",views.CancelarActividad.as_view()),
    path("PublicarActividad/",views.PublicarActividad.as_view()),
    path("ObtenerComentarios/",views.ObtenerComentarios.as_view()),
    path("EnviarComentarios/",views.EnviarComentarios.as_view()),
    path("GetProfileImage/",views.GetProfileImage.as_view()),
    
    path("CargarExcel/",views.CargarExcel.as_view()),
    path("asistente/equipoGuia/registrar/",views.AARegistrarNuevoIntegrante.as_view()),
    #--------------------------------------------------------------------------------------
    path("registrarProfesor/",views.AARegistrarProfesor.as_view()),
    path("registrarNuevoIntegrante/",views.AARegistrarNuevoIntegrante.as_view()),
    path("cambiarInfoProfesor/",views.AACambiarInfoMiembroEquipo.as_view()),
    path("definirCoordinador/",views.AADefinirCoordinador.as_view()),
    path("darDeBajaAProfesor/",views.AADarDeBajaAProfesor.as_view()),
    path("obtenerDetalleProfesor/",views.AAObtenerDetalleProfesor.as_view()),
    path("obtenerPlanTrabajo/",views.AAObtenerPlanTrabajo.as_view()),
    path("obtenerDetalleActividad/",views.AAObtenerDetalleActividad.as_view()),
]
