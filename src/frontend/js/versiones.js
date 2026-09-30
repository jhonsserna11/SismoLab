import { estado } from "./estado.js";

export function renderVersiones() {
    const contenido = document.getElementById("content");
    if (!contenido) return;

    const versiones = estado.versiones || [];

    contenido.innerHTML = `
        <div class="space-y">

            <div class="card">
                <div class="card-header">
                    <div>
                        <div class="card-title">
                            Versiones del escenario
                        </div>
                        <div class="card-sub">
                            Estado actual y puntos de restauración
                        </div>
                    </div>
                </div>

                <div style="padding: 16px;">

                    <div class="config-section">
                        <div class="config-section-title">
                            Estado actual
                        </div>

                        <div class="current-state">
                            <div>
                                <div class="config-lbl">
                                    Escenario
                                </div>
                                <div class="config-val">
                                    Actual
                                </div>
                            </div>

                            <div>
                                <span class="badge badge-success">
                                    Activo
                                </span>
                            </div>
                        </div>

                        <div class="action-row">
                            <button
                                class="btn btn-primary"
                                id="btn-crear-snapshot"
                            >
                                Crear snapshot
                            </button>
                        </div>
                    </div>

                    <div class="config-section">
                        <div class="config-section-title">
                            Snapshots
                        </div>

                        ${
                            versiones.length === 0
                                ? `
                                    <div class="detail-empty">
                                        <div class="detail-empty-icon">
                                            💾
                                        </div>
                                        <div>
                                            No hay snapshots guardados
                                        </div>
                                    </div>
                                `
                                : `
                                    <div>
                                        ${versiones.map((version, indice) => `
                                            <div class="snapshot-row">
                                                <div>
                                                    <div class="config-lbl">
                                                        ${version.nombre || `Snapshot ${indice + 1}`}
                                                    </div>
                                                    <div class="config-sub">
                                                        ${version.fecha || "Fecha no disponible"}
                                                    </div>
                                                </div>

                                                <div class="action-row">
                                                    <button
                                                        class="btn btn-ghost btn-sm"
                                                        data-restaurar="${indice}"
                                                    >
                                                        Restaurar
                                                    </button>
                                                </div>
                                            </div>
                                        `).join("")}
                                    </div>
                                `
                        }
                    </div>

                </div>
            </div>

        </div>
    `;

    conectarVersiones();
}

function conectarVersiones() {
    const botonSnapshot = document.getElementById(
        "btn-crear-snapshot"
    );

    if (botonSnapshot) {
        botonSnapshot.addEventListener("click", () => {
            alert(
                "La creación de snapshots se implementará posteriormente."
            );
        });
    }

    document.querySelectorAll("[data-restaurar]").forEach(boton => {
        boton.addEventListener("click", () => {
            alert(
                "La restauración de snapshots se implementará posteriormente."
            );
        });
    });
}