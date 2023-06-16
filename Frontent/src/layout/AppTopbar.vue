<script setup>
import AppBreadcrumb from './AppBreadcrumb.vue';
import { ref, onMounted, onBeforeUnmount, onUpdated } from 'vue';
import { useLayout } from '@/layout/composables/layout';
const { onMenuToggle, onProfileSidebarToggle } = useLayout();

const outsideClickListener = ref(null);
const topbarMenuActive = ref(false);

//const userImage = "/images/" + localStorage.imgUrl

onMounted(() => {
    bindOutsideClickListener();
});

onBeforeUnmount(() => {
    unbindOutsideClickListener();
});

onUpdated(() => {
    updatePicture()
})

const updatePicture = async () => {
    var request = {
        method: 'GET',
        headers: { Authorization: localStorage.token } //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
    };
    var response = await fetch('https://main.d2anrgvy7s2j70.amplifyapp.com/GetProfileImage/', request);
    var myJson = await response.json();
    localStorage.imgUrl = myJson.imgUrl
    //userImage = "/images/" + myJson.imgUrl
}


const bindOutsideClickListener = () => {
    if (!outsideClickListener.value) {
        outsideClickListener.value = (event) => {
            if (isOutsideClicked(event)) {
                topbarMenuActive.value = false;
            }
        };
        document.addEventListener('click', outsideClickListener.value);
    }
};
const unbindOutsideClickListener = () => {
    if (outsideClickListener.value) {
        document.removeEventListener('click', outsideClickListener);
        outsideClickListener.value = null;
    }
};
const isOutsideClicked = (event) => {
    if (!topbarMenuActive.value) return;

    const sidebarEl = document.querySelector('.layout-topbar-menu');
    const topbarEl = document.querySelector('.layout-topbar-menu-button');

    return !(sidebarEl.isSameNode(event.target) || sidebarEl.contains(event.target) || topbarEl.isSameNode(event.target) || topbarEl.contains(event.target));
};

const showProfileSidebar = () => {
    onProfileSidebarToggle();
};
</script>

<template>
    <div class="layout-topbar" >
        <div class="topbar-start">
            <AppBreadcrumb class="topbar-breadcrumb" ></AppBreadcrumb>
        </div>
        <div class="topbar-end">
            
        </div>
    </div>
</template>

<style lang="scss" scoped></style>
