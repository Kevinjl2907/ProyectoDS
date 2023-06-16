<script>
import config from '@/service/Config';
import { required } from '@vuelidate/validators';
import { useVuelidate } from '@vuelidate/core';
import { ref } from 'vue';
import {FilterMatchMode, FilterOperator} from "primevue/api";

// eslint-disable-next-line vue/no-export-in-script-setup
export default {
    name: 'Equipo Guia',
    setup() {
        return { v$: useVuelidate({ $autoDirty: true }) };
    },
    data() {
        return {
            // URL's
            url: 'https://main.d2anrgvy7s2j70.amplifyapp.com/CrearPlanTrabajo/',
            // Variables utilizadas por el CRUD
            fileAfiche: null,
            editMode: false,
            addMode: false,
            searchMode: true,
            EditarDialog: false,
            deleteDialog: false,
            selectedRecord: null,
            filters: {
                global: {value: null, matchMode: FilterMatchMode.CONTAINS},
                nombre: {value: null, matchMode: FilterMatchMode.CONTAINS},
            },
            // Variables utilizadas por la pantalla
            equipoGuia: null,
            semestres: null,
            semestre: null,
            minDate: ref(new Date()),
            maxDate: ref(new Date()),
            currentDate: ref(new Date()),
            planSemestre: null,
            planAgregar: null,
            planAgregarEnlace: null,
            // Variables para: Crear Plan de trabajo
            planTrabajo: {
                semestre: null,
                semanainicial: null,
                semanafinal: null,
                vacaciones: null
            },
            tipoActividad : null,
            // Variables para: Agregar Actividad
            actividad: {
                json: {
                    semana: 1,
                    planTrabajo: null,
                    tipo: null,
                    nombre: null,
                    fecha: null,
                    fechaPublicacion: null,
                    diasRecordatorios: null,
                    esvirtual: false,
                    responsables: null,
                },
                afiche: null
            },
            actividadMod: null, 
            modalidad: [
                {
                    id: 1,
                    nombre: 'Presencial'
                },
                {
                    id: 2,
                    nombre: 'Virtual'
                }
            ],
            semanas: null,

            // Variables para: Modificar actividad
            planesTrabajo: null,
            selectedPlan: null,
            selectedActividad: null,
            actividades: [],
            bodyActividad: {
                planTrabajo: null
            },
            bodyEliminarActividad: {
                idactividad: null
            },
            borrarActividad: false
        };
    },
    validations() {
        return {
            semestre: { required },
            semanainicial: { required },
            semanafinal: { required },
            vacaciones: { required }
        };
    },
    async mounted() {
        this.setMinDate();
        this.getPlanesTrabajo();
        this.getResponsables();
        this.createSemestre();
        this.initFilters();
        this.semestres = this.createSemestre();
        this.tipoActividad = await this.getTipoActividad();
    },
    methods: {
      clearFilter() {
        this.initFilters();
      },
      initFilters() {
        this.filters = {
          global: {value: null, matchMode: FilterMatchMode.CONTAINS},
          nombre: {operator: FilterOperator.AND, constraints: [{value: null, matchMode: FilterMatchMode.STARTS_WITH}]}
        };
      },
        opendDialog() {
            if (this.selectedActividad === null) {
                this.$swal.fire({
                    position: 'top-center',
                    icon: 'warning',
                    title: 'Warning',
                    text: 'Debe seleccionar una actividad primero.',
                    showConfirmButton: true
                });
            } else {
                console.log('actividad seleccionada', this.selectedActividad);
                
                this.actividadMod = Object.assign({},this.selectedActividad);
                this.actividadMod.diasRecordatorios = this.selectedActividad.diasrecordatorios;
                delete this.actividadMod.diasrecordatorios;
                this.actividadMod.responsables = Object.assign([],this.actividadMod.responsables);
                this.actividadMod.responsables.forEach(this.parseResponsables)
                this.actividadMod.fecha = this.getFecha(this.actividadMod.fecha);
                this.actividadMod.fechaPublicacion = this.getFecha(this.actividadMod.fechaPublicacion);
                this.updateMinMaxDateMod()
                this.EditarDialog = true
            }
        },
        parseResponsables(item,index,arr) {
            arr[index] = item.codigo
        },
        closeDialog() {
            this.EditarDialog = false;
            this.selectedActividad = null;
            this.buscarActividades();
        },
        async deleteItem() {
            console.log('actividad Seleccionada', this.selectedActividad);

            if (this.selectedActividad == null) {
                this.$swal.fire({
                    position: 'top-center',
                    icon: 'warning',
                    title: 'Error',
                    text: 'Debe seleccionar una linea primero',
                    showConfirmButton: true,
                    timer: config.globales.timer_errores
                });
            } else {
                this.borrarActividad = false;
                await this.$swal
                    .fire({
                        title: '¿Está seguro que desea eliminar est registro?',
                        text: '¡No podrá revertir esta acción!',
                        icon: 'warning',
                        showCancelButton: true,
                        confirmButtonColor: '#3085d6',
                        cancelButtonColor: '#d33',
                        confirmButtonText: 'Aceptar',
                        cancelButtonText: 'Cancelar'
                    })
                    .then((result) => {
                        if (result.isConfirmed) {
                            console.log('result', result);
                            this.borrarActividad = true;
                            this.bodyEliminarActividad.idactividad = this.selectedActividad.idactividad;
                        }
                    });
                if (this.borrarActividad) {
                    console.log(this.bodyEliminarActividad);
                    console.log(this.bodyActividad);
                    var request = {
                        method: 'POST',
                        headers: { Authorization: localStorage.token, 'Content-Type': 'application/json' },

                        body: JSON.stringify(this.bodyEliminarActividad) //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
                    };
                    var response = await fetch('https://main.d2anrgvy7s2j70.amplifyapp.com/BorrarActividad/', request);
                    var myJson = await response.json();
                    console.log(this.bodyActividad);
                    if (myJson.response === 'unsuccessful') {
                        console.log('no exito');
                    } else {
                        console.log('si se borro');
                        this.buscarActividades()
                    }
                }
            }
        },
        async api(url, objeto) {
            var request = {
                method: 'POST',
                headers: {
                    'content-Type': 'application/json',
                    Authorization: localStorage.token
                }, //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
                body: JSON.stringify(objeto)
            };

            var response = await fetch(url, request);
            response = await response.json();
            console.log('response', response);
            if (response.response === 'unsuccessful') {
                this.$swal.fire({
                    position: 'top-center',
                    icon: 'error',
                    title: 'Error',
                    text: 'Algo salio mal',
                    showConfirmButton: true
                });
                return false;
            } else if (response.response === 'weeksError') {
                this.$swal.fire({
                    position: 'top-center',
                    icon: 'error',
                    title: 'Error',
                    text: 'No hay suficientes semanas entre inicio y fin (recuerde las vacaciones no cuentan en las 16 semanas lectivas)',
                    showConfirmButton: true
                });
            } else if (response.response === 'datesError') {
                this.$swal.fire({
                    position: 'top-center',
                    icon: 'error',
                    title: 'Error',
                    text: 'Debe existir minimo un dia de diferencia entre fecha de realizacion y publicacion',
                    showConfirmButton: true
                });
            } else if (response.response === 'reminderError') {
                this.$swal.fire({
                    position: 'top-center',
                    icon: 'error',
                    title: 'Error',
                    text: 'Dias de Recordatorio no puede ser mayor a la diferencia entre la fecha en que se realiza y la fecha de publicación',
                    showConfirmButton: true
                });
            } else if (response.response === 'successful') {
                return true
            } else {
                this.$swal.fire({
                    position: 'top-center',
                    icon: 'error',
                    title: 'Error',
                    text: 'No se pudo crear el plan',
                    showConfirmButton: true
                });
                return false;
            }
        },
        async getResponsables() {
            var request = {
                method: 'GET',
                headers: { Authorization: localStorage.token } //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
            };
            var response = await fetch('https://main.d2anrgvy7s2j70.amplifyapp.com/DetalleEquipo/', request);
            //.then(response => response.json())
            //.then(data => token=data)
            //.catch(error => console.error(error));
            var myJson = await response.json();
            if (myJson.response === 'unsuccessful') {
                console.log('no exito');
            } else {
              this.equipoGuia = myJson.equipoTrabajo;
              console.log(this.equipoGuia)
            }
        },
        createSemestre() {
            var crearSemestres = [];
            var annioActual = new Date().getFullYear();
            for(let i = 0; i < 3; i++) {
                crearSemestres.push({
                    nombre : annioActual + " S1"
                });
                crearSemestres.push({
                    nombre : annioActual + " S2"
                });
                annioActual++;
            }
            return crearSemestres;
        },
        async crearPlanTrabajo() {
            if (this.validacionPlanTrabajo()) {
                this.planTrabajo.semestre = this.planSemestre.nombre;
                var response = await this.api(this.url, this.planTrabajo);

                if (response) {
                    this.$swal.fire({
                        position: 'top-center',
                        icon: 'success',
                        title: 'Enhorabuena',
                        text: 'Se ha creado el nuevo plan de trabajo con éxito.',
                        showConfirmButton: true
                    });
                }
            }
        },
        validacionPlanTrabajo() {
            if (this.planTrabajo.semanainicial !== null && this.planTrabajo.semanafinal !== null && this.planTrabajo.vacaciones !== null && this.planSemestre !== null) {
                return true;
            } else {
                this.$swal.fire({
                    position: 'top-center',
                    icon: 'warning',
                    title: 'Error',
                    text: 'Datos Incompletos',
                    showConfirmButton: true,
                    timer: config.globales.timer_errores
                });
                return false;
            }
        },
        async validacionActividad() {
            Date.prototype.toJSON = function(){
                const fechaTemp = new Date(this)
                const hoursDiff = fechaTemp.getHours() - fechaTemp.getTimezoneOffset() / 60;
                fechaTemp.setHours(hoursDiff);
                return fechaTemp.toISOString();
            };
            if(this.fileAfiche===null) {
                this.$swal.fire({
                    position: 'top-center',
                    icon: 'error',
                    title: 'Error',
                    text: 'Falta Subir el afiche',
                    showConfirmButton: true
                });
                return
            } else if (this.planAgregar===null) {
                this.$swal.fire({
                    position: 'top-center',
                    icon: 'error',
                    title: 'Error',
                    text: 'Seleccione plan',
                    showConfirmButton: true
                });
                return
            }

            if(this.planAgregarEnlace !== null && this.planAgregarEnlace !== "") {
                this.actividad.json.enlace = this.planAgregarEnlace;
            } else{
                delete this.actividad.json.enlace;
            }
            this.actividad.json.planTrabajo = this.planAgregar.semestre
            this.fileAfiche.append('json', JSON.stringify(this.actividad.json));
            
            var request = {
                method: 'POST',
                headers: { Authorization: localStorage.token }, //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
                body: this.fileAfiche
            };
            console.log(this.fileAfiche);
            var response = await fetch('https://main.d2anrgvy7s2j70.amplifyapp.com/AgregarActividad/', request);
            response = await response.json();
            console.log(response);

            if (response.response === 'unsuccessful') {
                this.$swal.fire({
                    position: 'top-center',
                    icon: 'error',
                    title: 'Error',
                    text: 'No se pudo guardar la informacion de la actividad, por favor revise sus datos.',
                    showConfirmButton: true
                });
            } else if (response.response === 'enlaceError') {
                this.$swal.fire({
                    position: 'top-center',
                    icon: 'error',
                    title: 'Error',
                    text: 'Coloque un enlace si va ser virtual.',
                    showConfirmButton: true
                });
            } else if (response.response === 'datesError') {
                this.$swal.fire({
                    position: 'top-center',
                    icon: 'error',
                    title: 'Error',
                    text: 'Debe existir minimo un dia de diferencia entre fecha de realizacion y publicacion',
                    showConfirmButton: true
                });
            } else if (response.response === 'reminderError') {
                this.$swal.fire({
                    position: 'top-center',
                    icon: 'error',
                    title: 'Error',
                    text: 'Dias de Recordatorio no puede ser mayor a la diferencia entre la fecha en que se realiza y la fecha de publicación',
                    showConfirmButton: true
                });
            } else if (response.response === 'successful') {
                this.$swal.fire({
                    position: 'top-center',
                    icon: 'success',
                    title: 'Enhorabuena',
                    text: 'Se pudo guardar la informacion de la actividad.',
                    showConfirmButton: true
                });
            }
        },
        updateMinMaxDate() {
            console.log(this.planAgregar)
            if(this.planAgregar===null) {
                return;
            }
            this.currentDate = ref(new Date());
            var fechaInicial = new Date(this.planAgregar.semanas[this.actividad.json.semana-1]);
            this.minDate = ref(new Date(fechaInicial));
            fechaInicial.setDate(fechaInicial.getDate()+6)
            this.maxDate = ref(new Date(fechaInicial));
        },
        updateMinMaxDateMod() {
            console.log(this.actividadMod.planTrabajo)
            if(this.actividadMod.planTrabajo===null) {
                return;
            }
            var currentPlan = null;
            for (var plan of this.planesTrabajo) {
                if (plan.semestre === this.actividadMod.planTrabajo) {
                    currentPlan = plan
                }
            }
            this.currentDate = ref(new Date());
            var fechaInicial = new Date(currentPlan.semanas[this.actividadMod.semana-1]);
            this.minDate = ref(new Date(fechaInicial));
            fechaInicial.setDate(fechaInicial.getDate()+6)
            this.maxDate = ref(new Date(fechaInicial));
            console.log(this.minDate)
            console.log(this.maxDate)
        },
        async getPlanesTrabajo() {
            var request = {
                method: 'GET',
                headers: { Authorization: localStorage.token } //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
            };
            var response = await fetch('https://main.d2anrgvy7s2j70.amplifyapp.com/PlanesTrabajoDisponibles/', request);
            var myJson = await response.json();
            if (myJson.response === 'unsuccessful') {
                console.log('no exito');
            } else {
                console.log(myJson);
                this.planesTrabajo = myJson.planes;
            }
        },
        async getTipoActividad() {
            var request = {
                method: 'GET',
                headers: { Authorization: localStorage.token } //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
            };
            var response = await fetch('https://main.d2anrgvy7s2j70.amplifyapp.com/ObtenerTipoAct/', request);
            var myJson = await response.json();
            return myJson.tipos
        },
        convertirFecha(fecha) {
            // Crear un objeto de fecha con la cadena proporcionada
            var fechaObjeto = new Date(fecha);

            // Obtener los componentes de fecha necesarios
            var anio = fechaObjeto.getFullYear();
            var mes = (fechaObjeto.getMonth() + 1).toString().padStart(2, '0');
            var dia = fechaObjeto.getDate().toString().padStart(2, '0');

            // Construir la fecha en el formato deseado (YYYY-MM-DD)
            var fechaConvertida = anio + '-' + mes + '-' + dia;

            return fechaConvertida;
        },
        async asignFile(event) {
            this.fileAfiche = new FormData();
            this.fileAfiche.append('afiche', event.files[0]);
        },
        setMinDate() {
            let today = new Date();
            let month = today.getMonth();
            let year = today.getFullYear();
            let prevMonth = month === 0 ? 11 : month - 1;
            let prevYear = prevMonth === 11 ? year - 1 : year;

            const minDate = ref(new Date());
            minDate.value.setFullYear(prevYear);

            this.minDate = minDate;
        },
        async buscarActividades() {
            //this.bodyActividad.planTrabajo = ;
            var request = {
                method: 'POST',
                headers: { Authorization: localStorage.token, 'Content-Type': 'application/json' },

                body: JSON.stringify({planTrabajo : this.bodyActividad.planTrabajo.semestre}) //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
            };
            var response = await fetch('https://main.d2anrgvy7s2j70.amplifyapp.com/ObtenerActividades/', request);
            var myJson = await response.json();
            console.log(this.bodyActividad);
            if (myJson.response === 'unsuccessful') {
                console.log('no exito');
            } else {
                console.log(myJson);
                this.actividades = myJson.actividades;
            }
        },
        async parseSelected() {
             
            if (this.actividadMod.planTrabajo===null) {
                this.closeDialog()
                this.$swal.fire({
                    position: 'top-center',
                    icon: 'error',
                    title: 'Error',
                    text: 'Seleccione plan',
                    showConfirmButton: true
                });
                return
            }
            
            if(this.fileAfiche===null) {
                this.fileAfiche = new FormData();
            } 

            if(this.actividadMod.enlace === null || this.actividadMod.enlace === "") {
                delete this.actividadMod.enlace;
            } 
            this.fileAfiche.append('json', JSON.stringify(this.actividadMod));
            
            var request = {
                method: 'POST',
                headers: { Authorization: localStorage.token }, //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
                body: this.fileAfiche
            };
            console.log(this.fileAfiche);
            var response = await fetch('https://main.d2anrgvy7s2j70.amplifyapp.com/ModificarActividad/', request);
            response = await response.json();
            console.log(response);

            if (response.response === 'unsuccessful') {
                this.closeDialog()
                this.$swal.fire({
                    position: 'top-center',
                    icon: 'error',
                    title: 'Error',
                    text: 'No se pudo guardar la informacion de la actividad, por favor revise sus datos.',
                    showConfirmButton: true
                });
            } else if (response.response === 'enlaceError') {
                this.closeDialog()
                this.$swal.fire({
                    position: 'top-center',
                    icon: 'error',
                    title: 'Error',
                    text: 'Coloque un enlace si va ser virtual.',
                    showConfirmButton: true
                });
            } else if (response.response === 'datesError') {
                this.closeDialog()
                this.$swal.fire({
                    position: 'top-center',
                    icon: 'error',
                    title: 'Error',
                    text: 'Debe existir minimo un dia de diferencia entre fecha de realizacion y publicacion',
                    showConfirmButton: true
                });
            } else if (response.response === 'reminderError') {
                this.closeDialog()
                this.$swal.fire({
                    position: 'top-center',
                    icon: 'error',
                    title: 'Error',
                    text: 'Dias de Recordatorio no puede ser mayor a la diferencia entre la fecha en que se realiza y la fecha de publicación',
                    showConfirmButton: true
                });
            } else if (response.response === 'successful') {
                this.closeDialog()
                this.$swal.fire({
                    position: 'top-center',
                    icon: 'success',
                    title: 'Enhorabuena',
                    text: 'Se pudo guardar la informacion de la actividad.',
                    showConfirmButton: true
                });
            }
        },
        getFullName(profe) {
            return profe.codigo + " " + profe.nombre + " " + profe.apellido1 + " " + profe.apellido2
        },
        getFecha(fecha) {
            return new Date(fecha)
        }
        ,
        changeprueba() {
            console.log(this.actividad.json.responsables)
        }
    }
};
</script>

<template>
    <TabView class="tabview-custom">
        <!--    CREAR PLAN DE TRABAJO-->
        <TabPanel>
            <template #header>
                <i class="pi pi-plus mr-2"></i>
                <span>Crear Plan de Trabajo</span>
            </template>

            <div class="surface-card p-4 shadow-2 border-round">
                <div class="grid formgrid p-fluid">
                    <div class="field mb-4 col-12 md:col-6">
                        <label class="font-medium">Semestre del Plan</label>
                        <Dropdown v-model="this.planSemestre" :options="this.semestres" optionLabel="nombre" placeholder="Seleccione el semestre del plan">
                            <template #option="slotProps">
                                <div class="flex align-items-center">
                                    <div>{{ slotProps.option.nombre }}</div>
                                </div>
                            </template>
                        </Dropdown>
                    </div>

                    <div class="field mb-4 col-12 md:col-6">
                        <label class="font-medium">Fecha Inicial</label>
                        <Calendar v-model="this.planTrabajo.semanainicial" showIcon placeholder="Ingrese la fecha inicial" dateFormat="yy-mm-dd" :disabledDays=[0,2,3,4,5,6] />
                    </div>

                    <div class="field mb-4 col-12 md:col-6">
                        <label class="font-medium">Fecha Final</label>
                        <Calendar v-model="this.planTrabajo.semanafinal" showIcon placeholder="Ingrese la fecha final" dateFormat="yy-mm-dd" :disabledDays=[0,2,3,4,5,6] />
                    </div>

                    <div class="field mb-4 col-12 md:col-6">
                        <label class="font-medium">Periodo de Vacaciones</label>
                        <Calendar v-model="this.planTrabajo.vacaciones" selectionMode="multiple" showIcon placeholder="Ingrese el periodo de vacaciones" dateFormat="yy-mm-dd" :disabledDays=[0,2,3,4,5,6] />
                    </div>

                    <div class="surface-100 mb-3 col-12" style="height: 2px"></div>

                    <div class="col-12">
                        <Button label="Crear Plan" class="w-auto mt-3" @click="this.crearPlanTrabajo()"></Button>
                    </div>
                </div>
            </div>
        </TabPanel>

        <!--    AGREGAR ACTIVIDAD-->
        <TabPanel>
            <template #header>
                <i class="pi pi-calendar-plus mr-2"></i>
                <span>Agregar Actividad</span>
            </template>
            <div class="surface-card p-4 shadow-2 border-round">
                <div class="grid formgrid p-fluid">
                    <!--          NOMBRE DE LA ACTIVIDAD-->
                    <div class="field mb-4 col-12">
                        <label for="nickname" class="font-medium">Nombre de la Actividad</label>
                        <InputText v-model="this.actividad.json.nombre" id="nombreActividad" type="text" />
                    </div>

                    <!--          LINEA DE SEPARACION-->
                    <div class="surface-100 mb-3 col-12" style="height: 2px"></div>

                    <div class="field mb-4 col-12 md:col-6">
                        <label class="font-medium">Semestre del Plan</label>
                        <Dropdown v-model="this.planAgregar" @change="this.updateMinMaxDate()" :options="this.planesTrabajo" optionLabel="semestre" :showClear="true" placeholder="Seleccione el semestre">
                            <template #option="slotProps">
                                <div>{{ slotProps.option.semestre }}</div>
                            </template>
                        </Dropdown>
                    </div>

                    <div class="field mb-4 col-12 md:col-1">
                        <label for="bio" class="font-medium">Virtual</label>
                        <InputSwitch v-model="this.actividad.json.esvirtual" />
                    </div>

                    <div class="field mb-4 col-12 md:col-6">
                        <label for="bio" class="font-medium">Semana a Planear</label>
                        <InputNumber v-model="this.actividad.json.semana" showButtons mode="decimal" @update:modelValue="this.updateMinMaxDate()" placeholder="Seleccione el numero de semana" :min="1" :max="16" :maxlength="2"></InputNumber>
                    </div>
                    <div class="field mb-4 col-12 md:col-6">
                        <label for="bio" class="font-medium">Dias de Recordatorio</label>
                        <InputNumber v-model="this.actividad.json.diasRecordatorios" showButtons mode="decimal" placeholder="Seleccione el numero de semana" :min="1" :max="16" :maxlength="2"></InputNumber>
                    </div>

                    <div class="field mb-4 col-12 md:col-6">
                        <label for="avatar" class="font-medium">Responsables</label>
                        <MultiSelect v-model="this.actividad.json.responsables" @change="this.changeprueba()" v-model:options="this.equipoGuia" :optionLabel="this.getFullName" optionValue="codigo" placeholder="Seleccione los responsables" class="w-full" />
                    </div>

                    <div class="field mb-4 col-12 md:col-6">
                        <label for="bio" class="font-medium">Tipo de Actividad</label>
                        <Dropdown v-model="this.actividad.json.tipo" :options="this.tipoActividad" optionLabel="destipoactividad" optionValue="destipoactividad" :filter="true" filterBy="destipoactividad" :showClear="true" placeholder="Seleccione el tipo de actividad">
                            <template #option="slotProps">
                                <div class="flex align-items-center">
                                    <div>{{ slotProps.option.destipoactividad }}</div>
                                </div>
                            </template>
                        </Dropdown>
                    </div>

                    <div class="field mb-4 col-12 md:col-6">
                        <label for="avatar" class="font-medium">Afiche</label>
                        <div class="flex align-items-center">
                            <i class="pi  pi-file-import mr-4" style="font-size: 3rem"></i>
                            <FileUpload mode="basic" name="afiche" :auto="true" url="./upload.php" accept="image/*" :maxFileSize="1000000" class="p-button-outlined p-button-plain" chooseLabel="Subir Afiche" customUpload @uploader="asignFile" />
                        </div>
                    </div>

                    <div class="field mb-4 col-12 md:col-6">
                        <label for="city" class="font-medium">Fecha de Publicación</label>
                        <Calendar :showIcon="true" :showButtonBar="true" v-model="this.actividad.json.fechaPublicacion" placeholder="Indique la fecha de publicación" showTime hourFormat="24" :minDate="this.currentDate" :maxDate="this.maxDate" />
                    </div>

                    <div class="field mb-4 col-12 md:col-6">
                        <label for="state" class="font-medium">Fecha de Realización</label>
                        <Calendar :showIcon="true" :showButtonBar="true" v-model="this.actividad.json.fecha" placeholder="Indique la fecha de realización" showTime hourFormat="24" :minDate="this.minDate" :maxDate="this.maxDate" />
                        <!--            <InputText id="state" type="text" />-->
                    </div>
                    <div class="surface-100 mb-3 col-12" style="height: 2px"></div>
                    <div class="field mb-4 col-12">
                        <label for="website" class="font-medium">Link de Reunión</label>
                        <div class="p-inputgroup">
                            <span class="p-inputgroup-addon">www</span>
                            <InputText v-model="this.planAgregarEnlace" id="linkReunion" type="text" placeholder="Ingrese el link de la reunión" />
                        </div>
                    </div>

                    <div class="surface-100 mb-3 col-12" style="height: 2px"></div>

                    <div class="col-12">
                        <Button label="Agregar Actividad" class="w-auto mt-3" @click="validacionActividad()" />
                    </div>
                </div>
            </div>
        </TabPanel>

        <!--MODIFICAR ACTIVIDAD-->
        <TabPanel>
            <template #header>
                <i class="pi pi-pencil mr-2"></i>
                <span>Modificar Actividad</span>
            </template>
            <div class="field mb-4 col-12 md:col-6">
                <label class="font-medium w-full">Semestre del Plan</label>
                <Dropdown v-model="this.bodyActividad.planTrabajo" :options="this.planesTrabajo" @change="this.buscarActividades()" optionLabel="semestre" :showClear="true" placeholder="Plan de trabajo" class="w-full">
                    <template #option="slotProps">
                        <div class="flex align-items-center">
                            <div>{{ slotProps.option.semestre }}</div>
                        </div>
                    </template>
                </Dropdown>
            </div>
            <div class="card">
                <DataTable
                    :value="this.actividades"
                    :paginator="true"
                    class="p-datatable-gridlines"
                    :rows="10"
                    dataKey="idactividad"
                    :rowHover="true"
                    v-model:filters="filters"
                    filterDisplay="menu"
                    :filters="filters"
                    responsiveLayout="scroll"
                    :globalFilterFields="['nombre']"
                    v-model:selection="selectedActividad"
                    :sorteable="true"
                    :resizableColumns="true"
                    :autoLayout="true"
                    selectionMode="single"
                    :scrollable="true"
                    scrollHeight="flex"
                >
                    <template #header>
                        <div class="mb-3 flex align-items-center justify-content-between">
                            <span class="text-xl font-normal text-900">Actividades Diponibles</span>
                            <div class="overflow-y-auto">
                                <Button type="button" icon="pi pi-filter-slash" label="Clear" class="p-button-outlined mr-2 mb-2" @click="initFilters()" />
                                <Button label="Modificar Actividad" class="p-button-outlined mr-2 mb-2" @click="this.opendDialog()" />
                                <span class="p-input-icon-left mb-2">
                                    <i class="pi pi-search" />
                                    <InputText v-model="filters['global'].value" placeholder="Buscar..." style="width: 100%" />
                                </span>
                            </div>
                        </div>
                    </template>
                    <template #empty> No hay información disponible </template>
                    <template #loading> Cargando, por favor espere. </template>
                    <Column field="nombre" header="Nombre" :sortable="true" style="min-width: 12rem">
                        <template #body="slotProps">
                            {{ slotProps.data.nombre }}
                        </template>
                    </Column>
                </DataTable>
            </div>
        </TabPanel>

        <!-- ELIMINAR ACTIVIDAD-->
        <TabPanel>
            <template #header>
                <i class="pi pi-pencil mr-2"></i>
                <span>Eliminar Actividad</span>
            </template>
            <div class="field mb-4 col-12 md:col-6">
                <label class="font-medium w-full">Semestre del Plan</label>
                <Dropdown v-model="this.bodyActividad.planTrabajo" :options="this.planesTrabajo" @change="this.buscarActividades()" optionLabel="semestre" :showClear="true" placeholder="Plan de trabajo" class="w-full">
                    <template #option="slotProps">
                        <div class="flex align-items-center">
                            <div>{{ slotProps.option.semestre }}</div>
                        </div>
                    </template>
                </Dropdown>
            </div>
            <div class="card">
                <DataTable
                    :value="this.actividades"
                    :paginator="true"
                    class="p-datatable-gridlines"
                    :rows="10"
                    dataKey="idactividad"
                    :rowHover="true"
                    v-model:filters="filters"
                    filterDisplay="menu"
                    :filters="filters"
                    responsiveLayout="scroll"
                    :globalFilterFields="['nombre']"
                    v-model:selection="selectedActividad"
                    :sorteable="true"
                    :resizableColumns="true"
                    :autoLayout="true"
                    selectionMode="single"
                    :scrollable="true"
                    scrollHeight="flex"
                >
                    <template #header>
                        <div class="mb-3 flex align-items-center justify-content-between">
                            <span class="text-xl font-normal text-900">Actividades Diponibles</span>
                            <div class="overflow-y-auto">
                                <Button type="button" icon="pi pi-filter-slash" label="Clear" class="p-button-outlined mr-2 mb-2" @click="initFilters()" />
                                <Button label="Eliminar Actividad" class="p-button-outlined mr-2 mb-2" @click="this.deleteItem()" />
                                <span class="p-input-icon-left mb-2">
                                    <i class="pi pi-search" />
                                                                    <InputText v-model="filters['global'].value" placeholder="Buscar..." style="width: 100%" />
                                </span>
                            </div>
                        </div>
                    </template>
                    <template #empty> No hay información disponible </template>
                    <template #loading> Cargando, por favor espere. </template>
                    <Column field="nombre" header="Nombre" :sortable="true" style="min-width: 12rem">
                        <template #body="slotProps">
                            {{ slotProps.data.nombre }}
                        </template>
                    </Column>
                </DataTable>
            </div>
        </TabPanel>
    </TabView>
    <Dialog v-model:visible="EditarDialog" :modal="true" :maximizable="true" appendTo="self" :style="{ width: '52vw' }" :breakpoints="{ '960px': '75vw', '640px': '100vw' }">
        <div class="grid formgrid p-fluid">
            <div class="surface-card p-4 shadow-2 border-round">
                <div class="grid formgrid p-fluid">
                    <!--          NOMBRE DE LA ACTIVIDAD-->
                    <div class="field mb-4 col-12">
                        <label for="nickname" class="font-medium">Nombre de la Actividad</label>
                        <InputText v-model="this.actividadMod.nombre" type="text" />
                    </div>

                    <!--          LINEA DE SEPARACION-->
                    <div class="surface-100 mb-3 col-12" style="height: 2px"></div>

                    <div class="field mb-4 col-12 md:col-6">
                        <label class="font-medium">Semestre del Plan</label>
                        <Dropdown v-model="this.actividadMod.planTrabajo" @change="updateMinMaxDateMod()" :options="this.planesTrabajo" optionValue="semestre" optionLabel="semestre" :showClear="true" placeholder="Seleccione el semestre">
                            <template #option="slotProps">
                                <div>{{ slotProps.option.semestre }}</div>
                            </template>
                        </Dropdown>
                    </div>

                    <div class="field mb-4 col-12 md:col-6">
                        <label for="bio" class="font-medium">Modalidad</label>
                        <InputSwitch v-model="this.actividadMod.esvirtual" class="ml-5" />
                    </div>

                    <div class="field mb-4 col-12 md:col-6">
                        <label for="bio" class="font-medium">Semana a Planear</label>
                        <InputNumber v-model="this.actividadMod.semana" @update:modelValue="this.updateMinMaxDateMod()" showButtons mode="decimal" placeholder="Seleccione el numero de semana" :min="1" :max="16" :maxlength="2"></InputNumber>
                    </div>
                    <div class="field mb-4 col-12 md:col-6">
                        <label for="bio" class="font-medium">Dias de Recordatorio</label>
                        <InputNumber v-model="this.actividadMod.diasRecordatorios" showButtons mode="decimal" placeholder="Seleccione el numero de semana" :min="1" :max="16" :maxlength="2"></InputNumber>
                    </div>

                    <div class="field mb-4 col-12 md:col-6">
                        <label for="avatar" class="font-medium">Responsables</label>
                        <MultiSelect v-model="this.actividadMod.responsables" :options="this.equipoGuia" :optionLabel="this.getFullName" optionValue="codigo" placeholder="Seleccione los responsables" class="w-full" />
                    </div>

                    <div class="field mb-4 col-12 md:col-6">
                        <label for="bio" class="font-medium">Tipo de Actividad</label>
                        <Dropdown v-model="this.actividadMod.tipo" :options="this.tipoActividad" optionValue="destipoactividad" optionLabel="destipoactividad" :filter="true" filterBy="destipoactividad" placeholder="Seleccione el tipo de actividad">
                            <template #option="slotProps">
                                <div class="flex align-items-center">
                                    <div>{{ slotProps.option.destipoactividad }}</div>
                                </div>
                            </template>
                        </Dropdown>
                    </div>

                    <div class="field mb-4 col-12 md:col-6">
                        <label for="avatar" class="font-medium">Afiche</label>
                        <div class="flex align-items-center">
                            <i class="pi  pi-file-import mr-4" style="font-size: 3rem"></i>
                            <FileUpload mode="basic" name="afiche" :auto="true" url="./upload.php" accept="image/*" :maxFileSize="1000000" class="p-button-outlined p-button-plain" chooseLabel="Subir Afiche" customUpload @uploader="asignFile" />
                        </div>
                    </div>

                    <div class="field mb-4 col-12 md:col-6">
                        <label for="city" class="font-medium">Fecha de Publicación</label>
                        <Calendar :showIcon="true" :showButtonBar="true" v-model="this.actividadMod.fechaPublicacion" placeholder="Indique la fecha de publicación" showTime hourFormat="24" v-model:minDate="this.currentDate" v-model:maxDate="this.maxDate" />
                    </div>

                    <div class="field mb-4 col-12 md:col-6">
                        <label for="state" class="font-medium">Fecha de Realización</label>
                        <Calendar :showIcon="true" :showButtonBar="true" v-model="this.actividadMod.fecha" placeholder="Indique la fecha de realización" showTime hourFormat="24" v-model:minDate="this.minDate" v-model:maxDate="this.maxDate" />
                        <!--            <InputText id="state" type="text" />-->
                    </div>
                    <div class="surface-100 mb-3 col-12" style="height: 2px"></div>
                    <div class="field mb-4 col-12">
                        <label for="website" class="font-medium">Link de Reunión</label>
                        <div class="p-inputgroup">
                            <span class="p-inputgroup-addon">www</span>
                            <InputText v-model="this.actividadMod.enlace" id="linkReunion" type="text" placeholder="Ingrese el link de la reunión" />
                        </div>
                    </div>

                    <div class="surface-100 mb-3 col-12" style="height: 2px"></div>

                    <div class="col-12">
                        <Button label="Modificar actividad" class="w-auto mt-3" @click="parseSelected()" />
                    </div>
                </div>
            </div>
        </div>
    </Dialog>
</template>

<style scoped lang="scss">
::v-deep(.p-datatable-frozen-tbody) {
    font-weight: bold;
}

::v-deep(.p-datatable-scrollable .p-frozen-column) {
    font-weight: bold;
}

.format {
    width: 100vw;
    height: 100vh;
}
</style>
