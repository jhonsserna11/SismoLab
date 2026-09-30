import { estado } from "./estado.js";

export function renderMetricas() {
    const contenido = document.getElementById("content");

    if (!contenido) return;

    const totalEventos = estado.eventos.length;
    const totalReportes = estado.reportes.length;
    const totalEstaciones = estado.estaciones.length;
    const totalZonas = estado.zonas.length;

    contenido.innerHTML = `
        <div class="space-y">

            <div class="card">
                <div class="card-header">
                    <div>
                        <div class="card-title">
                            Métricas
                        </div>
                        <div class="card-sub">
                            Indicadores generales del escenario actual
                        </div>
                    </div>
                </div>

                <div style="padding: 16px;">
                    <div class="metrics-row">
                        <div class="stat-card">
                            <div class="stat-icon">
                                🌋
                            </div>
                            <div>
                                <div class="stat-val">
                                    ${totalEventos}
                                </div>
                                <div class="stat-lbl">
                                    Eventos activos
                                </div>
                            </div>
                        </div>

                        <div class="stat-card">
                            <div class="stat-icon">
                                📡
                            </div>
                            <div>
                                <div class="stat-val">
                                    ${totalReportes}
                                </div>
                                <div class="stat-lbl">
                                    Reportes recibidos
                                </div>
                            </div>
                        </div>

                        <div class="stat-card">
                            <div class="stat-icon">
                                📍
                            </div>
                            <div>
                                <div class="stat-val">
                                    ${totalEstaciones}
                                </div>
                                <div class="stat-lbl">
                                    Estaciones
                                </div>
                            </div>
                        </div>

                        <div class="stat-card">
                            <div class="stat-icon">
                                🗺️
                            </div>
                            <div>
                                <div class="stat-val">
                                    ${totalZonas}
                                </div>
                                <div class="stat-lbl">
                                    Zonas
                                </div>
                            </div>
                        </div>

                    </div>
                </div>
            </div>

        </div>
    `;
}