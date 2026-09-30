import { estado } from "./estado.js";

export function renderHistorico() {
    const contenido = document.getElementById("content");

    if (!contenido) return;

    contenido.innerHTML = `
        <div class="space-y">
            <div class="card">
                <div class="card-header">
                    <div>
                        <div class="card-title">
                            Histórico
                        </div>
                        <div class="card-sub">
                            Eventos almacenados en el histórico del escenario
                        </div>
                    </div>
                </div>

                <div style="padding: 16px;">
                    <div class="tbl-wrap">
                        ${
                            estado.historico.length === 0
                                ? `
                                    <div class="detail-empty">
                                        <div class="detail-empty-icon">
                                            🗂️
                                        </div>
                                        <div>
                                            No hay eventos en el histórico
                                        </div>
                                    </div>
                                `
                                : `
                                    <table>
                                        <thead>
                                            <tr>
                                                <th>ID</th>
                                                <th>Magnitud</th>
                                                <th>Profundidad</th>
                                                <th>Epicentro</th>
                                                <th>Estado</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            ${estado.historico.map(evento => `
                                                <tr>
                                                    <td class="id-cell">
                                                        ${evento.id}
                                                    </td>
                                                    <td>
                                                        ${Number(evento.magnitud).toFixed(1)}
                                                        <span style="color: var(--text-4);">
                                                            Mw
                                                        </span>
                                                    </td>
                                                    <td>
                                                        ${evento.profundidad ?? "—"}
                                                        <span style="color: var(--text-4);">
                                                            km
                                                        </span>
                                                    </td>
                                                    <td class="mono">
                                                        (${evento.x ?? "—"}, ${evento.y ?? "—"})
                                                    </td>
                                                    <td>
                                                        ${evento.estado ?? "—"}
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