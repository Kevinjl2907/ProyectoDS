<script>
import { FilterMatchMode, FilterOperator } from 'primevue/api';
import config from '@/service/config.js';


// eslint-disable-next-line vue/no-export-in-script-setup
export default {
  name: "Equipo Guia",
  data() {

    return {
      // URL's
      url: "comunes/monedas/",
      // Variables utilizadas por el CRUD
      editMode: false,
      addMode: false,
      searchMode: true,
      EditarDialog: false,
      deleteDialog: false,
      selectedRecord: null,
      realizarDialog: false,
      currentPlanTrabajo: false,
      filters: {
        global: {value: null, matchMode: FilterMatchMode.CONTAINS},
        nombre: {value: null, matchMode: FilterMatchMode.CONTAINS},
      },
      // Variables utilizadas por la pantalla
      equipoGuia: null,
      justificacion: '',
      fileAfiche: null,
      enlace: '',
      actividades: null,
      bodyActividad: {
        planTrabajo: null
      },
      planesTrabajo: null,
      bodypublicarActividad: {
        idactividad: null
      },
      bodyCancelarActividad: {
        idactividad: null,
        justificacion: null,
      },

      bodyRealizarActividad: {
          idactividad: 'unid',
          enlace: 'unenlace'
        },
    };
  },
  created() {
    this.getPlanesTrabajo();
  },
  async mounted() {
    this.clearFilter();
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
    close(mostrar = false) {
      this.selectedRecord = null;
      this.limpiar();
      if (mostrar) {
        this.mostrar();
      }
    },
    limpiar() {
      (this.editMode = false), (this.addMode = false), (this.searchMode = false), (this.EditarDialog = false);
      this.justificacion = '';
      this.realizarDialog = false;
    },
    opendDialog() {
      this.EditarDialog = this.EditarDialog === true ? false : true
    },
    openRealizarActividadDialog() {
      this.realizarDialog = this.realizarDialog === true ? false : true
    },
    async deleteItem() {
      this.opendDialog()
      if (this.selectedRecord == null) {
        this.$swal.fire({
          position: "top-center",
          icon: "error",
          title: "Error",
          text: "Debe seleccionar una linea primero",
          showConfirmButton: true,
          timer: config.globales.timer_errores,
        });
      }
      else {
        this.bodyCancelarActividad.idactividad = this.selectedRecord.idactividad;
        this.bodyCancelarActividad.justificacion = this.justificacion;
        var request = {
          method: 'POST',
          headers: { Authorization: localStorage.token, 'Content-Type': 'application/json' },

          body: JSON.stringify(this.bodyCancelarActividad) //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
        };
        var response = await fetch('http://127.0.0.1:8000/PublicarActividad/', request);
        var myJson = await response.json();
        console.log(this.bodyActividad);
        this.close();
        if (myJson.response === 'unsuccessful') {
          console.log('no exito');
        } else if((myJson.response === 'successful')){
          this.$swal.fire({
            position: "top-center",
            icon: "success",
            title: "Publicado",
            text: "La actividad ha sido cancelada correctamente.",
            showConfirmButton: true,
            timer: config.globales.timer_errores,
          });
        }
        else {
          this.$swal.fire({
            position: "top-center",
            icon: "warning",
            title: "Error",
            text: "Algo ha sucedido, revisa e intentalo de nuevo.",
            showConfirmButton: true,
            timer: config.globales.timer_errores,
          });
        }
      }
    },
    async publicarActividad() {

      if (this.selectedRecord == null) {
        
        this.$swal.fire({
          position: "top-center",
          icon: "error",
          title: "Error",
          text: "Debe seleccionar una linea primero",
          showConfirmButton: true,
          timer: config.globales.timer_errores,
        });
      }
        else {
          this.bodypublicarActividad.idactividad = this.selectedRecord.idactividad;
          var request = {
            method: 'POST',
            headers: { Authorization: localStorage.token, 'Content-Type': 'application/json' },

            body: JSON.stringify(this.bodypublicarActividad) //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
          };
          var response = await fetch('http://127.0.0.1:8000/PublicarActividad/', request);
          var myJson = await response.json();
          console.log(this.bodyActividad);
          if (myJson.response === 'unsuccessful') {
            console.log('no exito');
          } else if((myJson.response === 'successful')){
            this.$swal.fire({
              position: "top-center",
              icon: "success",
              title: "Publicado",
              text: "La actividad ha sido publicada correctamente.",
              showConfirmButton: true,
              timer: config.globales.timer_errores,
            });
          }
          else {
            this.$swal.fire({
              position: "top-center",
              icon: "warning",
              title: "Error",
              text: "Algo ha sucedido, revisa e intentalo de nuevo.",
              showConfirmButton: true,
              timer: config.globales.timer_errores,
            });
          }
        }
    },
    async realizarActividad() {
      if (this.selectedRecord == null) {
        this.openRealizarActividadDialog()
        this.$swal.fire({
          position: "top-center",
          icon: "error",
          title: "Error",
          text: "Debe seleccionar una linea primero",
          showConfirmButton: true,
          timer: config.globales.timer_errores,
        });
      }
        else {
        console.log('esto es lo seleccionadoooooooo',this.selectedRecord)
        console.log('esta es la actividad', this.selectedRecord.idactividad)
          this.bodyRealizarActividad.idactividad = this.selectedRecord.idactividad;
          this.bodyRealizarActividad.enlace = this.enlace;
          this.fileAfiche.append('json', JSON.stringify(this.bodyRealizarActividad))
        this.close();

          var request = {
            method: 'POST',
            headers: { Authorization: localStorage.token, },

            body: this.fileAfiche //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
          };
          var response = await fetch('http://127.0.0.1:8000/RealizarActividad/', request);
          var myJson = await response.json();
          if (myJson.response === 'unsuccessful') {
            console.log('no exito');
          } else if((myJson.response === 'successful')){
            this.$swal.fire({
              position: "top-center",
              icon: "success",
              title: "Publicado",
              text: "La actividad ha sido realizada correctamente.",
              showConfirmButton: true,
              timer: config.globales.timer_errores,
            });
          }
          else {
            this.$swal.fire({
              position: "top-center",
              icon: "warning",
              title: "Error",
              text: "Algo ha sucedido, revisa e intentalo de nuevo.",
              showConfirmButton: true,
              timer: config.globales.timer_errores,
            });
          }
        }
    },
    /*async getTableContents() {
      var request = {
        method: "GET",
        headers: {"Authorization": localStorage.token}, //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
      };
      var response = await fetch("http://127.0.0.1:8000//", request)
      var myJson = await response.json()
      if (myJson.response === 'unsuccessful') {
        console.log('no exito')
      } else {
        this.actividades = myJson.actividades
        console.log(this.actividades)
      }
    },*/
    async getPlanesTrabajo() {
      var request = {
        method: 'GET',
        headers: { Authorization: localStorage.token } //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
      };
      var response = await fetch('http://127.0.0.1:8000/PlanesTrabajoDisponibles/', request);
      var myJson = await response.json();
      if (myJson.response === 'unsuccessful') {
        console.log('no exito');
      } else {
        console.log(myJson);
        this.planesTrabajo = myJson.planes;
      }
    },
    async buscarActividades() {
      this.bodyActividad.planTrabajo = this.currentPlanTrabajo.semestre;
      var request = {
        method: 'POST',
        headers: { Authorization: localStorage.token, 'Content-Type': 'application/json' },

        body: JSON.stringify(this.bodyActividad) //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
      };
      var response = await fetch('http://127.0.0.1:8000/ObtenerActividades/', request);
      var myJson = await response.json();
      console.log(this.bodyActividad);
      if (myJson.response === 'unsuccessful') {
        console.log('no exito');
      } else {
        console.log(myJson);
        this.actividades = myJson.actividades;
      }
    },

    async asignFile(event) {
      this.fileAfiche = new FormData();
      for (const file in event.files) {
        this.fileAfiche.append(`file${file}`, event.files[file]);
      }
    },
  }

};

</script>

<template>
    <div class="grid format">
        <div class="col-12">
            <div class="card">
              <div class="field mb-4 col-12 md:col-6">
                <label class="font-medium w-full">Semestre del Plan</label>
                <Dropdown v-model="this.currentPlanTrabajo" @change="this.buscarActividades()" :options="this.planesTrabajo" optionLabel="semestre" placeholder="Plan de trabajo" class="w-full">
                  <template #option="slotProps">
                    <div class="flex align-items-center">
                      <div>{{ slotProps.option.semestre }}</div>
                    </div>
                  </template>
                </Dropdown>
              </div>
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
                    v-model:selection="selectedRecord"
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
                          <Button type="button" label="Restablecer" class="p-button-outlined mr-2 mb-2" style="background-color: #468480; color: white;" @click="initFilters()" />
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
                  <Column headerStyle="min-width:10rem;">
                    <template #body="slotProps">
                      <Button v-tooltip.top="'Publicar Actividad'" icon="pi pi-megaphone" class="p-button-rounded p-button-success mr-2" @click="this.publicarActividad()" />
                      <Button v-tooltip.top="'Cancelar Actividad'" icon="pi pi-times" class="p-button-rounded p-button-danger mr-2" @click="this.opendDialog()" />
                      <Button v-tooltip.top="'Realizar Actividad'" icon="pi pi-thumbs-up" class="p-button-rounded p-button-warning mt-2" @click="this.openRealizarActividadDialog()" />
                    </template>
                  </Column>
                </DataTable>
            </div>
        </div>
    </div>
    <Dialog id="justificacionDialog" v-model:visible="EditarDialog" :modal="true" :maximizable="true" appendTo="self" :style="{ width: '52vw' }" :breakpoints="{ '960px': '75vw', '640px': '100vw' }">
      <form class="flex flex-column gap-3 mt-3">
        <div class="w-full">
          <label class="block mb-1 text-color text-base">Justificación sobre la cancelación</label>
          <Textarea v-model="justificacion" autoResize rows="5" cols="30" autofocus placeholder="Escriba aquí su justificación" class="w-full"/>
        </div>
      </form>
      <template #footer>
        <Button v-tooltip="'Cancelar Actividad'" icon="pi pi-cog" class="p-button-outlined" label="Cancelar Actividad" @click="this.deleteItem()"/>
      </template>
    </Dialog>
  <Dialog id="realizarActividadDialog" v-model:visible="realizarDialog" :modal="true" :maximizable="true" appendTo="self" :style="{ width: '52vw' }" :breakpoints="{ '960px': '75vw', '640px': '100vw' }">
    <form class="flex flex-column gap-3 mt-3">
      <label class="block mb-1 text-color text-base w-full">Link de Evidencia</label>
      <div class="w-full">
        <div class="p-inputgroup">
          <span class="p-inputgroup-addon">www</span>
          <InputText id="website" type="text" placeholder="Ingrese el link de la reunión" :v-model="this.enlace"/>
        </div>
      </div>


      <div class="w-full">
        <label for="avatar" class="font-medium w-full">Afiche</label>
        <div class="flex align-items-center">
          <i class="pi  pi-file-import mr-4" style="font-size: 3rem"></i>
          <FileUpload mode="basic" name="afiche" :auto="true" url="./upload.php" accept="image/*" :multiple="true" :advance="true" :maxFileSize="1000000" class="p-button-outlined p-button-plain" chooseLabel="Subir Afiche" customUpload @uploader="asignFile" />
        </div>

      </div>


      <div class="w-full">
          <label class="block mb-1 text-color text-base w-full"></label>
      </div>
    </form>
    <template #footer>
      <Button v-tooltip="'Realizar Actividad'" icon="pi pi-cog" class="p-button-outlined" label="Realizar Actividad" @click="this.realizarActividad()"/>
    </template>
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
  width: 98vw;
  height: 84vh;
}

</style>
