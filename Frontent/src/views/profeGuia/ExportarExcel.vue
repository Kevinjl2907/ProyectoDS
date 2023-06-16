<script>
import { utils, writeFile } from 'xlsx';

// eslint-disable-next-line vue/no-export-in-script-setup
export default {
    name: 'ExportarExcel',
    data() {
        return {
            // URL's
            url: 'comunes/monedas/',
            // Variables utilizadas por el CRUD
            editMode: false,
            addMode: false,
            searchMode: true,
            EditarDialog: false,
            deleteDialog: false,
            selectedRecord: null,
            // Variables utilizadas por la pantalla
            estudiantes: null,
            sedes: null,
            numEstudiante: null,
            nombre: null,
            apellido1: null,
            apellido2: null,
            nombreAdicional: null,
            sede: null,
            correo: null,
            telefonoCelular: null,
            disabeButton: true,
            estMiSede: [],
            dialog: false,
            data: {
                CA: [],
                AL: [],
                LI: [],
                SJ: [],
                SC: []
            }
        };
    },
    async created() {
        await this.getTableContents();
        this.disabeButton = false;
    },
    methods: {
        async getTableContents() {
            var request = {
                method: 'GET',
                headers: { Authorization: localStorage.token } //Token a5f4bab95e1d086c8fcec6ecdbe7fce0817dfe87
            };
            var response = await fetch('https://main.d2anrgvy7s2j70.amplifyapp.com/ListaEstudiantes/', request);
            //.then(response => response.json())
            //.then(data => token=data)
            //.catch(error => console.error(error));
            var myJson = await response.json();
            if (myJson.response === 'unsuccessful') {
                console.log('no exito');
            } else {
                this.estudiantes = myJson.estudiantes;
            }
        },
        ordenarEstudiantes() {
            for (var estudiante of this.estudiantes) {
                console.log('Esta es la info del estudiante', estudiante);
                if (estudiante.sede === 'CA') {
                    this.data.CA.push(estudiante);
                }
                if (estudiante.sede === 'LI') {
                    this.data.LI.push(estudiante);
                }
                if (estudiante.sede === 'SJ') {
                    this.data.SJ.push(estudiante);
                }
                if (estudiante.sede === 'SC') {
                    this.data.SC.push(estudiante);
                }
                if (estudiante.sede === 'AL') {
                    this.data.AL.push(estudiante);
                }
            }
        },
        async exportExcel(data, filename, isAll) {
            if (isAll) {
                const wb = utils.book_new();
                this.ordenarEstudiantes();

                for (const sheetName in this.data) {
                    const ws = utils.json_to_sheet(this.data[sheetName]);
                    utils.book_append_sheet(wb, ws, sheetName);
                }

                writeFile(wb, `${filename}`);
            } else {
                for (var estudiante of this.estudiantes) {
                    if (estudiante.sede === localStorage.sede) {
                        this.estMiSede.push(estudiante);
                    }
                }

                const ws = utils.json_to_sheet(this.estMiSede);
                const wb = utils.book_new();
                utils.book_append_sheet(wb, ws, `Estudiantes ${localStorage.sede}`);
                writeFile(wb, `${filename}`);
            }
        },
        openDialog() {
          this.dialog = this.detailInfo === true ? false : true;
      },
    }
};
</script>

<template>
  <div class="container">
    <div class="background-svg">

    </div>
  </div>

<!--  <Button label="Exportar a Excel Por Sede" icon="pi pi-check" size="large" :disabled="this.disabeButton" @click="exportExcel(this.estudiantes, 'EstudiantesSede.xlsx', false)"/>-->
<!--  <Button label="Exportar a Excel Por Sede" icon="pi pi-check" size="large" :disabled="this.disabeButton" @click="exportExcel(this.estudiantes, 'EstudiantesTodo.xlsx', true)"/>-->

<div class="buttonContainer">
  <h1 class="title">Generar Excel</h1>
  <Button label=" Exportar" @click="this.openDialog" size="mediunm" class="p-button-success p-button-outlined" icon="pi pi-file-export" ></Button>
</div>

  <Dialog v-model:visible="dialog" appendTo="body" :modal="true" :breakpoints="{'960px': '75vw', '640px': '100vw'}" :style="{width: '40vw'}" header="" >
    <div class="flex flex-column align-items-center my-4">
        <span class="flex align-items-center justify-content-center bg-cyan-100 text-cyan-800 mr-3 border-circle mb-3" style="width:64px;height:64px">
            <i class="pi pi-check text-5xl"></i>
        </span>
      <div class="font-medium text-2xl text-900">Exportar Estudiantes a Excel</div>
    </div>
    <p class="line-height-3 p-0 m-0">
    </p>
    <template #footer>
      <div class=" border-top-1 surface-border pt-3 flex">
        <Button  style="background-color: #468480; color: white;" @click="exportExcel(this.estudiantes, 'EstudiantesSede.xlsx', false)" label="Exportar Sede a Excel" class="p-button-outlined w-6 mr-2"></Button>
        <Button  style="background-color: #468480; color: white;" @click="exportExcel(this.estudiantes, 'EstudiantesSede.xlsx', true)" label="Exportar Todo a Excel" class="w-6 ml-2"></Button>
      </div>
    </template>
  </Dialog>



</template>
<style scoped>
.container{
  position: relative;
}

.background-svg{
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
}

.buttonContainer{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 50vh; /* Ajusta la altura según tus necesidades */
}


</style>
