import { estado } from "./estado.js";

export function renderConfiguracion() {
    const contenido = document.getElementById("content");
    if (!contenido) return;

    const configuracion = estado.configuracion || {
        W: 48,
        R: 40,
        L: 3,
        T: 72,
        modoEstres: false
    };

    contenido.innerHTML = `
        <div class="space-y">

            <div class="card">
                <div class="card-header">
                    <div>
                        <div class="card-title">
                            Configuración del escenario
                        </div>
                        <div class="card-sub">
                            Parámetros de operación de SismoLab
                        </div>
                    </div>
                </div>

                <div style="padding: 16px;">

                    <div class="config-section">
                        <div class="config-section-title">
                            Parámetros del escenario
                        </div>

                        <div class="config-row">
                            <div>
                                <div class="config-lbl">
                                    Ventana temporal (W)
                                </div>
                            </div>

                            <div class="config-val">
                                <input
                                    type="number"
                                    id="config-W"
                                    value="${configuracion.W}"
                                    min="0"
                                    step="1"
                                >
                                <span>h</span>
                            </div>
                        </div>

                        <div class="config-row">
                            <div>
                                <div class="config-lbl">
                                    Radio de proximidad (R)
                                </div>
                            </div>

                            <div class="config-val">
                                <input
                                    type="number"
                                    id="config-R"
                                    value="${configuracion.R}"
                                    min="0"
                                    step="1"
                                >
                                <span>km</span>
                            </div>
                        </div>

                        <div class="config-row">
                            <div>
                                <div class="config-lbl">
                                    Límite de asociaciones (L)
                                </div>
                            </div>

                            <div class="config-val">
                                <input
                                    type="number"
                                    id="config-L"
                                    value="${configuracion.L}"
                                    min="0"
                                    step="1"
                                >
                            </div>
                        </div>

                        <div class="config-row">
                            <div>
                                <div class="config-lbl">
                                    Tiempo de conservación (T)
                                </div>
                            </div>

                            <div class="config-val">
                                <input
                                    type="number"
                                    id="config-T"
                                    value="${configuracion.T}"
                                    min="0"
                                    step="1"
                                >
                                <span>h</span>
                            </div>
                        </div>

                        <div class="action-row">
                            <button
                                class="btn btn-primary"
                                id="btn-guardar-config"
                            >
                                Guardar configuración
                            </button>
                        </div>
                    </div>

                    <div class="config-section">
                        <div class="config-section-title">
                            Escenario
                        </div>

                        <div class="config-row">
                            <div>
                                <div class="config-lbl">
                                    Modo de estrés
                                </div>
                                <div class="config-sub">
                                    Permite operar el escenario con rotaciones
                                    del AVL diferidas.
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="config-section">
                        <div class="config-section-title">
                            Exportación
                        </div>

                        <div class="config-row">
                            <div>
                                <div class="config-lbl">
                                    Exportar escenario actual
                                </div>
                                <div class="config-sub">
                                    Guarda el estado actual del escenario
                                    para recuperarlo posteriormente.
                                </div>
                            </div>

                            <div>
                                <button
                                    class="btn btn-primary"
                                    id="btn-exportar-escenario"
                                >
                                    Exportar escenario
                                </button>
                            </div>
                        </div>
                    </div>

                </div>
            </div>

        </div>
    `;

    conectarConfiguracion();
}

function conectarConfiguracion() {
    const botonGuardar = document.getElementById(
        "btn-guardar-config"
    );

    if (botonGuardar) {
        botonGuardar.addEventListener("click", () => {
            alert(
                "La actualización de la configuración se implementará posteriormente."
            );
        });
    }

    const botonExportar = document.getElementById(
        "btn-exportar-escenario"
    );

    if (botonExportar) {
        botonExportar.addEventListener("click", () => {
            alert(
                "La exportación del escenario se implementará posteriormente."
            );
        });
    }
}