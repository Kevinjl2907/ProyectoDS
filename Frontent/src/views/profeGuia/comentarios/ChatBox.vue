<script setup>
import { ref } from 'vue';
import { useLayout } from '@/layout/composables/layout';

const { contextPath } = useLayout();
const props = defineProps({
    actividad: {
        type: Object,
        required: true,
        default: null
    }
});

//const imgNotFound = 'images/notfound.png'
const nombreActual = localStorage.name
const emit = defineEmits(['send:message']);
const op = ref(null);
const textContent = ref('');


const parseDate = (timestamp) => {
    var fechaObjeto= new Date(timestamp)
    return (fechaObjeto.toString().split("GMT")[0]);
};

const sendMessage = () => {
    if (textContent.value == '' || textContent.value === ' ' || props.actividad.idactividad == undefined) {
        return;
    }
    let message = {
        contenido: textContent.value,
        fecha: new Date().getTime(),
        autor: {
            nombre: localStorage.name,
            foto: ''
        }
    };

    emit('send:message', message);
    textContent.value = '';
};
</script>

<template>
    <div class="flex flex-column h-full">
        <div class="flex align-items-center border-bottom-1 surface-border p-3 lg:p-6">
            <div class="mr-2">
                <span class="text-900 font-semibold block">{{ actividad.nombre }}</span>
            </div>
        </div>
        <div class="user-message-container p-3 md:px-4 lg:px-6 lg:py-4 my-auto overflow-y-auto" style="max-height: 53vh">
            <div v-for="comentario in actividad.comentarios" :key="comentario">
                <div v-if="comentario.autor.nombre !== nombreActual" class="grid grid-nogutter mb-4">
                    <div class="mr-3 mt-1">
                        <img :src="'/images/' + comentario.autor.foto" @error="$event.target.src=imgNotFound" :alt="NaN" class="w-3rem h-3rem border-circle shadow-4" />
                    </div>
                    <div class="col mt-3">
                        <p class="text-900 font-semibold mb-3">{{ comentario.autor.nombre }}</p>
                        <span class="text-700 inline-block font-medium border-1 surface-border p-3 white-space-normal border-round" style="word-break: break-word; max-width: 80%">{{ comentario.contenido }}</span>
                        <p class="text-700 mt-3">{{ parseDate(comentario.fecha) }}</p>
                    </div>
                </div>

                <div v-if="comentario.autor.nombre === nombreActual" class="grid grid-nogutter mb-4">
                    <div class="col mt-3 text-right">
                        <span class="inline-block text-left font-medium border-1 surface-border bg-primary-100 text-primary-900 p-3 white-space-normal border-round" style="word-break: break-word; max-width: 80%">{{ comentario.contenido }}</span>
                        <p class="text-700 mt-3">{{ parseDate(comentario.fecha) }}</p>
                    </div>
                </div>
            </div>
        </div>
        <div class="p-3 md:p-4 lg:p-6 flex flex-column sm:flex-row align-items-center border-top-1 surface-border gap-3">
            <InputText id="message" type="text" placeholder="Type a message" class="flex-1 w-full sm:w-auto border-round" v-model="textContent" @keydown.enter="sendMessage()" />
            <div class="flex w-full sm:w-auto gap-3">
                <Button label="Enviar"  class="w-full sm:w-auto" style="background-color: #468480; color: white;" @click="sendMessage()"></Button>
            </div>
        </div>
    </div>
</template>
