<script>
import { FilterMatchMode, FilterOperator } from 'primevue/api';
import config from "@/service/Config";
// eslint-disable-next-line vue/no-export-in-script-setup
export default {
    name: 'Equipo Guia',
    data() {
        return {
            // URL's
            url: 'comunes/monedas/',
            // Variables utilizadas por el CRUD
            editMode: false,
            addMode: false,
            searchMode: true,
            EditarDialog: false,
            regProfDiaglog: false,
            deleteDialog: false,
            selectedRecord: null,
            allSedes: null,
            allRoles: null,
            rolIngreso: null,
            selectedIngreso: null,
            agregarProfeInfo: {
                codigosede: null,
                nombre: null,
                apellido1: null,
                apellido2: null,
                teloficina: null,
                telcelular:null,
                oficina:null,
                correo:null
            },
            editarProfeInfo: {
                codigo:null,
                nombre: null,
                apellido1: null,
                apellido2: null,
                teloficina: null,
                telcelular:null,
                oficina:null,
                correo:null,
                idasistente: localStorage.codigo
            },
            profeFoto: null,
            isMyInfo: null,
          myCode: localStorage.codigo,
            // Variables utilizadas por la pantalla
            equipoGuia: null,
            profesDisabled: null,
            isAssist: localStorage.type === 'asist' ? true : false, //true,
            editIsEnable: false,
            detailInfo: false,
            addProfe2Team: false,
            profeSeleccionado: null,
            filters: {
              global: {value: null, matchMode: FilterMatchMode.CONTAINS},
              nombre: {value: null, matchMode: FilterMatchMode.CONTAINS},
              sede: {value: null, matchMode: FilterMatchMode.CONTAINS},
              rol: {value: null, matchMode: FilterMatchMode.CONTAINS},
            },
        };
    },
    created() {
        this.editIsEnable = this.isAssist
        this.getSedes()
        this.getRoles()
        this.getTableContents();
        this.getProfesDisabled();
    },
    async mounted() {
        this.clearFilter();
        this.initFilters();
    },
  watch(){
      this.selectedRecord = function () {
        console.log(this.selectedRecord())
        return this.isMyInfo = localStorage.codigo === this.selectedRecord.codigo ? true : false;
    }
  },
    methods: {
        clearFilter() {
            this.initFilters();
          console.log(this.selectedRecord);
        },
        enableEditButton() {
            if(this.isAssist) {
                return
            }
            this.editIsEnable = (localStorage.codigo === this.selectedRecord.codigo ? true : false)
        },
        initFilters() {
            this.filters = {
                global: { value: null, matchMode: FilterMatchMode.CONTAINS },
                nombre: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
                sede: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
                rol: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] }
            };
        },
        opendDialog() {
            if (this.selectedRecord == null) {
                this.$swal.fire({
                    position: "top-center",
                    icon: "error",
                    title: "Error",
                    text: "Debe seleccionar una linea primero",
                    showConfirmButton: true,
                    timer: config.globales.timer_errores,
                });
                return
            }
            this.editarProfeInfo.codigo = this.selectedRecord.codigo
            this.editarProfeInfo.nombre = this.selectedRecord.nombre
            this.editarProfeInfo.apellido1 = this.selectedRecord.apellido1
            this.editarProfeInfo.apellido2 = this.selectedRecord.apellido2
            this.editarProfeInfo.teloficina = this.selectedRecord.teloficina
            this.editarProfeInfo.telcelular = this.selectedRecord.telcelular
            this.editarProfeInfo.oficina = this.selectedRecord.oficina
            this.editarProfeInfo.correo = this.selectedRecord.correo
            this.profeFoto = null
            this.EditarDialog = this.EditarDialog === true ? false : true;
            if(this.EditarDialog === false)
                this.selectedRecord = null
        },
        regProfDiag() {
            this.profeFoto = null
            this.agregarProfeInfo= {
                codigosede: null,
                nombre: null,
                apellido1: null,
                apellido2: null,
                teloficina: null,
                telcelular:null,
                oficina:null,
                correo:null
            }
            this.regProfDiaglog = this.regProfDiaglog === true ? false : true;
        },
        async darBaja() {
          if (this.selectedRecord == null) {
            this.$swal.fire({
              position: "top-center",
              icon: "error",
              title: "Error",
              text: "Debe seleccionar una linea primero",
              showConfirmButton: true,
              timer: config.globales.timer_errores,
            });
            return
          }
          var codigo = this.selectedRecord.codigo;
          let borrar = null;
          borrar = await this.$swal.fire({
              title: "¿Está seguro que desea dar de baja al profesor?",
              text: "El equipo de trabajo estara incompleto",
              icon: "warning",
              showCancelButton: true,
              confirmButtonColor: "#3085d6",
              cancelButtonColor: "#d33",
              confirmButtonText: "Aceptar",
              cancelButtonText: "Cancelar",
          });
          if(!borrar.isConfirmed) {
            return
          }
          var request = {
                method: 'POST',
                headers: { Authorization: localStorage.token,"content-Type": "application/json"  }, //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
                body: JSON.stringify({
                    idasistente: localStorage.codigo,
                    codigoProfesor: codigo
                })
            };
            var response = await fetch('http://127.0.0.1:8000/darDeBajaAProfesor/', request);
            var myJson = await response.json();
            if (myJson.response === 'successful') {
                this.$swal.fire({
                    position: "top-center",
                    icon: "success",
                    title: "Enhorabuena",
                    text: "Profesor dado de baja correctamente.",
                    showConfirmButton: true,
                    timer: config.globales.timer_errores,
                });
                this.getProfesDisabled();
                this.getTableContents();
            } else {
                console.log(myJson)
                await this.$swal.fire({
                    position: "top-center",
                    icon: "warning",
                    title: "Error",
                    text: "No se completo con exito",
                    showConfirmButton: true,
                    timer: config.globales.timer_errores,
                });
            }
        },
        opendDetailDialog() {
          if (this.selectedRecord == null) {
          this.$swal.fire({
            position: "top-center",
            icon: "warning",
            title: "Error",
            text: "Debe seleccionar una linea primero",
            showConfirmButton: true,
            timer: config.globales.timer_errores,
          });

        }
          if (this.selectedRecord !== null)
            this.detailInfo = this.detailInfo === true ? false : true;
        },
        openAddProfe2Team() {
            this.addProfe2Team = this.addProfe2Team === true ? false : true;
        },
        async getTableContents() {
            var request = {
                method: 'GET',
                headers: { Authorization: localStorage.token } //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
            };
            var response = await fetch('http://127.0.0.1:8000/DetalleEquipo/', request);
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
        async getProfesDisabled() {
            var request = {
                method: 'GET',
                headers: { Authorization: localStorage.token } //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
            };
            var response = await fetch('http://127.0.0.1:8000/DetalleProfes/', request);
            var myJson = await response.json();
            if (myJson.response === 'unsuccessful') {
                console.log('no exito');
            } else {
              this.profesDisabled = myJson.profes;
              console.log(this.profesDisabled)
            }
        },
        async registroProfesores() {
            const repattern = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/;
            for (var algo in this.agregarProfeInfo) {
                if(this.agregarProfeInfo[algo]===null) {
                    this.regProfDiaglog = false
                    await this.$swal.fire({
                        position: "top-center",
                        icon: "warning",
                        title: "Error",
                        text: "Faltan datos",
                        showConfirmButton: true,
                        timer: config.globales.timer_errores,
                    });
                    this.regProfDiaglog = true
                    return
                }
            }

            if(!repattern.test(this.agregarProfeInfo.correo)) {
                this.regProfDiaglog = false
                await this.$swal.fire({
                    position: "top-center",
                    icon: "warning",
                    title: "Error",
                    text: "El formato del correo es incorrecto",
                    showConfirmButton: true,
                    timer: config.globales.timer_errores,
                });
                this.regProfDiaglog = true
                return
            }

            if(this.profeFoto===null){
                this.profeFoto = new FormData
            }

            this.profeFoto.append('json',JSON.stringify(this.agregarProfeInfo))

            var request = {
                method: 'POST',
                headers: { Authorization: localStorage.token }, //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
                body: this.profeFoto
            };
            var response = await fetch('http://127.0.0.1:8000/registrarProfesor/', request);
            var myJson = await response.json();
            if (myJson.response === 'successful') {
                this.regProfDiag();
                this.$swal.fire({
                    position: "top-center",
                    icon: "success",
                    title: "Enhorabuena",
                    text: "Profesor agregado correctamente.",
                    showConfirmButton: true,
                    timer: config.globales.timer_errores,
                });
                this.getProfesDisabled();
            } else if (myJson.response === "Ya existe un profesor con este correo" ) {
                this.regProfDiaglog = false
                await this.$swal.fire({
                    position: "top-center",
                    icon: "warning",
                    title: "Error",
                    text: "El correo ya existe",
                    showConfirmButton: true,
                    timer: config.globales.timer_errores,
                });
                this.regProfDiaglog = true
            } else {
                console.log(myJson)
                this.regProfDiaglog = false
                    await this.$swal.fire({
                        position: "top-center",
                        icon: "warning",
                        title: "Error",
                        text: "No se completo con exito",
                        showConfirmButton: true,
                        timer: config.globales.timer_errores,
                    });
                this.regProfDiaglog = true
            }
        },
        async editarProfesores() {
            const repattern = /^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/;
            console.log(this.editarProfeInfo)
            for (var algo in this.editarProfeInfo) {
                if(this.editarProfeInfo[algo]===null && algo !== 'idasistente') {
                    this.EditarDialog = false
                    await this.$swal.fire({
                        position: "top-center",
                        icon: "warning",
                        title: "Error",
                        text: "Faltan datos",
                        showConfirmButton: true,
                        timer: config.globales.timer_errores,
                    });
                    this.EditarDialog = true
                    return
                }
            }

            if(!repattern.test(this.editarProfeInfo.correo)) {
                this.EditarDialog = false
                await this.$swal.fire({
                    position: "top-center",
                    icon: "warning",
                    title: "Error",
                    text: "El formato del correo es incorrecto",
                    showConfirmButton: true,
                    timer: config.globales.timer_errores,
                });
                this.EditarDialog = true
                return
            }

            if(this.profeFoto===null){
                this.profeFoto = new FormData
            }
            
            if(!this.isAssist) {
                this.editarProfeInfo.idasistente = null
            }

            this.profeFoto.append('json',JSON.stringify(this.editarProfeInfo))

            var request = {
                method: 'POST',
                headers: { Authorization: localStorage.token }, //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
                body: this.profeFoto
            };
            var response = await fetch('http://127.0.0.1:8000/cambiarInfoProfesor/', request);
            var myJson = await response.json();
            if (myJson.response === 'successful') {
                this.updatePicture();
                this.opendDialog();
                this.$swal.fire({
                    position: "top-center",
                    icon: "success",
                    title: "Enhorabuena",
                    text: "Profesor editado correctamente.",
                    showConfirmButton: true,
                    timer: config.globales.timer_errores,
                });
                this.getTableContents()
            } else if (myJson.response === "Ya existe un profesor con este correo" ) {
                this.EditarDialog = false
                await this.$swal.fire({
                    position: "top-center",
                    icon: "warning",
                    title: "Error",
                    text: "El correo ya existe",
                    showConfirmButton: true,
                    timer: config.globales.timer_errores,
                });
                this.EditarDialog = true
            } else {
                console.log(myJson)
                this.EditarDialog = false
                    await this.$swal.fire({
                        position: "top-center",
                        icon: "warning",
                        title: "Error",
                        text: "No se completo con exito",
                        showConfirmButton: true,
                        timer: config.globales.timer_errores,
                    });
                this.EditarDialog = true
            }
        },
        async updatePicture() {
            var request = {
                method: 'GET',
                headers: { Authorization: localStorage.token } //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
            };
            var response = await fetch('http://127.0.0.1:8000/GetProfileImage/', request);
            var myJson = await response.json();
            localStorage.imgUrl = myJson.imgUrl
            console.log(myJson.imgUrl)
        },
        async registroIngreso() {
            if(this.selectedIngreso === null) {
                this.addProfe2Team = false
                await this.$swal.fire({
                    position: "top-center",
                    icon: "warning",
                    title: "Error",
                    text: "Debe seleccionar una linea primero",
                    showConfirmButton: true,
                    timer: config.globales.timer_errores,
                });
                this.addProfe2Team = true
                return
            }
            if(this.rolIngreso === null) {
                this.addProfe2Team = false
                await this.$swal.fire({
                    position: "top-center",
                    icon: "warning",
                    title: "Error",
                    text: "Debe seleccionar un rol primero",
                    showConfirmButton: true,
                    timer: config.globales.timer_errores,
                });
                this.addProfe2Team = true
                return
            }
            var request = {
                method: 'POST',
                headers: { Authorization: localStorage.token,"content-Type": "application/json"  }, //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
                body: JSON.stringify({
                    idasistente: localStorage.codigo,
                    codigo: this.selectedIngreso.codigo,
                    rol: this.rolIngreso
                })
            };
            var response = await fetch('http://127.0.0.1:8000/registrarNuevoIntegrante/', request);
            var myJson = await response.json();
            if (myJson.response === 'successful') {
                this.openAddProfe2Team();
                this.$swal.fire({
                    position: "top-center",
                    icon: "success",
                    title: "Enhorabuena",
                    text: "Profesor agregado correctamente.",
                    showConfirmButton: true,
                    timer: config.globales.timer_errores,
                });
                this.getProfesDisabled();
                this.getTableContents();
            } else if (myJson.error === "Ya existe un profesor con este correo") {
                this.addProfe2Team = false
                await this.$swal.fire({
                    position: "top-center",
                    icon: "warning",
                    title: "Error",
                    text: "Ya existe un profesor con este correo",
                    showConfirmButton: true,
                    timer: config.globales.timer_errores,
                });
                this.addProfe2Team = true
            } else if (myJson.response === "El asistente debe ser de Cartago") {
                this.addProfe2Team = false
                await this.$swal.fire({
                    position: "top-center",
                    icon: "warning",
                    title: "Error",
                    text: "Asignar coordinadores es funcion unicamente del asistente de cartago",
                    showConfirmButton: true,
                    timer: config.globales.timer_errores,
                });
                this.addProfe2Team = true
            } else {
                console.log(myJson)
                this.openAddProfe2Team();
                await this.$swal.fire({
                    position: "top-center",
                    icon: "warning",
                    title: "Error",
                    text: "No se completo con exito",
                    showConfirmButton: true,
                    timer: config.globales.timer_errores,
                });
            }
        },
        async convertirCoordinador() {
            if(this.selectedRecord === null) {
                await this.$swal.fire({
                    position: "top-center",
                    icon: "warning",
                    title: "Error",
                    text: "Debe seleccionar una linea primero",
                    showConfirmButton: true,
                    timer: config.globales.timer_errores,
                });
                return
            }
            if(this.selectedRecord.rol === 'Coordinador') {
                await this.$swal.fire({
                    position: "top-center",
                    icon: "warning",
                    title: "Error",
                    text: "El individuo ya es coordinador",
                    showConfirmButton: true,
                    timer: config.globales.timer_errores,
                });
                return
            }
            var request = {
                method: 'POST',
                headers: { Authorization: localStorage.token,"content-Type": "application/json"  }, //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
                body: JSON.stringify({
                    idasistente: localStorage.codigo,
                    codigoProfesor: this.selectedRecord.codigo
                })
            };
            var response = await fetch('http://127.0.0.1:8000/definirCoordinador/', request);
            var myJson = await response.json();
            if (myJson.response === 'successful') {
                this.selectedRecord = null
                this.$swal.fire({
                    position: "top-center",
                    icon: "success",
                    title: "Enhorabuena",
                    text: "Profesor coordinador asignado",
                    showConfirmButton: true,
                    timer: config.globales.timer_errores,
                });
                this.getTableContents();
            } else if (myJson.response === "El asistente debe ser de Cartago") {
                await this.$swal.fire({
                    position: "top-center",
                    icon: "warning",
                    title: "Error",
                    text: "Funcion solo permitida por el asistente de Cartago",
                    showConfirmButton: true,
                    timer: config.globales.timer_errores,
                });
            } else {
                console.log(myJson)
                await this.$swal.fire({
                    position: "top-center",
                    icon: "warning",
                    title: "Error",
                    text: "No se logro completar con exito la operacion",
                    showConfirmButton: true,
                    timer: config.globales.timer_errores,
                });
            }
        },
        async getSedes() {
            var request = {
                method: 'GET',
                headers: { Authorization: localStorage.token} //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
            };
            var response = await fetch('http://127.0.0.1:8000/ObtenerSedes/', request);
            var myJson = await response.json();
            if (myJson.response === 'unsuccessful') {
                console.log('no exito');
            } else {
              this.allSedes = myJson.sedes;
              console.log(this.allSedes)
            }
        },
        async getRoles() {
            var request = {
                method: 'GET',
                headers: { Authorization: localStorage.token } //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
            };
            var response = await fetch('http://127.0.0.1:8000/ObtenerRoles/', request);
            var myJson = await response.json();
            if (myJson.response === 'unsuccessful') {
                console.log('no exito');
            } else {
              this.allRoles = myJson.roles;
              console.log(this.allRoles)
            }
        },
        async assignFile(event) {
            this.profeFoto = new FormData();
            this.profeFoto.append('foto', event.files[0]);
        },
    }
};
</script>

<template>
    <div class="grid format">
        <div class="col-12">
            <div class="card">
                <DataTable
                    :value="equipoGuia"
                    :paginator="true"
                    class="p-datatable-gridlines"
                    :rows="10"
                    dataKey="numprofesor"
                    :rowHover="true"
                    v-model:filters="filters"
                    :filters="filters"
                    responsiveLayout="scroll"
                    :globalFilterFields="['nombre', 'sede', 'rol']"
                    v-model:selection="this.selectedRecord"
                    :sorteable="true"
                    :resizableColumns="true"
                    :autoLayout="true"
                    selectionMode="single"
                    :scrollable="true"
                    scrollHeight="flex"
                    tableStyle="min-width: 50rem"
                    @update:selection="this.enableEditButton"
                >
                    <template #header>

                      <div class="mb-3 flex align-items-center justify-content-between">
                        <span class="text-xl font-normal text-900">Equipo de Trabajo</span>
                        <div class="overflow-y-auto">
                          <Button type="button" icon="pi pi-filter-slash" label="Clear" class="p-button-outlined mr-2 mb-2 p-button-help" @click="clearFilter()" />
                          <Button label="Ver Detalle" class="p-button-outlined mr-2 mb-2 p-button-warning" @click="this.opendDetailDialog()" />
                          <Button v-tooltip.top="'Agrega un profesor al equipo de trabajo.'" label="Agregar Profesor" class="p-button-outlined mr-2 mb-2 p-button-success" v-show="isAssist" @click="this.openAddProfe2Team()" />
                          <Button v-tooltip.top="'Agregar un nuevo profesor a la liste general de profesores.'" label="Registrar Profesor" class="p-button-outlined mr-2 mb-2 p-button-icon" v-show="isAssist" @click="this.regProfDiag()" />
                          <Button label="Dar de Baja" class="p-button-outlined mr-2 mb-2 p-button-danger" v-show="isAssist" @click="this.darBaja()" />
                          <Button label="Convertir Coordinador" class="p-button-outlined mr-2 mb-2 p-button-info" v-show="isAssist" @click="this.convertirCoordinador()" />
                          <Button label="Editar" class="p-button-outlined mr-2 mb-2" v-show="editIsEnable" @click="this.opendDialog()" />
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
                    <Column field="sede" header="Sede" :sortable="true" style="min-width: 12rem">
                        <template #body="slotProps">
                            {{ slotProps.data.sede }}
                        </template>
                    </Column>
                    <Column field="rol" header="Rol" :sortable="true" style="min-width: 12rem">
                        <template #body="slotProps">
                            {{ slotProps.data.rol }}
                        </template>
                    </Column>
                </DataTable>
            </div>
        </div>
    </div>
    <Dialog v-model:visible="detailInfo" :modal="true" :maximizable="true" appendTo="self" :style="{ width: '52vw' }" :breakpoints="{ '960px': '75vw', '640px': '100vw' }">
        <div class="surface-ground">
            <div class="surface-section px-6 pt-5">
                <div class="text-3xl font-medium text-900 mb-4">Detalles</div>
            </div>
            <div class="surface-section px-6 py-5">
                <div class="flex align-items-start flex-column lg:flex-row lg:justify-content-between">
                    <div class="flex align-items-start flex-column md:flex-row">
                        <img :src="'/images/' + this.selectedRecord.fotografia" @error="$event.target.src='/images/notfound.png'" class="mr-5 mb-3 lg:mb-0 border-circle" style="width: 90px; height: 90px" />
                        <div>
                            <span class="text-900 font-medium text-3xl">{{ this.selectedRecord.nombre }} {{ this.selectedRecord.apellido1 }} {{ this.selectedRecord.apellido2 }}</span>
                            <i class="pi pi-star-fill text-2xl ml-4 text-yellow-500" v-if="selectedRecord.rol === 'Profesor Coordinador'"></i>
                            <div class="text-500">{{ this.selectedRecord.correo }}</div>
                            <div class="flex align-items-center flex-wrap text-sm">
                                <div class="mr-5 mt-3">
                                    <span class="font-medium text-500">Sede</span>
                                    <div class="text-700 mt-2">{{ this.selectedRecord.sede }}</div>
                                </div>
                                <div class="mr-5 mt-3">
                                    <span class="font-medium text-500">Código</span>
                                    <div class="text-700 mt-2">{{ this.selectedRecord.codigo }}</div>
                                </div>
                              <div class="mr-5 mt-3">
                              <span class="font-medium text-500">Oficina</span>
                              <div class="text-700 mt-2">{{ this.selectedRecord.oficina }}</div>
                            </div>
                                <div class="mr-5 mt-3">
                                    <span class="font-medium text-500">Teléfono Oficina</span>
                                    <div class="text-700 mt-2">{{ this.selectedRecord.teloficina }}</div>
                                </div>

                              <div class="mt-3">
                                    <span class="font-medium text-500">Teléfono Personal</span>
                                    <div class="text-700 mt-2">{{ this.selectedRecord.telcelular }}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="mt-3 lg:mt-0">
                        <Button icon="pi pi-bookmark" class="p-button-rounded mr-2"></Button>
                        <Button icon="pi pi-heart" class="p-button-rounded p-button-success mr-2"></Button>
                        <Button icon="pi pi-list" class="p-button-rounded p-button-help"></Button>
                    </div>
                </div>
            </div>
        </div>
    </Dialog>

    <!-- PROFE AL TEAM PA -->      
    <Dialog v-model:visible="addProfe2Team" :modal="true" :maximizable="true" appendTo="self" :style="{ width: '70vw' }" :breakpoints="{ '960px': '75vw', '640px': '100vw' }">
      <div class="grid format2">
        <div class="col-8">
          <div class="card">
            <DataTable
                :value="profesDisabled"
                :paginator="true"
                class="p-datatable-gridlines"
                :rows="10"
                dataKey="id"
                :rowHover="true"
                v-model:filters="filters"
                filterDisplay="menu"
                :filters="filters"
                responsiveLayout="scroll"
                :globalFilterFields="['nombre', 'sede', 'rol']"
                v-model:selection="selectedIngreso"
                :sorteable="true"
                :resizableColumns="true"
                :autoLayout="true"
                selectionMode="single"
                :scrollable="true"
                scrollHeight="flex"
            >
              <template #header>

                <div class="mb-3 flex align-items-center justify-content-between">
                  <span class="text-xl font-normal text-900">Profesores</span>
                  <div class="overflow-y-auto">
                    <Dropdown v-model="this.rolIngreso" :options="this.allRoles" optionValue="desrol" optionLabel="desrol" placeholder="Seleccione un rol" class="w-full md:w-14rem mr-2" />
                    <Button label="Ingresar Profesores" class="p-button-outlined mr-2 mb-2 p-button-success" @click="this.registroIngreso()" />
                    <span class="p-input-icon-left mb-2">
                                <i class="pi pi-search" />
                                <InputText v-model="filters['global'].value" placeholder="Buscar..." style="width: 100%" />
                            </span>
                  </div>
                </div>
              </template>
              <template #empty> No hay información disponible </template>
              <template #loading> Cargando, por favor espere. </template>
              <Column field="codigo" header="codigo" :sortable="true" class="p-col-2">
                <template #body="slotProps">
                  {{ slotProps.data.codigo }}
                </template>
              </Column>
              <Column field="nombre" header="Nombre" :sortable="true" class="p-col-2">
                <template #body="slotProps">
                  {{ slotProps.data.nombre }}
                </template>
              </Column>
              <Column field="sede" header="Sede" :sortable="true" class="p-col-1" style="min-width: auto">
                <template #body="slotProps">
                  {{ slotProps.data.sede }}
                </template>
              </Column>
            </DataTable>
          </div>
        </div>
      </div>
    </Dialog>
    <Dialog v-model:visible="this.EditarDialog" :modal="true" :maximizable="true" appendTo="self" :style="{ width: '52vw' }" :breakpoints="{ '960px': '75vw', '640px': '100vw' }">
        <div class="surface-ground px-4 py-8 md:px-6 lg:px-8">
            <div class="p-fluid flex flex-column lg:flex-row">
                <div class="surface-card p-5 shadow-2 border-round flex-auto">
                    <div class="text-900 font-semibold text-lg mt-3">Perfil</div>
                    <Divider></Divider>
                    <div class="flex gap-5 flex-column-reverse md:flex-row">
                        <div class="flex-auto p-fluid">
                            <div class="mb-4">
                                <label for="state" class="block font-medium text-900 mb-2">Nombre</label>
                                <InputText id="state" type="text" v-model.trim="this.editarProfeInfo.nombre" />
                            </div>
                            <div class="mb-4">
                                <label for="state" class="block font-medium text-900 mb-2">Apellido 1</label>
                                <InputText id="state" type="text" v-model.trim="this.editarProfeInfo.apellido1" />
                            </div>
                            <div class="mb-4">
                                <label for="state" class="block font-medium text-900 mb-2">Apellido 2</label>
                                <InputText id="state" type="text" v-model.trim="this.editarProfeInfo.apellido2" />
                            </div>
                            <div class="mb-4">
                                <label for="sede" class="block font-medium text-900 mb-2">Sedes</label>
                                <Dropdown v-model="this.selectedRecord.sede" disabled :options="this.allSedes" optionValue="codigosede" optionLabel="codigosede" placeholder="Select" />
                            </div>
                            <div class="mb-4">
                                <label for="ID" class="block font-medium text-900 mb-2">Telefono de Oficina</label>
                                <InputText id="state" type="text" v-model.trim="this.editarProfeInfo.teloficina" />
                            </div>
                            <div class="mb-4">
                                <label for="state" class="block font-medium text-900 mb-2">Oficina</label>
                                <InputText id="state" type="text" v-model.trim="this.editarProfeInfo.oficina" />
                            </div>
                            <div class="mb-4">
                                <label for="state" class="block font-medium text-900 mb-2">Correo Institucional</label>
                                <InputText id="state" type="text" :disabled="!this.isAssist" v-model.trim="this.editarProfeInfo.correo" />
                            </div>
                            <div class="mb-4">
                                <label for="state" class="block font-medium text-900 mb-2">Número Celular</label>
                                <InputText id="state" type="text" v-model.trim="this.editarProfeInfo.telcelular" />
                            </div>
                            <div>
                                <Button label="Editar Profesor" class="w-auto mr-2" @click="this.editarProfesores()"></Button>
                            </div>
                        </div>
                        <div class="flex flex-column align-items-center flex-or">
                            <span class="font-medium text-900 mb-2">Foto</span>
                            <FileUpload mode="basic" name="fotoProfe" chooseLabel="Subir" :auto="true" accept="image/*" :maxFileSize="1000000" :customUpload="true" @uploader="this.assignFile" />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </Dialog>
    <Dialog v-model:visible="this.regProfDiaglog" :modal="true" :maximizable="true" appendTo="self" :style="{ width: '52vw' }" :breakpoints="{ '960px': '75vw', '640px': '100vw' }">
        <div class="surface-ground px-4 py-8 md:px-6 lg:px-8">
            <div class="p-fluid flex flex-column lg:flex-row">
                <div class="surface-card p-5 shadow-2 border-round flex-auto">
                    <div class="text-900 font-semibold text-lg mt-3">Perfil</div>
                    <Divider></Divider>
                    <div class="flex gap-5 flex-column-reverse md:flex-row">
                        <div class="flex-auto p-fluid">
                            <div class="mb-4">
                                <label for="state" class="block font-medium text-900 mb-2">Nombre</label>
                                <InputText id="state" type="text" v-model.trim="this.agregarProfeInfo.nombre" />
                            </div>
                            <div class="mb-4">
                                <label for="state" class="block font-medium text-900 mb-2">Apellido 1</label>
                                <InputText id="state" type="text" v-model.trim="this.agregarProfeInfo.apellido1" />
                            </div>
                            <div class="mb-4">
                                <label for="state" class="block font-medium text-900 mb-2">Apellido 2</label>
                                <InputText id="state" type="text" v-model.trim="this.agregarProfeInfo.apellido2" />
                            </div>
                            <div class="mb-4">
                                <label for="sede" class="block font-medium text-900 mb-2">Sedes</label>
                                <Dropdown v-model="this.agregarProfeInfo.codigosede" :options="this.allSedes" optionValue="codigosede" optionLabel="codigosede" placeholder="Select" />
                            </div>
                            <div class="mb-4">
                                <label for="ID" class="block font-medium text-900 mb-2">Telefono de Oficina</label>
                                <InputNumber :useGrouping="false" id="ID" type="number" :max=99999999 :min=10000000 v-model.trim="this.agregarProfeInfo.teloficina" />
                            </div>
                            <div class="mb-4">
                                <label for="state" class="block font-medium text-900 mb-2">Oficina</label>
                                <InputText id="state" type="text" v-model.trim="this.agregarProfeInfo.oficina" />
                            </div>
                            <div class="mb-4">
                                <label for="state" class="block font-medium text-900 mb-2">Correo Institucional</label>
                                <InputText id="state" type="text" v-model.trim="this.agregarProfeInfo.correo" />
                            </div>
                            <div class="mb-4">
                                <label for="state" class="block font-medium text-900 mb-2">Número Celular</label>
                                <InputNumber :useGrouping="false" id="ID" type="number" v-model.trim="this.agregarProfeInfo.telcelular" :max=99999999 :min=10000000 />
                            </div>
                            <div>
                                <Button label="Agregar" class="w-auto mr-2" @click="this.registroProfesores()"></Button>
                            </div>
                        </div>
                        <div class="flex flex-column align-items-center flex-or">
                            <span class="font-medium text-900 mb-2">Foto</span>
                            <FileUpload mode="basic" name="fotoProfe" chooseLabel="Subir" :auto="true" accept="image/*" :maxFileSize="1000000" :customUpload="true" @uploader="this.assignFile" />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </Dialog>
</template>


<style scoped lang="scss">
//* {
//  border: 1px solid red;
//}

::v-deep(.p-datatable-frozen-tbody) {
    font-weight: bold;
}

::v-deep(.p-datatable-scrollable .p-frozen-column) {
    font-weight: bold;
}

.format {
    width: 98vw;
    height: 84vh;
}

.format2 {
    width: 95vw;
    height: 85vh;
}

</style>
