<script setup>
import { ref } from 'vue';

import AppSubMenu from './AppSubMenu.vue';

const menuUser = localStorage.type;
let model = null;


const profesorGuiaMenu = [
      {
        label: 'Equipo Guia',
        icon: 'pi pi-fw pi-sitemap',
        to: '/equipoGuia'
      },
      {
        label: 'Estudiantes',
        icon: 'pi pi-fw pi-users',
        to: '/modificarEstudiante'
      },
      {
        label: 'Generar Excel',
        icon: 'pi pi-fw pi-file-excel',
        to: '/exportarExcel'
      },
      {
        label: 'Comentarios',
        icon: 'pi pi-fw pi-comments',
        to: '/comentarios'
      },
      {
        label: 'Plan de Trabajo',
        icon: 'pi pi-fw pi-calendar',
        to: '/planTrabajoProfe'
      }]

const profesorCoordinador = [
  {
    label: 'Equipo Guia',
    icon: 'pi pi-fw pi-sitemap',
    to: '/equipoGuia'
  },
  /*{
    label: 'Estudiantes',
    icon: 'pi pi-fw pi-users',
    to: '/estudiantes'
  },*/
  {
    label: 'Estudiantes',
    icon: 'pi pi-fw pi-users',
    to: '/modificarEstudiante'
  },
  {
    label: 'Generar Excel',
    icon: 'pi pi-fw pi-file-excel',
    to: '/exportarExcel'
  },
  {
    label: 'Comentarios',
    icon: 'pi pi-fw pi-comments',
    to: '/comentarios'
  },
  {
    label: 'Plan de Trabajo',
    icon: 'pi pi-fw pi-calendar',
    to: '/planTrabajoProfe'
  },
  {
    label: 'Administrar Plan de Trabajo',
    icon: 'pi pi-fw pi-cog',
    to: '/admin-planTrabajo'
  },
  {
    label: 'Administrar Actividades',
    icon: 'pi pi-fw pi-tags',
    to: '/admin-actividades'
  }
]

const asistenteAdministrativa = [
      {
        label: 'Equipo de Trabajo',
        icon: 'pi pi-fw pi-sitemap',
        to: '/equipoGuia'
      },
      {
        label: 'Estudiantes',
        icon: 'pi pi-fw pi-users',
        to: '/modificarEstudiante'
      },
      {
        label: 'Generar Excel',
        icon: 'pi pi-fw pi-file-excel',
        to: '/exportarExcel'
      },
      {
        label: 'Plan de Trabajo',
        icon: 'pi pi-fw pi-calendar',
        to: '/planTrabajo'
      }
        ]


if (menuUser === 'asist'){
  model = ref(asistenteAdministrativa);
}

if (menuUser === 'PG'){
  model = ref(profesorGuiaMenu);
}

if (menuUser === 'PGC'){
  model = ref(profesorCoordinador);
}


</script>

<template>
    <AppSubMenu :model="model" />
</template>

<style lang="scss" scoped></style>
