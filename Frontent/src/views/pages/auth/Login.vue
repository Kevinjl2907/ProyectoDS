<script setup>
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useLayout } from '@/layout/composables/layout';
import AppConfig from '@/layout/AppConfig.vue';
import Swal from 'sweetalert2'

const correoprueba = ref('jimenezkevin@itcr.ac.cr')
const contraprueba = ref('12345')
const router = useRouter();
const rememberMe = ref(false);
const { layoutConfig } = useLayout();
const darkMode = computed(() => {
    return layoutConfig.colorScheme.value !== 'light';
});

let disableButton = false;
let disableTestClick = false

const navigateToDashboard = () => {
    router.push({ name: 'Inicio' });
};

const navigateToNewPassword = () => {
  router.push({ name: 'newpassword' });
};

const loginRequest = async () =>  {
    var request = {
        method: "POST",
        headers: {"content-Type": "application/json",
                  "Authorization": ""}, //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
        body: JSON.stringify({ username : correoprueba['_rawValue'], 
                               password : contraprueba['_rawValue'],})
    };
    disableButton = true;
    var response = await fetch("http://127.0.0.1:8000/login/", request)
        //.then(response => response.json())
        //.then(data => token=data)
        //.catch(error => console.error(error));
    var myJson = await response.json()
    if (myJson.response === 'unsuccessful') {
        router.push({ name: 'error' })
    } else {
        localStorage.token = "Token " + myJson.token;
        localStorage.type = myJson.type;//myJson.type;
        localStorage.sede = myJson.sede;
        localStorage.name = myJson.name;
        localStorage.imgUrl = myJson.imgUrl;
        localStorage.codigo = myJson.codigo;
        navigateToDashboard()
    }
};

const resetPassRequest = async () =>  {
    if(disableTestClick) {
        return
    } 
    disableTestClick = true
    Swal.fire({
        title: "Cargando...",
        html: "Espere un momento porfavor"
    })
    Swal.showLoading()
    var request = {
        method: "POST",
        headers: {"content-Type": "application/json",
                  "Authorization": ""}, //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
        body: JSON.stringify({ username : correoprueba['_rawValue']})
    };
    
    var response = await fetch("http://127.0.0.1:8000/reset/", request)
    var myJson = await response.json()
    Swal.hideLoading()
    console.log(myJson)
    if(myJson['response'] == 'successful'){
        await Swal.fire({
            position: "top-center",
            icon: "success",
            title: "Enhorabuena",
            text: "Revisa tu correo para verificar",
            showConfirmButton: true,
        });
        disableTestClick = false
    } else {
        await Swal.fire({
            position: "top-center",
            icon: "warning",
            title: "Error",
            text: "El usuario no existe o no esta activo",
            showConfirmButton: true,
        });
        disableTestClick = false
    }
};
</script>

<template>
    <label style="width: 1800; height: 80px; background: #468480; position: absolute; color: #468480; text-align: left;"></label>
    <div class="px-5 min-h-screen flex justify-content-center align-items-center">
        <div class="border-1 border-round py-7 px-4 md:px-7 z-1" style="background-color: #468480;">
            <div class="mb-4" style="background-color: #468480; ">
                <div class="text-xl" style="text-align: center; background-color: #468480; color: #FFFFFF;">Inicio de Sesión</div>
            </div>
            <div class="flex flex-column" style="background-color: #468480;">
                <span class="p-input-icon-left w-full mb-4">
                    <i class="pi pi-envelope"></i>
                    <InputText id="email" v-model="correoprueba" type="text" class="w-full md:w-25rem" placeholder="Email" />
                </span>
                <span class="p-input-icon-left w-full mb-4">
                    <i class="pi pi-lock"></i>
                    <InputText id="password" v-model="contraprueba" type="password" class="w-full md:w-25rem" placeholder="Contraseña" />
                </span>
                <div class="mb-4 flex flex-wrap gap-3" style="background-color: #468480;">
                    <a class=" cursor-pointer hover:text-primary cursor-pointer ml-auto transition-colors transition-duration-300" @click="resetPassRequest" style="color: #FFFFFF;">Reiniciar Contraseña</a>
                </div>
                <Button label="Ingresar" class="w-full" @click="loginRequest" :disabled="disableButton" style="background-color: #856845;"></Button>
            </div>
        </div>
    </div>
    <AppConfig simple />
</template>
