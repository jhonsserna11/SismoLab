import { estado } from "./estado.js";
export function renderEstaciones() {
    const contenido = document.getElementById("content");

    if (!contenido) return;

    contenido.innerHTML = `
        <div class="space-y">

            <div class="card">

                <div class="card-header">
                    <div>
                        <div class="card-title">
                            Estaciones sísmicas
                        </div>

                        <div class="card-sub">
                            Estaciones configuradas para el escenario actual
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
                                    <th></th>
                                </tr>
                            </thead>

                            <tbody>
                                ${estado.estaciones.map(estacion => `
                                    <tr>
                                        <td class="id-cell">${estacion.id_estacion}</td>
                                        <td>${estacion.nombre}</td>
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