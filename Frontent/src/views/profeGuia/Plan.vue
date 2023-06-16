<script>
import FullCalendar from '@fullcalendar/vue3';
import dayGridPlugin from '@fullcalendar/daygrid';
import interactionPlugin from '@fullcalendar/interaction';
import config from "../../service/Config";

export default {
    components: {
        FullCalendar // make the <FullCalendar> tag available
    },
    created() {
        this.buscarActividades();
    },
    data() {
        return {
            singleEvent: { title: '', date: '' },
            allEvents: null,
            closestEvent: null,
            openNextEventDialog: false,
            calendarOptions: {
                plugins: [dayGridPlugin, interactionPlugin],
                initialView: 'dayGridMonth',
                dateClick: this.handleDateClick,
                events: []
            }
        };
    },
    methods: {
        handleDateClick: function (arg) {
            alert('date click! ' + arg.dateStr);
        },
        async buscarActividades() {
            //this.bodyActividad.planTrabajo = this.currentPlanTrabajo.semestre;
            var request = {
                method: 'GET',
                headers: { Authorization: localStorage.token},
            };
            var response = await fetch('https://main.d2anrgvy7s2j70.amplifyapp.com/ObtenerAActividades/', request);
            var myJson = await response.json();
            if (myJson.response === 'unsuccessful') {
              this.$swal.fire({
                position: "top-center",
                icon: "warning",
                title: "Error",
                text: "Ha ocurrido un error",
                showConfirmButton: true,
                timer: config.globales.timer_errores,
              });
            } else {
                this.allEvents = myJson.actividades;
                this.transformData();
                this.findClosestEvent();
            }
        },
        transformData() {
            let singleEvent;
            this.findClosestEvent();
            for (const event in this.allEvents) {
                if (this.closestEvent === this.allEvents[event]) {
                    singleEvent = { title: this.allEvents[event].nombre, date: this.allEvents[event].fecha, backgroundColor: 'red' };
                    this.calendarOptions.events.push(singleEvent);
                } else {
                    singleEvent = { title: this.allEvents[event].nombre, date: this.allEvents[event].fecha, backgroundColor: 'black' };
                    this.calendarOptions.events.push(singleEvent);
                }
            }
        },

        findClosestEvent() {
            const today = new Date();
            let closestDate = Infinity;
            let closestEvent = null;

            for (const event of this.allEvents) {
                const eventDate = new Date(event.fecha);

                if (eventDate >= today && eventDate < closestDate) {
                    closestDate = eventDate;
                    closestEvent = event;
                }
            }
            this.closestEvent = closestEvent;
        },
        opendDialog() {
            this.openNextEventDialog = this.openNextEventDialog === true ? false : true;
        }
    }
};
</script>
<template>
    <div class="grid format">
        <div class="col-12">
            <div class="card demo-app-main">
                <h5>Calendario de Actividades</h5>
                <Button label="Ver Proxima Actividad" class="p-button-outlined mr-2 mb-2" @click="this.opendDialog()" />
                <div class="calendar-container">
                    <FullCalendar :options="calendarOptions" class="calendarContainer" />
                </div>
            </div>
        </div>
    </div>
    <Dialog v-model:visible="openNextEventDialog" :header="'Proxima Actividad'" :modal="true" :maximizable="true" appendTo="self" :style="{ width: '52vw' }" :breakpoints="{ '960px': '75vw', '640px': '100vw' }">
        <div class="surface-section">
            <ul class="list-none p-0 m-0">
                <li class="flex align-items-center py-3 px-2 border-top-1 surface-border flex-wrap">
                    <div class="text-500 w-6 md:w-2 font-medium">Nombre</div>
                    <div class="text-900 w-full md:w-8 md:flex-order-0 flex-order-1 pl-8">{{ this.closestEvent.nombre }}</div>
                    <div class="w-6 md:w-2 flex justify-content-end"></div>
                </li>
                <li class="flex align-items-center py-3 px-2 border-top-1 surface-border flex-wrap">
                    <div class="text-500 w-6 md:w-2 font-medium">Plan de trabajo</div>
                    <div class="text-900 w-full md:w-8 md:flex-order-0 flex-order-1 pl-8">{{ this.closestEvent.planTrabajo }}</div>
                    <div class="w-6 md:w-2 flex justify-content-end"></div>
                </li>
                <li class="flex align-items-end py-3 px-2 border-top-1 surface-border flex-wrap">
                    <div class="text-500 w-6 md:w-2 font-medium">Fecha</div>
                    <div class="text-900 w-full md:w-8 md:flex-order-0 flex-order-1 pl-8">{{ new Date(this.closestEvent.fecha).toLocaleString('es-ES') }}</div>
                    <div class="w-6 md:w-2 flex justify-content-end"></div>
                </li>
                <li class="flex align-items-center py-3 px-2 border-top-1 surface-border flex-wrap">
                    <div class="text-500 w-6 md:w-2 font-medium">Tipo de Actividad</div>
                    <div class="text-900 w-full md:w-8 md:flex-order-0 flex-order-1 pl-8">{{ this.closestEvent.tipo }}</div>
                </li>
                <li class="align-items py-3 px-2 border-top-1 surface-border">
                  <div class="responsables-container">
                    <div class="responsables-label text-500">Responsables</div>
                    <div class="responsables-list">
                      <div v-for="(responsable, i) in this.closestEvent.responsables" :key="i" class="text-900">
                        {{responsable}}
                      </div>
                    </div>
                  </div>
                </li>
                <li class="flex align-items-center py-3 px-2 border-top-1 surface-border flex-wrap">
                    <div class="text-500 w-6 md:w-2 font-medium">Modalidad</div>
                    <Chip v-show="this.closestEvent.esvirtual" :label="'VIRTUAL'" class="mr-2 ml-8"></Chip>
                    <Chip v-show="!this.closestEvent.esvirtual" :label="'PRESENCIAL'" class="mr-2 ml-8"></Chip>
                </li>
                <li v-if="this.closestEvent.esvirtual" class="flex align-items-center py-3 px-2 border-top-1 surface-border flex-wrap">
                    <div class="text-500 w-6 md:w-2 font-medium">enlace</div>
                    <div class="text-900 w-full md:w-8 md:flex-order-0 flex-order-1 pl-8">{{ this.closestEvent.enlace }}</div>
                    <div class="w-6 md:w-2 flex justify-content-end"></div>
                </li>
                <li class="flex align-items-center py-3 px-2 border-top-1 border-bottom-1 surface-border flex-wrap">
                    <div class="text-500 w-6 md:w-2 font-medium">Estado</div>
                    <div class="text-900 w-full md:w-8 md:flex-order-0 flex-order-1 line-height-3 pl-8">
                        {{ this.closestEvent.estado }}
                    </div>
                </li>
                <li class="flex text-align py-3 px-2 border-top-1 border-bottom-1 surface-border flex-wrap">
                    <img class="centerImg" v-bind:src="'/images/' + this.closestEvent.afiche" height="300" @error="$event.target.src='/images/imgnotfound.png'">
                </li>
            </ul>
        </div>
    </Dialog>
</template>

<style scoped>
.highlighted-event {
    background-color: red;
    color: white;
}

.calendarContainer {
    padding: 10px;
    border-radius: 5px;
    min-height: 50rem;
    max-height: 50rem;
}
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
