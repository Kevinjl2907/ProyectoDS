// Archivo de configuración
//import process from '../../tests/unit/.eslintrc';
import storage from "@/service/storage";

const globales = {
    version: "1.0.0",
    owner: "trust.",
    retrocede_anos: 75,
    avanza_anos: 50,
    retrocede_anos_dashboard: 3,
    modulo_seguridad: 1,
    modulo_comunes: 2,
    modulo_personas: 3,
    modulo_credito: 4,
    modulo_garantias: 5,
    timer_errores: 10000,
    Storage: "Session", // Session / Local
    Storage_expira: 12, // horas.
    unaOpcion: 1, // Traer todas las opciones o solo una por rol.
    idleTime: 5, // 2 Minutos
    timeleft: 10000, // Tiempo de espera antes de ser desconectado del sistema, 10 segundos.
    timeRefresh: 12 * 60 * 60, // 15 horas, igual a Storage_expira, pero en segundos
    //creaAcceso: ambiente.env === "production" ? false : true, // Crear el acceso en la base de datos.
    creaAcceso: true,
    separadorCSV: ";",
};

const paginacion = {
    page_size: 10,
    short_page_size: 3,
    medium_page_size: 50,
    large_page_size: 100,
    no_paginar: 100000000,
    showPaginator: true,
    limit: 20, // Tiene que ser igual a page_size, es el equivalente en postgres
    paginatorTable: [10, 20, 30],
    paginatorTemplate: "CurrentPageReport FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink JumpToPageDropdown",
    currentPageReportTemplate: "{first}..{last} de {totalRecords} registros",
    botones_footer: false,
};

const SecretKey = {
    //aes: '8b$btx_c3le=egl+h584bu(_5yrdk@f_c5)7%oltvaax6r2-$g',
    aes_SALT: "19670509",
    aes_KEY: "67050930290015667092630292031302",
    aes_IV: "1993091419941229",
    aes_MIN: 30,
    token: "6be2b6e6aa27a2be3e369b37f68d7263e260a2e0fa850ab2ec72099520fc0815",
};

const locale = {
    locale: "es-CR",
    localeFns: "es",
    edicion: "en-US", // Para que digite los datos con punto para los decimales
    formato_fecha_topbar: "dddd DD MMMM, YYYY, h:mm:ss a",
    formato_fecha_reportes: "dd/mm/yyyy",
};


const isAdmin = () => {
    let isAdmin = storage.getStorage("numorganizacion") === 1;
    return isAdmin;
};

export default {
    globales,
    paginacion,
    SecretKey,
    locale,
    print,
    isAdmin
};
