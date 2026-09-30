import { estado } from "./estado.js";

function actualizarReloj() {
    const reloj = document.getElementById("utc-clock");

    if (!reloj) return;

    const fecha = estado.tiempo;

    const año = fecha.getUTCFullYear();
    const mes = String(fecha.getUTCMonth() + 1).padStart(2, "0");
    const dia = String(fecha.getUTCDate()).padStart(2, "0");

    const hora = String(fecha.getUTCHours()).padStart(2, "0");
    const minuto = String(fecha.getUTCMinutes()).padStart(2, "0");
    const segundo = String(fecha.getUTCSeconds()).padStart(2, "0");

    reloj.textContent =
        `${año}-${mes}-${dia} ${hora}:${minuto}:${segundo} UTC`;
}

function abrirEditorReloj() {
    const reloj = document.getElementById("utc-clock");

    if (!reloj) return;

    // Si ya está abierto, no hacemos nada
    if (document.getElementById("editor-reloj")) return;

    const fecha = estado.tiempo;

    const editor = document.createElement("div");
    editor.id = "editor-reloj";
    editor.className = "editor-reloj";

    editor.innerHTML = `
        <div class="campo-tiempo">
            <label>Año</label>
            <input id="tiempo-año" type="number" value="${fecha.getUTCFullYear()}">
        </div>

        <div class="campo-tiempo">
            <label>Mes</label>
            <input id="tiempo-mes" type="number" min="1" max="12"
                   value="${fecha.getUTCMonth() + 1}">
        </div>

        <div class="campo-tiempo">
            <label>Día</label>
            <input id="tiempo-dia" type="number" min="1" max="31"
                   value="${fecha.getUTCDate()}">
        </div>

        <div class="campo-tiempo">
            <label>Hora</label>
            <input id="tiempo-hora" type="number" min="0" max="23"
                   value="${fecha.getUTCHours()}">
        </div>

        <div class="campo-tiempo">
            <label>Min</label>
            <input id="tiempo-minuto" type="number" min="0" max="59"
                   value="${fecha.getUTCMinutes()}">
        </div>

        <div class="campo-tiempo">
            <label>Seg</label>
            <input id="tiempo-segundo" type="number" min="0" max="59"
                   value="${fecha.getUTCSeconds()}">
        </div>

        <div class="acciones-tiempo">
            <button id="tiempo-cancelar" type="button">Cancelar</button>
            <button id="tiempo-aceptar" type="button">Aceptar</button>
        </div>
    `;

    reloj.parentElement.appendChild(editor);

    document.getElementById("tiempo-cancelar")
        .addEventListener("click", cerrarEditorReloj);

    document.getElementById("tiempo-aceptar")
        .addEventListener("click", aplicarTiempo);
}
function cerrarEditorReloj() {
    const editor = document.getElementById("editor-reloj");

    if (editor) {
        editor.remove();
    }
}

function aplicarTiempo() {
    const año = Number(document.getElementById("tiempo-año").value);
    const mes = Number(document.getElementById("tiempo-mes").value);
    const dia = Number(document.getElementById("tiempo-dia").value);
    const hora = Number(document.getElementById("tiempo-hora").value);
    const minuto = Number(document.getElementById("tiempo-minuto").value);
    const segundo = Number(document.getElementById("tiempo-segundo").value);

    const nuevaFecha = new Date(
        Date.UTC(año, mes - 1, dia, hora, minuto, segundo)
    );

    if (
        nuevaFecha.getUTCFullYear() !== año ||
        nuevaFecha.getUTCMonth() !== mes - 1 ||
        nuevaFecha.getUTCDate() !== dia ||
        nuevaFecha.getUTCHours() !== hora ||
        nuevaFecha.getUTCMinutes() !== minuto ||
        nuevaFecha.getUTCSeconds() !== segundo
    ) {
        alert("La fecha ingresada no es válida.");
        return;
    }

    estado.tiempo = nuevaFecha;

    actualizarReloj();
    cerrarEditorReloj();
}

export function avanzarSegundo() {
    estado.tiempo.setUTCSeconds(
        estado.tiempo.getUTCSeconds() + 1
    );

    actualizarReloj();
}

export function iniciarReloj() {
    actualizarReloj();

    const reloj = document.getElementById("utc-clock");

    if (reloj) {
        reloj.addEventListener("click", abrirEditorReloj);
    }

    const boton = document.getElementById("next-second");

    if (boton) {
        boton.addEventListener("click", avanzarSegundo);
    }
}