import { estado } from "./estado.js";
import { renderResumen } from "./resumen.js";
import { renderEventos } from "./eventos.js";

const titulos = {
    resumen: "Resumen",
    eventos: "Eventos",
    reportes: "Reportes",
    zonas: "Zonas",
    estaciones: "Estaciones",
    historico: "Histórico",
    metricas: "Métricas",
    configuracion: "Configuración",
    versiones: "Versiones",
    arboles: "Árboles"
};

export function navegar(seccion) {
    estado.seccion = seccion;

    document.querySelectorAll(".nav-btn").forEach((boton) => {
        boton.classList.remove("active");
    });

    const botonActivo = document.querySelector(
        `.nav-btn[data-section="${seccion}"]`
    );

    if (botonActivo) {
        botonActivo.classList.add("active");
    }

    actualizarTitulo(seccion);

    if (seccion === "resumen") {
        renderResumen();
    }

    if (seccion === "eventos") {
        renderEventos();
    }
}

function actualizarTitulo(seccion) {
    const titulo = document.getElementById("hdr-section");

    if (titulo) {
        titulo.textContent = titulos[seccion] || "SismoLab";
    }
}

export function iniciarNavegacion() {
    document.querySelectorAll(".nav-btn").forEach((boton) => {
        boton.addEventListener("click", () => {
            navegar(boton.dataset.section);
        });
    });

    navegar(estado.seccion);
}