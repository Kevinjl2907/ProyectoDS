<script setup>
import UserCard from './UserCard.vue';
import { ref, watch, onBeforeMount } from 'vue';

const props = defineProps({
    actividades: {
        type: Array,
        default: () => []
    }
});

const planes = ref([])
var firstPlanSelected = 'Seleccione un Plan'
const planActual = ref('')
var userImage = "/images/" + localStorage.imgUrl
const imgNotFound = 'images/notfound.png'
const nombreUsuario = localStorage.name;
const filteredActividades = ref([]);
const searchedActividad = ref('');
const emit = defineEmits(['change:active:actividad','change:active:plan']);

onBeforeMount(async () => {
    updatePicture();
    planes.value = await getPlanes();
    if(planes.value.length > 0){
        planActual.value = planes.value[0].semestre
        firstPlanSelected = planes.value[0].semestre
        onChangeActivePlan(planes.value[0])
    }
});
watch(
    () => props.actividades,
    (newActividades) => {
        filteredActividades.value = newActividades;
    },
    { immediate: true }
);

const getPlanes = async () => {
    var request = {
            method: 'GET',
            headers: { Authorization: localStorage.token } //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
        };
        var response = await fetch('https://main.d2anrgvy7s2j70.amplifyapp.com/PlanesTrabajoDisponibles/', request);
        var myJson = await response.json();
        return myJson.planes
};

const updatePicture = async () => {
    var request = {
        method: 'GET',
        headers: { Authorization: localStorage.token } //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
    };
    var response = await fetch('https://main.d2anrgvy7s2j70.amplifyapp.com/GetProfileImage/', request);
    var myJson = await response.json();
    localStorage.imgUrl = myJson.imgUrl
    userImage = "/images/" + myJson.imgUrl
    console.log(myJson.imgUrl)
}

const onChangeActiveUser = (user) => {
    emit('change:active:actividad', user);
};

const onChangeActivePlan = (plan) => {
    emit('change:active:plan', plan);
};

const filter = async () => {
    if (searchedActividad.value === '') {
        filteredActividades.value = props.actividades;
        return;
    }
    
    const filteredArr = filteredActividades.value.filter((actividad) => actividad.nombre.toLowerCase().includes(searchedActividad.value.toLowerCase()));

    filteredActividades.value = [...filteredArr];
};
</script>

