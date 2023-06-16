<script>
import { FilterMatchMode, FilterOperator } from 'primevue/api';
import AgregarEstudiante from "@/views/profeGuia/AgregarEstudiante.vue";
import config from "@/service/Config";

// eslint-disable-next-line vue/no-export-in-script-setup
export default {
  name: "Estudiante",
  components: {AgregarEstudiante},
  data() {
    return {
      // URL's
      url: "comunes/monedas/",
      // Variables utilizadas por el CRUD
      editMode: false,
      addMode: false,
      searchMode: true,
      EditarDialog: false,
      agregarDialog: false,
      deleteDialog: false,
      selectedRecord: null,
      openDetail: false,
      // Variables utilizadas por la pantalla
      estudiantes: null,
      sedes: null,
      numEstudiante: null,
      nombre: null,
      apellido1: null,
      apellido2: null,
      nombreadicional: null,
      sede: null,
      correotec: null,
      telefono: null,
      isAsist: localStorage.type === 'asist' ? true : false,
      filters: {
        global: {value: null, matchMode: FilterMatchMode.CONTAINS},
        carnet: {value: null, matchMode: FilterMatchMode.CONTAINS},
        nombre: {value: null, matchMode: FilterMatchMode.CONTAINS},
        apellido1: {value: null, matchMode: FilterMatchMode.CONTAINS},
        apellido2: {value: null, matchMode: FilterMatchMode.CONTAINS},
        nombreadicional: {value: null, matchMode: FilterMatchMode.CONTAINS},
        sede: {value: null, matchMode: FilterMatchMode.CONTAINS},
        correotec: {value: null, matchMode: FilterMatchMode.CONTAINS},
        telefono: {value: null, matchMode: FilterMatchMode.CONTAINS},
      }
    };
  },
  created() {
    this.getTableContents()
    this.getSedes()
  },
  async mounted() {
    this.clearFilter();
  },
  methods: {
    clearFilter() {
      this.filtro = '';
      this.initFilters();
    },
    initFilters() {
      this.filters = {
        global: { value: null, matchMode: FilterMatchMode.CONTAINS },
        carnet: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
        nombre: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
        apellido1: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
        apellido2: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
        nombreadicional: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
        sede: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
        correotec: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
        telefono: { operator: FilterOperator.AND, constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }] },
      };
    },
    limpiar() {
      (this.editMode = false), (this.addMode = false), (this.searchMode = false), (this.EditarDialog = false);
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
              this.sedes = myJson.sedes;
              console.log(this.sedes)
            }
    },
    close(mostrar = false) {
      this.selectedRecord = null;
      this.limpiar();
      if (mostrar) {
        this.mostrar();
      }
    },
    opendDialog(){
      this.EditarDialog = this.EditarDialog === true ? false : true
    },
    openDetailDialog(){
      this.openDetail = this.openDetail === true ? false : true
    },
    agregarDialogOpen() {
      this.agregarDialog = true
    },
    agregarDialogClose() {
      this.agregarDialog = false
    },
    addStudent(){
      this.EditarDialog = this.EditarDialog === true ? false : true
    },
    editItem() {
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
      if (this.selectedRecord.sede !== localStorage.sede){
        this.$swal.fire({
          position: "top-center",
          icon: "warning",
          title: "Error",
          text: "Solo puede editar estudiantes de su propia sede.",
          showConfirmButton: true,
          timer: config.globales.timer_errores,
        });
      }
      else {
        this.carnet = this.selectedRecord.carnet;
        this.nombre = this.selectedRecord.nombre;
        this.apellido1 = this.selectedRecord.apellido1;
        this.apellido2 = this.selectedRecord.apellido2;
        this.nombreadicional = this.selectedRecord.nombreadicional;
        this.sede = this.selectedRecord.sede;
        this.correotec = this.selectedRecord.correotec;
        this.telefono = this.selectedRecord.telefono;
        (this.addMode = false), (this.searchMode = false);
        (this.editMode = true), (this.EditarDialog = true);
      }
    },
    async getTableContents() {
      var request = {
            method: "GET",
            headers: {"Authorization": localStorage.token}, //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
        };
        var response = await fetch("http://127.0.0.1:8000/ListaEstudiantes/", request)
            //.then(response => response.json())
            //.then(data => token=data)
            //.catch(error => console.error(error));
        var myJson = await response.json()
        if (myJson.response === 'unsuccessful') {
            console.log('no exito')
        } else {
          this.estudiantes = myJson.estudiantes
          console.log(this.estudiantes)
        }
    },
    async modEstudiante() {
      var edicion = {}
      
      if(!(this.nombre === this.selectedRecord.nombre)) {
        edicion["nombre"] = this.nombre
      }

      if(!(this.apellido1 === this.selectedRecord.apellido1)) {
        edicion["apellido1"] = this.apellido1
      }

      if(!(this.apellido2 === this.selectedRecord.apellido2)){
        edicion["apellido2"] = this.apellido2
      }

      if(!(this.nombreadicional === this.selectedRecord.nombreadicional)){
        edicion["nombreadicional"] = this.nombreadicional
      }

      if(!(this.sede === this.selectedRecord.sede)){
        edicion["sede"] = this.sede
      }

      if(!(this.telefono === this.selectedRecord.telefono)){
        edicion["telefono"] = this.telefono
      }

      console.log(edicion)
      var request = {
            method: "POST",
            headers: {"content-Type": "application/json",
                      "Authorization": localStorage.token}, //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
            body: JSON.stringify({
              carnet:this.carnet,
              editar:edicion
            })
      };

      var response = await fetch("http://127.0.0.1:8000/ModificarEstudiante/", request)
      response = await response.json()
      console.log(response.response)
      this.close();
      if(response.response === 'unsuccessful') {
        this.$swal.fire({
          position: "top-center",
          icon: "error",
          title: "Error",
          text: "Algo salio mal",
          showConfirmButton: true,
        });
      } else if(response.response === 'successful'){
        this.$swal.fire({
          position: "top-center",
          icon: "success",
          title: "Enhorabuena",
          text: "Se ha editado el registro",
          showConfirmButton: true,
        });
        this.getTableContents();
      }
    },
    async cargarExcel(event) {
      console.log(event.files[0])
      var elBody = new FormData()
      elBody.append('file',event.files[0])
      console.log(elBody)
      var request = {
          method: "POST",
          headers: {"Authorization": localStorage.token,}, //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
          body: elBody
      };

      var response = await fetch("http://127.0.0.1:8000/CargarExcel/", request)
      response = await response.json()
      console.log(response)
      this.agregarDialogClose();
      if(response.response === 'unsuccessful') {
        this.$swal.fire({
          position: "top-center",
          icon: "error",
          title: "Error",
          text: "El excel es incompatible o algun registro ya esta en la base de datos",
          showConfirmButton: true,
        });
      } else if(response.response === 'successful'){
        this.$swal.fire({
          position: "top-center",
          icon: "success",
          title: "Enhorabuena",
          text: "Se logro incluir todos los registros del excel",
          showConfirmButton: true,
        });
        this.getTableContents();
      }
    }
  },
};


</script>

<template>
  <div class="grid format">
    <div class="col-12">
      <div class="card">
        <DataTable
            :value="estudiantes"
            :paginator="true"
            class="p-datatable-gridlines"
            :rows="10"
            dataKey="carnet"
            :rowHover="true"
            v-model:filters="filters"
            filterDisplay="menu"
            :filters="filters"
            responsiveLayout="scroll"
            :globalFilterFields="['carnet','nombre', 'apellido1', 'apellido2', 'sede', 'correotec', 'telefono']"
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
              <span class="text-xl font-normal text-900">Estudiantes</span>
              <div class="overflow-y-auto">
                <Button type="button"  label="Restablecer" class="p-button-filled mr-2 mb-2" style="background-color: #468480; color: white;" @click="initFilters()" />
                <Button v-show="isAsist" label="Agregar" class="p-button-outlined p-button-success mr-2 mb-2" @click="this.agregarDialogOpen()"/>
                <Button v-show="!isAsist" label="Modificar estudiante" class="p-button-outlined p-button-warning mr-2 mb-2" style="background-color: #468480; color: white; " @click="this.editItem()"/>
              </div>
            </div>
          </template>
          <template #empty> No hay información disponible </template>
          <template #loading> Cargando, por favor espere. </template>
          <Column field="nombre" header="Identificacion" :sortable="true" style="min-width: 12rem">
            <template #body="slotProps">
              {{ slotProps.data.carnet }}
            </template>
          </Column>
          <Column field="nombre" header="Nombre" :sortable="true" style="min-width: 12rem">
            <template #body="slotProps">
              {{ slotProps.data.nombre }}
            </template>
          </Column>
          <Column field="apellido1" header="Primer Apellido" :sortable="true" style="min-width: 12rem">
            <template #body="slotProps">
              {{ slotProps.data.apellido1 }}
            </template>
          </Column>
          <Column field="apellido2" header="Segundo Apellido" :sortable="true" style="min-width: 12rem">
            <template #body="slotProps">
              {{ slotProps.data.apellido2 }}
            </template>
          </Column>
          <Column field="sede" header="Sede" :sortable="true" style="min-width: 12rem">
            <template #body="slotProps">
              {{ slotProps.data.sede }}
            </template>
          </Column>
          <Column field="correotec" header="Correo" :sortable="true" style="min-width: 12rem">
            <template #body="slotProps">
              {{ slotProps.data.correotec }}
            </template>
          </Column>
          <Column field="telefono" header="Celular" :sortable="true" style="min-width: 12rem">
            <template #body="slotProps">
              {{ slotProps.data.telefono }}
            </template>
          </Column>
        </DataTable>
      </div>
    </div>
  </div>
  <Dialog v-model:visible="this.openDetail" header="Ver detalles" :modal="true" :maximizable="true" appendTo="self" :style="{ width: '52vw' }" :breakpoints="{ '960px': '75vw', '640px': '100vw' }">

    <div class="surface-ground">
      <div class="surface-section px-6 pt-5">
        <div class="text-3xl font-medium text-900 mb-4">Detalles</div>
      </div>
      <div class="surface-section px-6 py-5">
        <div class="flex align-items-start flex-column lg:flex-row lg:justify-content-between">
          <div class="flex align-items-start flex-column md:flex-row">
            <img src="/images/avatar.png" class="mr-5 mb-3 lg:mb-0" style="width:90px;height:90px" />
            <div>
              <span class="text-900 font-medium text-3xl">{{this.selectedRecord.nombre}} {{this.selectedRecord.apellido1}} {{this.selectedRecord.apellido2}}</span>
              <i class="pi pi-star-fill text-2xl ml-4 text-yellow-500" v-if="selectedRecord.rol === 'Profesor Coordinador'"></i>
              <div class="text-500">{{this.selectedRecord.nombreAdicional}}</div>
              <div class="text-500">{{this.selectedRecord.correotec}}</div>
              <div class="flex align-items-center flex-wrap text-sm">
                <div class="mr-5">
                  <span class="font-medium text-500">Sede</span>
                  <div class="text-700 mt-2">{{ this.selectedRecord.sede }}</div>
                </div>
                <div class="">
                  <span class="font-medium text-500">Teléfono Personal</span>
                  <div class="text-700 mt-2">{{this.selectedRecord.telefono}}</div>
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

  <!--  VENTANA PARA AGREGAR UN ESTUDIANTE NUEVO-->
  <Dialog v-model:visible="this.addMode" header="Agregar Estudiantes" :modal="true" :maximizable="true" appendTo="self" :style="{ width: '52vw' }" :breakpoints="{ '960px': '75vw', '640px': '100vw' }">
    <AgregarEstudiante :sedes="this.sedes"/>
  </Dialog>


  <!--  VENTANA PARA EDITAR UN ESTUDIANTE EXISTENTE-->
  <Dialog v-model:visible="this.EditarDialog" header="Editar Información de Estudiante" :modal="true" :maximizable="true" appendTo="self" :style="{ width: '52vw' }" :breakpoints="{ '960px': '75vw', '640px': '100vw' }">
    <div class="surface-ground px-4 py-8 md:px-6 lg:px-8">
      <div class="p-fluid flex flex-column lg:flex-row">
        <div class="surface-card p-5 shadow-2 border-round flex-auto">
          <div class="text-900 font-semibold text-lg mt-3">Profile</div>
          <Divider></Divider>
          <div class="flex gap-5 flex-column-reverse md:flex-row">
            <div class="flex-auto p-fluid">
              <div class="mb-4">
                <label for="Carnet" class="block font-medium text-900 mb-2">Carnet</label>
                <InputNumber id="Carnet" type="number" :useGrouping="false" v-model.trim="this.carnet" disabled/>
              </div>
              <div class="mb-4">
                <label for="state" class="block font-medium text-900 mb-2">Nombre</label>
                <InputText id="state" type="text" v-model.trim="this.nombre"/>
              </div>
              <div class="mb-4">
                <label for="state" class="block font-medium text-900 mb-2">Apellido 1</label>
                <InputText id="state" type="text" v-model.trim="this.apellido1"/>
              </div>
              <div class="mb-4">
                <label for="state" class="block font-medium text-900 mb-2">Apellido 2</label>
                <InputText id="state" type="text" v-model.trim="this.apellido2"/>
              </div>
              <div class="mb-4">
                <label for="state" class="block font-medium text-900 mb-2">Nombre Adicional</label>
                <InputText id="state" type="text" v-model.trim="this.nombreadicional"/>
              </div>
              <div class="mb-4">
                <label for="sede" class="block font-medium text-900 mb-2">Sedes</label>
                <Dropdown v-model="this.sede" :options="this.sedes" optionValue="codigosede" optionLabel="codigosede" placeholder="Select" />
              </div>
              <div class="mb-4">
                <label for="state" class="block font-medium text-900 mb-2">Correo Institucional</label>
                <InputText id="state" type="text" v-model.trim="this.correotec" disabled/>
              </div>
              <div class="mb-4">
                <label for="state" class="block font-medium text-900 mb-2">Número Celular</label>
                <InputNumber id="state" type="number" :useGrouping="false" v-model.trim="this.telefono"/>
              </div>
              <div>
                <Button label="Guardar" class="w-auto mr-2" @click="this.modEstudiante()"></Button>
                <Button label="Cancelar" class="w-auto mr-2 p-button-danger" @click=this.close()></Button>
              </div>
            </div>
            <div class="flex flex-column align-items-center flex-or">
              <span class="font-medium text-900 mb-2">Foto</span>
              <FileUpload mode="basic" name="fotoProfe" chooseLabel="Subir" :auto="true" accept="image/*" :maxFileSize="1000000" :customUpload="true" @uploader="null" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </Dialog>

  <Dialog v-model:visible="this.agregarDialog" header="Agregar Estudiantes" :modal="true" :maximizable="true" appendTo="self" :style="{ width: '52vw' }" :breakpoints="{ '960px': '75vw', '640px': '100vw' }">
    <div class="flex flex-column align-items-center flex-or">
      <FileUpload align-items-center previewWidth="0" name="subirExcel" multiple="false"
                  mode="advanced" fileLimit="1"  accept=".xlsx" :customUpload="true"
                  @uploader="this.cargarExcel" chooseLabel="Escoger"
                  uploadLabel="Subir" cancelLabel="Cancelar"
                  invalidFileTypeMessage="{0}: Tipo de archivo invalido.">
      </FileUpload>
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
  width: 98vw;
  height: 84vh;
}

</style>
