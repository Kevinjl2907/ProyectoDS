<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const navigate1 = () => {
    router.push({ name: 'Landing' });
};

const navigate2 = () => {
  router.push({ name: 'Administrar Plan de Trabajo' });
};

const navigate3 = () => {
    router.push({ name: 'Landing' });
};

const navigateToEstudiantes = () => {
  console.log("Se ha hecho clic en el botón 'Estudiantes'");
  router.push({ name:'Estudiantes'});
};

const navigate5 = () => {
    router.push({ name: 'Landing' });
};

</script>

<template>

  <div >
    <div class="button-container">
      <Button label="Gestionar Personal" class="button"></Button>
      <Button label="Plan de trabajo" class="button" @click="navigate2" ></Button>
      <Button label="Consultas" class="button" ></Button>
      <Button label="Estudiantes" class="button" @click="navigateToEstudiantes"></Button>
      <Button label="Equipo de trabajo" class="button"></Button>
    </div>
  </div>
</template>

<style>

.button-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  
}

.button {
  width: 200px; 
  height: 60px;
  margin-bottom: 10px;
  background-color: #856845;
}

</style>