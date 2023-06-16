<script setup>
import { ref, nextTick, onMounted, onBeforeMount } from 'vue';
import ChatBox from './ChatBox.vue';
import ChatSidebar from './ChatSidebar.vue';
import { useLayout } from '@/layout/composables/layout';

const { contextPath } = useLayout();

var planTrabajoSelec = ''
const activeActividadId = ref(1);
const actividades = ref([]);
/*
onBeforeMount(async () => {
    actividades.value = await comentariosRequest()
    activeActividadId.value = actividades.value[0].idactividad
    scrollToLastMessage();
});*/

const changeActiveActividad = (actividad) => {
    activeActividadId.value = actividad.idactividad;
    scrollToLastMessage();
};

const changeActivePlan = async (plan) => {
    //console.log(plan)
    planTrabajoSelec = plan.semestre;
    actividades.value = await comentariosRequest()
    if(actividades.value.length > 0){
        activeActividadId.value = actividades.value[0].idactividad
    }
    scrollToLastMessage();
};

const sendMessage = async (message) => {
    const activeActividad= findActiveActividad();
    activeActividad.comentarios.push(message);
    await enviarComentarioRequest(message,activeActividad.idactividad)
    actividades.value = await comentariosRequest()
    scrollToLastMessage();
};

const findActiveActividad = () => {
    //console.log(actividades.value)
    return actividades.value.find((actividad) => actividad.idactividad === activeActividadId.value) || {};
};

const scrollToLastMessage = async () => {
    const element = document.querySelector('.user-message-container');

    await nextTick(() => {
        element.scroll({ top: element.scrollHeight });
    });
};

const comentariosRequest = async () =>  {
    
    var request = {
        method: "POST",
        headers: {"content-Type": "application/json",
                  "Authorization": localStorage.token}, //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
        body: JSON.stringify({ planTrabajo : planTrabajoSelec })
    };

    var response = await fetch("https://main.d2anrgvy7s2j70.amplifyapp.com/ObtenerComentarios/", request);
    var myJson = await response.json();
    return myJson.actividades
};

const enviarComentarioRequest = async (mensaje,idactividad) =>  {
    var request = {
        method: "POST",
        headers: {"content-Type": "application/json",
                  "Authorization": localStorage.token}, //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
        body: JSON.stringify({ idactividad : idactividad, 
                               comentario: mensaje})
    };

    var response = await fetch("https://main.d2anrgvy7s2j70.amplifyapp.com/EnviarComentarios/", request);
    var myJson = await response.json();
    //console.log(myJson)
};

</script>


<template>
    <div class="flex flex-column md:flex-row gap-5" style="min-height: 81vh">

        <div class="flex-1 border-1 surface-border surface-card border-round">
            <chat-box @send:message="sendMessage" :actividad="findActiveActividad()"></chat-box>
        </div>
    </div>
</template>
