import { estado } from "./estado.js";

export function renderArboles() {
    const contenido = document.getElementById("content");

    if (!contenido) return;
    contenido.innerHTML = `
        <div class="space-y">

            <div style="display:flex;align-items:center;gap:16px;flex-wrap:wrap">
                <div class="tree-toggle">
                    <button class="tree-tab active" data-tree-type="avl">
                        AVL
                    </button>

                    <button class="tree-tab" data-tree-type="bst">
                        BST
                    </button>
                </div>

                <div class="tree-stats">
                    <span>Nodos: <strong>0</strong></span>
                    <span style="color:var(--divider)">|</span>
                    <span>Altura AVL: <strong style="color:#0369a1">0</strong></span>
                    <span style="color:var(--divider)">|</span>
                    <span>Altura BST: <strong style="color:#b45309">0</strong></span>
                    <span style="color:var(--divider)">|</span>
                    <span>BF máx: <strong>0</strong></span>
                </div>

                <select id="tree-highlight" style="margin-left:auto">
                    <option value="">Resaltar nodo…</option>
                </select>
            </div>

            <div class="tree-legend">
                <span><strong>Leyenda:</strong></span>

                <span>
                    <span class="legend-dot"
                          style="background:#ef4444;border:1.5px solid #fca5a5"></span>
                    P3 Alta
                </span>

                <span>
                    <span class="legend-dot"
                          style="background:#f97316;border:1.5px solid #fdba74"></span>
                    P2 Media
                </span>

                <span>
                    <span class="legend-dot"
                          style="background:#3b82f6;border:1.5px solid #7dd3fc"></span>
                    P1 Baja
                </span>

                <span style="color:var(--card-border)">|</span>

                <span>
                    Nodo:
                    <strong>ID · Magnitud · BF</strong>
                </span>
            </div>

            <div class="tree-canvas-wrap">

                <div class="tree-canvas-header">
                    <div>
                        <span class="card-title">
                            Árbol AVL — estructura principal de eventos
                        </span>

                        <span style="margin-left:8px;font-size:11px;color:var(--text-4)">
                            ordenado por prioridad → magnitud → ID
                        </span>
                    </div>

                    <span class="mono" style="font-size:11px;color:var(--text-4)">
                        h = 0
                    </span>
                </div>

                <div class="tree-svg-scroll">
                    <div style="padding:40px;text-align:center;color:var(--text-4)">
                        Sin eventos para visualizar
                    </div>
                </div>

            </div>

            <div class="card">

                <div class="card-header">
                    <div class="card-title">
                        Recorrido en orden (inorder)
                    </div>
                </div>

                <div class="tbl-wrap">

                    <table>
                        <thead>
                            <tr>
                                <th>Pos.</th>
                                <th>ID evento</th>
                                <th>Clave</th>
                                <th>Magnitud</th>
                                <th>Profundidad</th>
                                <th>Prioridad</th>
                                <th>Estado</th>
                                <th>BF</th>
                                <th>Altura</th>
                            </tr>
                        </thead>

                        <tbody>
                            <tr>
                                <td colspan="9"
                                    style="text-align:center;color:var(--text-4);padding:24px">
                                    Sin eventos
                                </td>
                            </tr>
                        </tbody>
                    </table>

                </div>

            </div>

        </div>
    `;

    const botones = contenido.querySelectorAll(".tree-tab");

    botones.forEach(boton => {
        boton.addEventListener("click", () => {

            botones.forEach(b => b.classList.remove("active"));

            boton.classList.add("active");
        });
    });
}