import { estado } from "./estado.js";

export function renderResumen() {
    const contenido = document.getElementById("content");

    if (!contenido) return;

    const eventos = estado.eventos;
    const reportes = estado.reportes;
    const zonas = estado.zonas;
    const estaciones = estado.estaciones;

    const pendientes = eventos.filter(
        (evento) => evento.estado === "Pendiente"
    ).length;

    const prioridadAlta = eventos.filter(
        (evento) => Number(evento.prioridad) === 3
    ).length;

    const reportesPendientes = reportes.filter(
        (reporte) => !reporte.procesado
    ).length;

    contenido.innerHTML = `
        <div class="space-y">

            <div class="stat-grid">

                <div class="stat-card">
                    <div class="stat-icon" style="background:#0ea5e918">
                        📡
                    </div>
                    <div>
                        <div class="stat-val">${eventos.length}</div>
                        <div class="stat-lbl">Eventos activos</div>
                        <div class="stat-hint" style="color:#0ea5e9">
                            en estructura AVL
                        </div>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="stat-icon" style="background:#f9731618">
                        ⏳
                    </div>
                    <div>
                        <div class="stat-val">${pendientes}</div>
                        <div class="stat-lbl">Pendientes</div>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="stat-icon" style="background:#dc262618">
                        ⚠️
                    </div>
                    <div>
                        <div class="stat-val">${prioridadAlta}</div>
                        <div class="stat-lbl">Prioridad Alta</div>
                        <div class="stat-hint" style="color:#dc2626">
                            revisión urgente
                        </div>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="stat-icon" style="background:#8b5cf618">
                        📋
                    </div>
                    <div>
                        <div class="stat-val">${reportesPendientes}</div>
                        <div class="stat-lbl">Reportes</div>
                        <div class="stat-hint" style="color:#8b5cf6">
                            en cola FIFO
                        </div>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="stat-icon" style="background:#64748b18">
                        🗄️
                    </div>
                    <div>
                        <div class="stat-val">${estado.historico.length}</div>
                        <div class="stat-lbl">Archivados</div>
                    </div>
                </div>

                <div class="stat-card">
                    <div class="stat-icon" style="background:#10b98118">
                        ✅
                    </div>
                    <div>
                        <div class="stat-val">Operativo</div>
                        <div class="stat-lbl">Sistema</div>
                        <div class="stat-hint" style="color:#10b981">
                            ${estado.modoEstres ? "modo estrés" : "modo normal"}
                        </div>
                    </div>
                </div>

            </div>

            <div class="map-wrap">

                <div class="map-panel card">

                    <div class="card-header">
                        <div>
                            <div class="card-title">
                                Escenario Sísmico
                            </div>

                            <div class="card-sub">
                                1000 × 1000 unidades
                            </div>
                        </div>

                        <div class="map-legend">
                            <span>
                                <span class="legend-dot" style="background:#ef4444"></span>
                                Alta
                            </span>

                            <span>
                                <span class="legend-dot" style="background:#f97316"></span>
                                Media
                            </span>

                            <span>
                                <span class="legend-dot" style="background:#3b82f6"></span>
                                Baja
                            </span>

                            <span>
                                <span class="legend-square"
                                      style="background:#bfdbfe44;border:1px solid #93c5fd"></span>
                                Zona
                            </span>

                            <span>▲ Estación</span>
                        </div>
                    </div>

                    <div style="padding:16px;overflow:auto">
                        ${crearMapa()}
                    </div>

                </div>

                <div class="detail-panel" style="min-height:300px">

                    <div class="card-header">
                        <div class="card-title">
                            Evento seleccionado
                        </div>
                    </div>

                    ${crearDetalleEvento()}

                </div>

            </div>

        </div>
    `;

    conectarEventosMapa();
}

function crearMapa() {
    const ancho = 420;
    const alto = 360;

    const convertirX = (x) => (Number(x) / 1000) * ancho;
    const convertirY = (y) => (Number(y) / 1000) * alto;

    let cuadricula = "";

    for (let i = 1; i < 10; i++) {
        const x = (i / 10) * ancho;
        const y = (i / 10) * alto;

        cuadricula += `
            <line
                x1="${x}"
                y1="0"
                x2="${x}"
                y2="${alto}"
                stroke="#e2e8f0"
                stroke-width=".5"
            />

            <line
                x1="0"
                y1="${y}"
                x2="${ancho}"
                y2="${y}"
                stroke="#e2e8f0"
                stroke-width=".5"
            />
        `;
    }

    const zonas = estado.zonas.map((zona) => {
        const x = Number(zona.xMin);
        const y = Number(zona.yMin);
        const anchoZona = Number(zona.xMax) - x;
        const altoZona = Number(zona.yMax) - y;

        return `
            <rect
                x="${convertirX(x)}"
                y="${convertirY(y)}"
                width="${convertirX(anchoZona)}"
                height="${convertirY(altoZona)}"
                fill="#bfdbfe30"
                stroke="#93c5fd"
                stroke-width="1"
                rx="2"
            />

            <text
                x="${convertirX(x) + 4}"
                y="${convertirY(y) + 11}"
                font-size="7"
                fill="#64748b"
            >
                ${escaparHTML(zona.nombre ?? zona.id ?? "")}
            </text>
        `;
    }).join("");

    const eventos = estado.eventos.map((evento) => {
        const magnitud = Number(evento.magnitud ?? evento.magnitude ?? 0);

        const radio = obtenerRadioMagnitud(magnitud);
        const color = obtenerColorMagnitud(magnitud);

        const seleccionado =
            estado.eventoSeleccionado === evento.id;

        return `
            <g
                class="map-node"
                data-evento-id="${escaparHTML(evento.id)}"
                style="cursor:pointer"
                transform="
                    translate(
                        ${convertirX(evento.x)},
                        ${convertirY(evento.y)}
                    )
                "
            >

                ${
                    seleccionado
                        ? `
                            <circle
                                r="${radio + 6}"
                                fill="none"
                                stroke="${color}"
                                stroke-width="1.5"
                                stroke-dasharray="3,2"
                                opacity=".7"
                            />
                        `
                        : ""
                }

                <circle
                    r="${radio}"
                    fill="${color}"
                    fill-opacity=".8"
                    stroke="${seleccionado ? "#fff" : color}"
                    stroke-width="${seleccionado ? 2 : .5}"
                />

                <text
                    text-anchor="middle"
                    y="${radio + 9}"
                    font-size="6"
                    fill="#334155"
                >
                    ${escaparHTML(String(evento.id))}
                </text>

            </g>
        `;
    }).join("");

    return `
        <svg
            width="${ancho}"
            height="${alto}"
            viewBox="0 0 ${ancho} ${alto}"
            class="map-svg"
            id="scenario-map"
        >

            ${cuadricula}
            ${zonas}
            ${eventos}

            <text
                x="2"
                y="${alto - 3}"
                font-size="6"
                fill="#94a3b8"
            >
                0
            </text>

            <text
                x="${ancho - 25}"
                y="${alto - 3}"
                font-size="6"
                fill="#94a3b8"
            >
                1000
            </text>

            <text
                x="2"
                y="8"
                font-size="6"
                fill="#94a3b8"
            >
                1000
            </text>

        </svg>
    `;
}

function crearDetalleEvento() {
    const evento = estado.eventos.find(
        (elemento) => elemento.id === estado.eventoSeleccionado
    );

    if (!evento) {
        return `
            <div class="detail-empty">
                <div class="detail-empty-icon">📍</div>

                Haz clic en un evento del mapa
                para ver sus detalles
            </div>
        `;
    }

    const magnitud = evento.magnitud ?? evento.magnitude;
    const profundidad = evento.profundidad ?? evento.depth;
    const fecha = evento.fecha ?? evento.datetime;

    return `
        <div class="detail-body">

            <div class="slide-in">

                <div class="detail-id">
                    ${escaparHTML(String(evento.id))}
                </div>

                <div class="detail-row">
                    <span class="detail-label">
                        Magnitud
                    </span>

                    <span class="detail-val">
                        ${Number(magnitud).toFixed(1)} Mw
                    </span>
                </div>

                <div class="detail-row">
                    <span class="detail-label">
                        Profundidad
                    </span>

                    <span class="detail-val">
                        ${profundidad} km
                    </span>
                </div>

                <div class="detail-row">
                    <span class="detail-label">
                        Epicentro
                    </span>

                    <span class="detail-val mono">
                        (${evento.x}, ${evento.y})
                    </span>
                </div>

                <div class="detail-row">
                    <span class="detail-label">
                        Fecha UTC
                    </span>

                    <span class="detail-val">
                        ${formatearUTC(fecha)}
                    </span>
                </div>

                <div class="detail-row">
                    <span class="detail-label">
                        Estaciones
                    </span>

                    <span class="detail-val mono">
                        ${(evento.estaciones ?? []).join(", ")}
                    </span>
                </div>

                <div class="detail-row">
                    <span class="detail-label">
                        Revisión
                    </span>

                    <span class="detail-val">
                        #${evento.revision}
                    </span>
                </div>

                <div class="detail-row">
                    <span class="detail-label">
                        Prioridad
                    </span>

                    <span class="detail-val">
                        ${crearBadgePrioridad(evento.prioridad)}
                    </span>
                </div>

                <div class="detail-row">
                    <span class="detail-label">
                        Estado
                    </span>

                    <span class="detail-val">
                        ${crearBadgeEstado(evento.estado)}
                    </span>
                </div>

            </div>

            <div class="detail-actions">

                <button
                    class="btn btn-primary btn-sm"
                    type="button"
                    data-action="consultar-evento"
                >
                    Consultar
                </button>

                <button
                    class="btn btn-dark btn-sm"
                    type="button"
                    data-action="corregir-evento"
                >
                    Corregir
                </button>

                ${
                    evento.estado === "Pendiente"
                        ? `
                            <button
                                class="btn btn-success btn-sm"
                                type="button"
                                data-action="revisar-evento"
                            >
                                Marcar revisado
                            </button>
                        `
                        : ""
                }

                <button
                    class="btn btn-danger btn-sm"
                    type="button"
                    data-action="eliminar-evento"
                >
                    Eliminar
                </button>

            </div>

        </div>
    `;
}

function obtenerRadioMagnitud(magnitud) {
    if (magnitud >= 6.0) return 9;
    if (magnitud >= 4.5) return 7;
    return 5;
}

function obtenerColorMagnitud(magnitud) {
    if (magnitud >= 6.0) return "#ef4444";
    if (magnitud >= 4.5) return "#f97316";
    return "#3b82f6";
}

function crearBadgePrioridad(prioridad) {
    if (Number(prioridad) === 3) {
        return `<span class="badge badge-high">Alta</span>`;
    }

    if (Number(prioridad) === 2) {
        return `<span class="badge badge-medium">Media</span>`;
    }

    return `<span class="badge badge-low">Baja</span>`;
}

function crearBadgeEstado(estadoEvento) {
    if (estadoEvento === "Pendiente") {
        return `<span class="badge badge-pending">Pendiente</span>`;
    }

    return `
        <span class="badge badge-reviewed">
            ${escaparHTML(estadoEvento ?? "")}
        </span>
    `;
}


function conectarEventosMapa() {
    document.querySelectorAll(".map-node").forEach((nodo) => {
        nodo.addEventListener("click", () => {
            estado.eventoSeleccionado = nodo.dataset.eventoId;

            renderResumen();
        });
    });
}

function escaparHTML(valor) {
    return String(valor)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function formatearUTC(fecha) {
    if (!fecha) return "—";

    const valor = new Date(fecha);

    if (Number.isNaN(valor.getTime())) {
        return String(fecha);
    }

    const año = valor.getUTCFullYear();
    const mes = String(valor.getUTCMonth() + 1).padStart(2, "0");
    const dia = String(valor.getUTCDate()).padStart(2, "0");

    const hora = String(valor.getUTCHours()).padStart(2, "0");
    const minuto = String(valor.getUTCMinutes()).padStart(2, "0");
    const segundo = String(valor.getUTCSeconds()).padStart(2, "0");

    return `${año}-${mes}-${dia} ${hora}:${minuto}:${segundo} UTC`;
}