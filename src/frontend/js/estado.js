export const estado = {
    seccion: "resumen",
    eventoSeleccionado: null,

    modoEstres: false,
    temaOscuro: false,

    tiempo: new Date("2026-10-01T10:00:00Z"),

    eventos: [],
    reportes: [],
    zonas: [
        {
            id: "Z-1",
            nombre: "Zona mia",
            xMin: 0,
            xMax: 250,
            yMin: 0,
            yMax: 250
        },
        {
            id: "Z-2",
            nombre: "Zona suya",
            xMin: 250,
            xMax: 500,
            yMin: 250,
            yMax: 500
        }
    ],
    estaciones: [
        {
            id_estacion: "EST-1",
            nombre: "Estación Manizales",
        }
    ],

    historico: [],
    versiones: []
};