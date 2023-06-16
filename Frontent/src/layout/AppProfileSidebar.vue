<script setup>
import { useLayout } from '@/layout/composables/layout';
import { useRouter } from 'vue-router';

const { layoutState } = useLayout();

const router = useRouter();
const nombre = localStorage.name

const navigateToLogin = () => {
    router.push({ name: 'Login' });
};
const logoutRequest = async () => {
    var request = {
        method: "GET",
        headers: {"content-Type": "application/json",
                  "Authorization": localStorage.token}, //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
    };
    var response = await fetch("https://main.d2anrgvy7s2j70.amplifyapp.com/logout/", request)

    var myJson = await response.json()
    if (myJson.response === 'unsuccessful') {
        this.$swal.fire({
            position: 'top-center',
            icon: 'error',
            title: 'Error',
            text: 'Ha ocurrido un error',
            showConfirmButton: true
        });
    } else {
        layoutState.profileSidebarVisible.value = false
        navigateToLogin()
    }
};

</script>

<template>
    <Sidebar v-model:visible="layoutState.profileSidebarVisible.value" position="right" class="layout-profile-sidebar w-full sm:w-25rem">
        <div class="flex flex-column mx-auto md:mx-0">
            <span class="mb-2 font-semibold">Bienvenido</span>
            <span class="text-color-secondary font-medium mb-5">{{ nombre }}</span>

            <ul class="list-none m-0 p-0">
                <li>
                    <a class="cursor-pointer flex surface-border mb-3 p-3 align-items-center border-1 surface-border border-round hover:surface-hover transition-colors transition-duration-150" @click="logoutRequest">
                        <span>
                            <i class="pi pi-power-off text-xl text-primary"></i>
                        </span>
                        <div class="ml-3">
                            <span class="mb-2 font-semibold">Sign Out</span>
                            <p class="text-color-secondary m-0">¡Nos vemos, hasta pronto!</p>
                        </div>
                    </a>
                </li>
            </ul>
        </div>
    </Sidebar>
</template>
