<script setup>
const props = defineProps({
    actividad: {
        type: Object,
        required: true
    }
});
//console.log(props.actividad)
</script>

<template>
    <div class="flex flex-nowrap justify-content-between align-items-center border-1 surface-border border-round p-3 cursor-pointer select-none hover:surface-hover transition-colors transition-duration-150" tabindex="0">
        <div class="flex align-items-center">
            <div class="relative md:mr-3">
                <i class="pi pi-briefcase" style="font-size: 2rem"></i>
            </div>
            <div class="flex-column hidden md:flex">
                <span class="text-900 font-semibold block">{{ actividad.nombre }}</span>
            </div>
        </div>
    </div>
</template>
