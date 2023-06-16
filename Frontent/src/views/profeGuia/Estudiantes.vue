<script>
import { FilterMatchMode, FilterOperator } from 'primevue/api';


// eslint-disable-next-line vue/no-export-in-script-setup
export default {
  name: "Estudiantes",
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
      // Variables utilizadas por la pantalla
      estudiantes: null,
      filters: {
        global: {value: null, matchMode: FilterMatchMode.CONTAINS},
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
  },
  async mounted() {
    this.clearFilter();
  },
  methods: {
    initFilters() {
      this.filters = {
        global: { value: null, matchMode: FilterMatchMode.CONTAINS },
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
      this.v$.$reset();
    },
    opendDialog(){
      this.EditarDialog = this.EditarDialog === true ? false : true
    },
    async getTableContents() {
      var request = {
            method: "GET",
            headers: {"Authorization": localStorage.token}, //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
        };
        var response = await fetch("https://main.d2anrgvy7s2j70.amplifyapp.com/ListaEstudiantes/", request)
        var myJson = await response.json()
        if (myJson.response === 'unsuccessful') {
            console.log('no exito')
        } else {
          this.estudiantes = myJson.estudiantes
          console.log(this.estudiantes)
        }
    },
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
            :loading="loading1"
            :filters="filters"
            responsiveLayout="scroll"
            :globalFilterFields="['identificacion','nombre', 'apellido1', 'apellido2', 'sede', 'correotec', 'telefono']"
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
                <Button type="button"  label="Restablecer" class="p-button-filled mr-2 mb-2" style="background-color: #468480; color: white;" @click="this.initFilters()" />
                <Button label="Mostrar Informacion" class="p-button mr-6 mb-2 p-button-warning" style="background-color: #468480; color: white; " @click="this.opendDialog()" />
                <Button label="Importar Excel" class="p-button mr-6 mb-2 p-button-warning" style="background-color: #468480; color: white; " @click="this.opendDialog()" />
                <Button v-tooltip.top="'Agrega un profesor al equipo de trabajo.'" label="Agregar Profesor" class="p-button-outlined mr-2 mb-2 p-button-success" v-show="isAssist" @click="this.openAddProfe2Team()" />
                <Button v-tooltip.top="'Agregar un nuevo profesor a la liste general de profesores.'" label="Registrar Profesor" class="p-button-outlined mr-2 mb-2 p-button-icon" v-show="isAssist" @click="this.opendDialog()" />
                <Button label="Dar de Baja" class="p-button-outlined mr-2 mb-2 p-button-danger" v-show="isAssist" @click="this.deleteItem()" />
                <Button label="Editar" class="p-button-outlined mr-4 mb-2"  v-show="isAssist" @click="this.opendDialog()" />
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
          <Column field="telefono" header="Telefono" :sortable="true" style="min-width: 12rem">
            <template #body="slotProps">
              {{ slotProps.data.telefono }}
            </template>
          </Column>
        </DataTable>
      </div>
    </div>
  </div>
  <Dialog v-model:visible="EditarDialog" :header="DialogHeader" :modal="true" :maximizable="true" appendTo="self" :style="{ width: '52vw' }" :breakpoints="{ '960px': '75vw', '640px': '100vw' }">

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
