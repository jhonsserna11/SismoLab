import { estado } from "./estado.js";

export function renderEventos() {
    const contenido = document.getElementById("content");

    if (!contenido) return;

    contenido.innerHTML = `
        <div class="space-y">

            <div class="card">

                <div class="card-header">
                    <div>
                        <div class="card-title">
                            Eventos sísmicos
                        </div>

                        <div class="card-sub">
                            Eventos activos registrados en el escenario
                        </div>
                    </div>

                    <button
                        class="btn btn-primary"
                        type="button"
                        id="nuevo-evento"
                    >
                        + Nuevo evento
                    </button>
                </div>

                <div style="padding: 16px;">

                    <div class="toolbar">

                        <input
                            type="text"
                            id="buscar-evento"
                            placeholder="Buscar por ID..."
                        />

                        <select id="filtro-prioridad">
                            <option value="todas">
                                Todas las prioridades
                            </option>

                            <option value="3">
                                Prioridad alta
                            </option>

                            <option value="2">
                                Prioridad media
                            </option>

                            <option value="1">
                                Prioridad baja
                            </option>
                        </select>

                        <select id="filtro-estado">
                            <option value="todos">
                                Todos los estados
                            </option>

                            <option value="Pendiente">
                                Pendiente
                            </option>

                            <option value="Revisado">
                                Revisado
                            </option>
                        </select>

                    </div>

                    <div class="tbl-wrap">
                        ${crearTablaEventos(estado.eventos)}
                    </div>

                </div>

            </div>

        </div>
    `;

    conectarEventos();
}


function crearTablaEventos(eventos) {

    if (eventos.length === 0) {

        return `
            <div class="detail-empty">

                <div class="detail-empty-icon">
                    📡
                </div>

                <div>
                    No hay eventos registrados
                </div>

            </div>
        `;
    }

    return `
        <table>

            <thead>
                <tr>
                    <th>ID</th>
                    <th>Magnitud</th>
                    <th>Profundidad</th>
                    <th>Epicentro</th>
                    <th>Prioridad</th>
                    <th>Estado</th>
                    <th>Revisión</th>
                    <th></th>
                </tr>
            </thead>

            <tbody>

                ${eventos.map((evento) => `
                    <tr
                        data-evento-id="${escaparHTML(String(evento.id))}"
                        class="${
                            String(estado.eventoSeleccionado) ===
                            String(evento.id)
                                ? "selected"
                                : ""
                        }"
                    >

                        <td class="id-cell">
                            ${escaparHTML(String(evento.id))}
                        </td>

                        <td>
                            ${Number(
                                evento.magnitud ??
                                evento.magnitude ??
                                0
                            ).toFixed(1)}

                            <span style="color: var(--text-4);">
                                Mw
                            </span>
                        </td>

                        <td>
                            ${evento.profundidad ??
                              evento.depth ??
                              "—"}

                            <span style="color: var(--text-4);">
                                km
                            </span>
                        </td>

                        <td class="mono">
                            (${evento.x ?? "—"}, ${evento.y ?? "—"})
                        </td>

                        <td>
                            ${crearBadgePrioridad(evento.prioridad)}
                        </td>

                        <td>
                            ${crearBadgeEstado(evento.estado)}
                        </td>

                        <td class="mono">
                            #${evento.revision ?? 1}
                        </td>

                        <td>
                            <button
                                class="btn btn-sm btn-dark"
                                data-action="consultar"
                                data-id="${escaparHTML(String(evento.id))}"
                            >
                                Ver
                            </button>
                        </td>

                    </tr>
                `).join("")}

            </tbody>

        </table>
    `;
}


function conectarEventos() {

    const buscar = document.getElementById("buscar-evento");
    const filtroPrioridad =
        document.getElementById("filtro-prioridad");
    const filtroEstado =
        document.getElementById("filtro-estado");

    if (buscar) {
        buscar.addEventListener("input", aplicarFiltros);
    }

    if (filtroPrioridad) {
        filtroPrioridad.addEventListener("change", aplicarFiltros);
    }

    if (filtroEstado) {
        filtroEstado.addEventListener("change", aplicarFiltros);
    }

    conectarFilasTabla();

    const nuevo = document.getElementById("nuevo-evento");

    if (nuevo) {
        nuevo.onclick = abrirFormularioEvento;
    }
}

function abrirFormularioEvento() {

    const contenido = document.getElementById("content");

    if (!contenido) return;

    contenido.innerHTML = `
        <div class="space-y">

            <div class="card">

                <div class="card-header">

                    <div>
                        <div class="card-title">
                            Nuevo evento sísmico
                        </div>

                        <div class="card-sub">
                            Registre los datos del evento detectado
                        </div>
                    </div>

                    <button
                        class="btn btn-dark"
                        type="button"
                        id="cancelar-evento"
                    >
                        Cancelar
                    </button>

                </div>

                <div style="padding: 20px;">

                    <form id="form-evento">

                        <div class="form-grid">

                            <div class="form-group">
                                <label for="evento-id">
                                    Identificador
                                </label>

                                <input
                                    id="evento-id"
                                    type="number"
                                    min="1"
                                    max="999999"
                                    placeholder="Ej. 1001"
                                >
                            </div>


                            <div class="form-group">
                                <label for="evento-magnitud">
                                    Magnitud
                                </label>

                                <input
                                    id="evento-magnitud"
                                    type="number"
                                    step="0.1"
                                    placeholder="Ej. 5.2"
                                >
                            </div>


                            <div class="form-group">
                                <label for="evento-profundidad">
                                    Profundidad
                                </label>

                                <div class="input-unit">
                                    <input
                                        id="evento-profundidad"
                                        type="number"
                                        step="0.1"
                                        placeholder="Ej. 25.0"
                                    >

                                    <span>km</span>
                                </div>
                            </div>


                            <div class="form-group">
                                <label for="evento-x">
                                    Coordenada X
                                </label>

                                <input
                                    id="evento-x"
                                    type="number"
                                    step="0.1"
                                    placeholder="Ej. 12.5"
                                >
                            </div>


                            <div class="form-group">
                                <label for="evento-y">
                                    Coordenada Y
                                </label>

                                <input
                                    id="evento-y"
                                    type="number"
                                    step="0.1"
                                    placeholder="Ej. 8.3"
                                >
                            </div>


                            <div class="form-group">
                                <label for="evento-fecha">
                                    Fecha y hora UTC
                                </label>

                                <input
                                    id="evento-fecha"
                                    type="datetime-local"
                                    step="1"
                                >
                            </div>

                        </div>


                        <div class="form-group" style="margin-top: 20px;">

                            <label for="evento-estaciones">
                                Estaciones emisoras
                            </label>

                            <input
                                id="evento-estaciones"
                                type="text"
                                placeholder="Ej. EST-1, EST-3"
                            >

                            <div class="form-help">
                                Separe las estaciones mediante comas.
                            </div>

                        </div>


                        <div
                            id="form-evento-mensaje"
                            class="form-message"
                            style="display: none;"
                        ></div>


                        <div class="form-actions">

                            <button
                                class="btn btn-dark"
                                type="button"
                                id="cancelar-evento-form"
                            >
                                Cancelar
                            </button>

                            <button
                                class="btn btn-primary"
                                type="submit"
                            >
                                Crear evento
                            </button>

                        </div>

                    </form>

                </div>

            </div>

        </div>
    `;


    document
        .getElementById("cancelar-evento")
        .addEventListener("click", renderEventos);


    document
        .getElementById("cancelar-evento-form")
        .addEventListener("click", renderEventos);


    document
        .getElementById("form-evento")
        .addEventListener("submit", (evento) => {

            evento.preventDefault();

            const mensaje =
                document.getElementById("form-evento-mensaje");

            mensaje.textContent =
                "El formulario está listo. La creación se conectará a la lógica de Python.";

            mensaje.style.display = "block";
        });
}


function conectarFilasTabla() {

    document.querySelectorAll("tbody tr").forEach((fila) => {

        fila.addEventListener("click", (evento) => {

            if (evento.target.closest("button")) {
                return;
            }

            estado.eventoSeleccionado = fila.dataset.eventoId;

            renderEventos();
        });
    });

    document
        .querySelectorAll("[data-action='consultar']")
        .forEach((boton) => {

            boton.addEventListener("click", () => {

                estado.eventoSeleccionado = boton.dataset.id;

                renderEventos();
            });
        });
}


function aplicarFiltros() {

    const buscar =
        document.getElementById("buscar-evento");

    const filtroPrioridad =
        document.getElementById("filtro-prioridad");

    const filtroEstado =
        document.getElementById("filtro-estado");

    const texto = buscar.value
        .trim()
        .toLowerCase();

    const prioridad = filtroPrioridad.value;
    const estadoFiltro = filtroEstado.value;

    const filtrados = estado.eventos.filter((evento) => {

        const coincideId =
            String(evento.id)
                .toLowerCase()
                .includes(texto);

        const coincidePrioridad =
            prioridad === "todas" ||
            String(evento.prioridad) === prioridad;

        const coincideEstado =
            estadoFiltro === "todos" ||
            evento.estado === estadoFiltro;

        return (
            coincideId &&
            coincidePrioridad &&
            coincideEstado
        );
    });

    const tabla = document.querySelector(".tbl-wrap");

    if (tabla) {
        tabla.innerHTML = crearTablaEventos(filtrados);
        conectarFilasTabla();
    }
}


function crearBadgePrioridad(prioridad) {

    if (Number(prioridad) === 3) {
        return `
            <span class="badge badge-danger">
                Alta
            </span>
        `;
    }

    if (Number(prioridad) === 2) {
        return `
            <span class="badge badge-warning">
                Media
            </span>
        `;
    }

    return `
        <span class="badge badge-info">
            Baja
        </span>
    `;
}


function crearBadgeEstado(estadoEvento) {

    if (estadoEvento === "Pendiente") {
        return `
            <span class="badge badge-warning">
                Pendiente
            </span>
        `;
    }

    return `
        <span class="badge badge-success">
            ${escaparHTML(estadoEvento ?? "—")}
        </span>
    `;
}


function escaparHTML(valor) {

    return String(valor)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}