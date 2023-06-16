<script>

import Listbox from 'primevue/listbox';
export default {
  data() {
    return {
      planesTrabajo: null,
      currentPlanTrabajo: null,
      currentActividades: null,
      currentActividad: null,
      isVisible: false,
      verDetalle: false,
    };
  },
  mounted() {
    this.getPlanesTrabajo()
  },
  methods: {
    async getPlanesTrabajo() {
      var request = {
        method: 'GET',
        headers: { Authorization: localStorage.token } //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
      };
      var response = await fetch('http://127.0.0.1:8000/PlanesTrabajoCompletos/', request);
      var myJson = await response.json();
      if (myJson.response === 'unsuccessful') {
        console.log('no exito');
      } else {
        console.log(myJson);
        this.planesTrabajo = myJson.planes;
      }
    },
    async buscarActividades() {
        console.log("si")
        this.currentActividades = this.currentPlanTrabajo.actividades
        this.isVisible = true
        console.log(this.currentActividades)
    },
    changeDialogState() {
      this.verDetalle = this.verDetalle === true ? false : true
    },

  }
};
</script>

<template>
  <div class="card flex flex-column">
    <div class="flex flex-wrap gap-2 mb-4">
      <label class="font-medium w-full">Planes de Trabajo</label>
      <Dropdown v-model="this.currentPlanTrabajo" @change="this.buscarActividades()" :options="this.planesTrabajo" optionLabel="semestre" placeholder="Plan de trabajo" class="w-full">
        <template #option="slotProps">
          <div class="flex align-items-center">
            <div>{{ slotProps.option.semestre }}</div>
          </div>
        </template>
      </Dropdown>
    </div>
    <div class="card flex">
      <div v-if="this.isVisible">
        <ul class="list-none p-0 m-0 w-17rem">
            <li class="flex align-items-center py-3 px-2 border-top-1 surface-border flex-wrap">
                <div class="text-500 w-6 md:w-6 font-medium">Semestre</div>
                <div class="text-900">{{ this.currentPlanTrabajo.semestre }}</div>
                <div class="w-6 md:w-2 flex justify-content-end"></div>
            </li>
            <li class="flex align-items-center py-3 px-2 border-top-1 surface-border flex-wrap">
                <div class="text-500 w-6 md:w-6 font-medium">Semana Inicial</div>
                <div class="text-900">{{ this.currentPlanTrabajo.semanainicial }}</div>
                <div class="w-6 md:w-2 flex justify-content-end"></div>
            </li>
            <li class="flex align-items-end py-3 px-2 border-top-1 surface-border flex-wrap">
                <div class="text-500 w-6 md:w-6 font-medium">Semana Final</div>
                <div class="text-900">{{ this.currentPlanTrabajo.semanafinal }}</div>
                <div class="w-6 md:w-2 flex justify-content-end"></div>
            </li>
            <li class="flex align-items-center py-3 px-2 border-top-1 surface-border flex-wrap">
                <div class="text-500 text-center font-medium">Semanas de vacaciones</div>
                <Listbox :options="this.currentPlanTrabajo.semanas" emptyMessage="No hay vacaciones" class="w-full" listStyle="max-height:165px"/>
            </li>
        </ul>
      </div>
      <Divider v-if="this.isVisible" layout="vertical" />
      <div class="w-full">
      <DataTable
            v-if="this.isVisible"
            :value="this.currentActividades"
            class="p-datatable-gridlines"
            :rows="5"
            :rowHover="true"
            filterDisplay="menu"
            responsiveLayout="scroll"
            v-model:selection="this.currentActividad"
            :sorteable="true"
            :resizableColumns="true"
            :autoLayout="true"
            selectionMode="single"
            :scrollable="true"
            scrollHeight="flex"
            paginator
            @update:selection="this.changeDialogState()"
        >
          <template #empty> No hay información disponible </template>
          <template #loading> Cargando, por favor espere. </template>
          <Column field="nombre" header="Nombre" :sortable="true" style="min-width: 12rem"/>
          <Column field="fecha" header="Fecha" :sortable="true" style="min-width: 12rem">
            <template #body="slotProps">
              {{ new Date(slotProps.data.fecha).toLocaleString('es-ES') }}
            </template>
          </Column>
          <Column field="tipo" header="tipo" :sortable="true" style="min-width: 12rem"/>
      </DataTable>
      </div>
    </div>
  </div>
  <Dialog v-model:visible="verDetalle" :header="'Detalle de actividad'" :modal="true" :maximizable="true" appendTo="self" :style="{ width: '52vw' }" :breakpoints="{ '960px': '75vw', '640px': '100vw' }">
        <div class="surface-section">
            <ul class="list-none p-0 m-0">
                <li class="flex align-items-center py-3 px-2 border-top-1 surface-border flex-wrap">
                    <div class="text-500 w-6 md:w-2 font-medium">Nombre</div>
                    <div class="text-900 w-full md:w-8 md:flex-order-0 flex-order-1 pl-8">{{ this.currentActividad.nombre }}</div>
                    <div class="w-6 md:w-2 flex justify-content-end"></div>
                </li>
                <li class="flex align-items-center py-3 px-2 border-top-1 surface-border flex-wrap">
                    <div class="text-500 w-6 md:w-2 font-medium">Plan de trabajo</div>
                    <div class="text-900 w-full md:w-8 md:flex-order-0 flex-order-1 pl-8">{{ this.currentActividad.planTrabajo }}</div>
                    <div class="w-6 md:w-2 flex justify-content-end"></div>
                </li>
                <li class="flex align-items-end py-3 px-2 border-top-1 surface-border flex-wrap">
                    <div class="text-500 w-6 md:w-2 font-medium">Fecha</div>
                    <div class="text-900 w-full md:w-8 md:flex-order-0 flex-order-1 pl-8">{{ new Date(this.currentActividad.fecha).toLocaleString('es-ES') }}</div>
                    <div class="w-6 md:w-2 flex justify-content-end"></div>
                </li>
                <li class="flex align-items-end py-3 px-2 border-top-1 surface-border flex-wrap">
                    <div class="text-500 w-6 md:w-2 font-medium">Fecha de Publicacion</div>
                    <div class="text-900 w-full md:w-8 md:flex-order-0 flex-order-1 pl-8">{{ new Date(this.currentActividad.fechaPublicacion).toLocaleString('es-ES') }}</div>
                    <div class="w-6 md:w-2 flex justify-content-end"></div>
                </li>
                <li class="flex align-items-center py-3 px-2 border-top-1 surface-border flex-wrap">
                    <div class="text-500 w-6 md:w-2 font-medium">Tipo de Actividad</div>
                    <div class="text-900 w-full md:w-8 md:flex-order-0 flex-order-1 pl-8">{{ this.currentActividad.tipo }}</div>
                </li>
                <li class="align-items py-3 px-2 border-top-1 surface-border">
                  <div class="responsables-container">
                    <div class="responsables-label text-500">Responsables</div>
                    <div class="responsables-list">
                      <div v-for="(responsable, i) in this.currentActividad.responsables" :key="i" class="text-900">
                        {{responsable}}
                      </div>
                    </div>
                  </div>
                </li>
                <li class="flex align-items-center py-3 px-2 border-top-1 surface-border flex-wrap">
                    <div class="text-500 w-6 md:w-2 font-medium">Modalidad</div>
                    <Chip v-show="this.currentActividad.esvirtual" :label="'VIRTUAL'" class="mr-2 ml-8"></Chip>
                    <Chip v-show="!this.currentActividad.esvirtual" :label="'PRESENCIAL'" class="mr-2 ml-8"></Chip>
                </li>
                <li v-if="this.currentActividad.esvirtual" class="flex align-items-center py-3 px-2 border-top-1 surface-border flex-wrap">
                    <div class="text-500 w-6 md:w-2 font-medium">enlace</div>
                    <div class="text-900 w-full md:w-8 md:flex-order-0 flex-order-1 pl-8">{{ this.currentActividad.enlace }}</div>
                    <div class="w-6 md:w-2 flex justify-content-end"></div>
                </li>
                <li class="flex align-items-center py-3 px-2 border-top-1 border-bottom-1 surface-border flex-wrap">
                    <div class="text-500 w-6 md:w-2 font-medium">Estado</div>
                    <div class="text-900 w-full md:w-8 md:flex-order-0 flex-order-1 line-height-3 pl-8">
                        {{ this.currentActividad.estado }}
                    </div>
                </li>
                <li class="flex text-align py-3 px-2 border-top-1 border-bottom-1 surface-border flex-wrap">
                    <img class="centerImg" v-bind:src="'/images/' + this.currentActividad.afiche" height="300" @error="$event.target.src='/images/imgnotfound.png'">
                </li>
            </ul>
        </div>
    </Dialog>
</template>

<style scoped>
.centerImg {
  display: block;
  margin-left: auto;
  margin-right: auto;
}
.responsables-container {
  display: flex;
  align-items: flex-start;
}

.responsables-label {
  font-weight: 500;
  margin-right: 8.8rem; /* Ajusta el espacio entre "Responsables" y la lista */
}

.responsables-list {
  display: flex;
  flex-direction: column; /* Cambia la dirección de los elementos a vertical */
  gap: 0.1rem; /* Ajusta el espacio entre los responsables */
}
/**{
  border: 1px solid red;
}*/
</style>