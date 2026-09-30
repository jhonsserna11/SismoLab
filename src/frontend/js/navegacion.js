import { estado } from "./estado.js";
import { renderResumen } from "./resumen.js";
import { renderEventos } from "./eventos.js";
import { renderEstaciones } from "./estaciones.js";
import { renderZonas } from "./zonas.js";
import { renderReportes } from "./reportes.js";
import { renderHistorico } from "./historico.js";
import { renderMetricas } from "./metricas.js";
import { renderConfiguracion } from "./configuracion.js";
import { renderVersiones } from "./versiones.js";
import { renderArboles } from "./arboles.js";

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
    if (seccion === "estaciones") {
        renderEstaciones();
    }
    if (seccion === "zonas") {
        renderZonas();
    }
    if (seccion === "reportes") {
        renderReportes();
    }
    if (seccion === "historico") {
        renderHistorico();
    }
    if (seccion === "metricas") {
        renderMetricas();
    }
    if (seccion === "configuracion") {
        renderConfiguracion();
    }
    if (seccion === "versiones") {
        renderVersiones();
    }
    if (seccion === "arboles") {
        renderArboles();
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