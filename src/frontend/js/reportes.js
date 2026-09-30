import { estado } from "./estado.js";

export function renderReportes() {
    const contenido = document.getElementById("content");

    if (!contenido) return;

    contenido.innerHTML = `
        <div class="space-y">
            <div class="card">
                <div class="card-header">
                    <div>
                        <div class="card-title">
                            Reportes
                        </div>
                        <div class="card-sub">
                            Reportes recibidos de las estaciones
                        </div>
                    </div>
                </div>

                <div style="padding: 16px;">
                    <div class="tbl-wrap">
                        ${
                            estado.reportes.length === 0
                                ? `
                                    <div class="detail-empty">
                                        <div class="detail-empty-icon">
                                            📡
                                        </div>
                                        <div>
                                            No hay reportes recibidos
                                        </div>
                                    </div>
                                `
                                : `
                                    <table>
                                        <thead>
                                            <tr>
                                                <th>ID</th>
                                                <th>Evento</th>
                                                <th>Estación</th>
                                                <th>Revisión</th>
                                                <th>Estado</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            ${estado.reportes.map(reporte => `
                                                <tr>
                                                    <td class="id-cell">
                                                        ${reporte.id}
                                                    </td>
                                                    <td>
                                                        ${reporte.eventoId}
                                                    </td>
                                                    <td>
                                                        ${reporte.estacionId}
                                                    </td>
                                                    <td class="mono">
                                                        #${reporte.revision}
                                                    </td>
                                                    <td>
                                                        ${reporte.estado}
                                                    </td>
                                                </tr>
                                            `).join("")}
                                        </tbody>
                                    </table>
                                `
                        }
                    </div>
                </div>
            </div>
        </div>
    `;
}