import { estado } from "./estado.js";
export function renderZonas() {
    const contenido = document.getElementById("content");

    if (!contenido) return;

    contenido.innerHTML = `
        <div class="space-y">

            <div class="card">

                <div class="card-header">
                    <div>
                        <div class="card-title">
                            Zonas
                        </div>

                        <div class="card-sub">
                            Zonas configuradas para el escenario actual
                        </div>
                    </div>
                </div>

                <div style="padding: 16px;">

                    <div class="tbl-wrap">

                        <table>
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Nombre</th>
                                    <th>Rango X</th>
                                    <th>Rango Y</th>
                                    <th>Estado</th>
                                </tr>
                            </thead>

                            <tbody>
                                ${estado.zonas.map(zona => `
                                    <tr>
                                        <td class="id-cell">${zona.id}</td>
                                        <td>${zona.nombre}</td>
                                        <td class="mono">${zona.xMin} – ${zona.xMax}</td>
                                        <td class="mono">${zona.yMin} – ${zona.yMax}</td>
                                        <td>
                                            <span class="badge ${zona.poblada ? "badge-success" : "badge-info"}">
                                                ${zona.poblada ? "Poblada" : "No poblada"}
                                            </span>
                                        </td>
                                    </tr>
                                `).join("")}
                            </tbody>

                        </table>

                    </div>

                </div>

            </div>

        </div>
    `;
}