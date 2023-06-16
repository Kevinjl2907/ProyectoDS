<script>
export default {
  name: "AgregarEstudiante",
  props: ['sedes'],

  data(){
    return{
      sedeSeleccionada: null,
    }
  }
}
</script>


<template>

  <div class="surface-ground px-4 py-8 md:px-6 lg:px-8">
    <div class="p-fluid flex flex-column lg:flex-row">
      <div class="surface-card p-5 shadow-2 border-round flex-auto">
        <div class="text-900 font-semibold text-lg mt-3">Profile</div>
        <Divider></Divider>
        <div class="flex gap-5 flex-column-reverse md:flex-row">
          <div class="flex-auto p-fluid">
            <div class="mb-4">
              <label for="ID" class="block font-medium text-900 mb-2">ID</label>
              <InputNumber id="ID" type="number" disabled/>
            </div>
            <div class="mb-4">
              <label for="state" class="block font-medium text-900 mb-2">Nombre</label>
              <InputText id="state" type="text" />
            </div>
            <div class="mb-4">
              <label for="state" class="block font-medium text-900 mb-2">Apellido 1</label>
              <InputText id="state" type="text" />
            </div>
            <div class="mb-4">
              <label for="state" class="block font-medium text-900 mb-2">Apellido 2</label>
              <InputText id="state" type="text" />
            </div>
            <div class="mb-4">
              <label for="state" class="block font-medium text-900 mb-2">Nombre Adicional</label>
              <InputText id="state" type="text" />
            </div>
            <div class="mb-4">
              <label for="state" class="block font-medium text-900 mb-2">Sedes</label>
              <Dropdown v-model="this.sedeSeleccionada" :options="this.$props.sedes.codigo" optionLabel="nombres" placeholder="Select" />
            </div>
            <div class="mb-4">
              <label for="state" class="block font-medium text-900 mb-2">Correo Institucional</label>
              <InputText id="state" type="text" />
            </div>
            <div class="mb-4">
              <label for="state" class="block font-medium text-900 mb-2">Número Celular</label>
              <InputText id="state" type="text" />
            </div>
            <div>
              <Button label="Guardar" class="w-auto mr-2"></Button>
              <Button label="Cancelar" class="w-auto mr-2 p-button-danger"></Button>
            </div>
          </div>
          <div class="flex flex-column align-items-center flex-or">
            <span class="font-medium text-900 mb-2">Foto</span>
            <img src="/images/avatar.png" class="h-10rem w-10rem" />
            <Button type="button" icon="pi pi-pencil" class="p-button-rounded -mt-4"></Button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>



<style scoped>

</style>