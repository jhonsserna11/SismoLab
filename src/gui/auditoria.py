import tkinter as tk


class PantallaAuditoria:

    def __init__(self, padre, escenario, mostrar_estado):
        self.padre = padre
        self.escenario = escenario
        self.mostrar_estado = mostrar_estado

    def mostrar(self):
        self.limpiar()

        titulo = tk.Label(
            self.padre,
            text="Auditoría",
            font=("Arial", 22, "bold")
        )
        titulo.pack(anchor="w", pady=(0, 5))

        subtitulo = tk.Label(
            self.padre,
            text="Estado estructural del escenario",
            font=("Arial", 11)
        )
        subtitulo.pack(anchor="w", pady=(0, 20))

        avl = self.escenario.avl

        tk.Label(
            self.padre,
            text="Árbol AVL",
            font=("Arial", 15, "bold")
        ).pack(anchor="w", pady=(0, 10))

        tk.Label(
            self.padre,
            text=f"Nodos: {avl.peso()}",
            font=("Arial", 11)
        ).pack(anchor="w", pady=2)

        tk.Label(
            self.padre,
            text=f"Altura: {avl.altura()}",
            font=("Arial", 11)
        ).pack(anchor="w", pady=2)

        tk.Label(
            self.padre,
            text=(
                "Modo estrés: "
                + ("ACTIVADO" if self.escenario.modo_estres else "DESACTIVADO")
            ),
            font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=(2, 15))

        tk.Label(
            self.padre,
            text="Factores de balance",
            font=("Arial", 13, "bold")
        ).pack(anchor="w", pady=(10, 5))

        factores = tk.Text(
            self.padre,
            height=12,
            width=60,
            state="normal"
        )
        factores.pack(fill="both", expand=True)

        self.mostrar_factores(
            factores,
            getattr(avl, "raiz", None)
        )

        factores.config(state="disabled")

        self.mostrar_estado("Auditoría actualizada")

    def mostrar_factores(self, texto, nodo):
        if nodo is None:
            return

        key = nodo.key

        factor = getattr(
            nodo,
            "factor_balance",
            getattr(nodo, "factor", "N/D")
        )

        texto.insert(
            "end",
            f"ID={key.id_key} | "
            f"P={key.prioridad} | "
            f"M={key.magnitud} | "
            f"Factor={factor}\n"
        )

        self.mostrar_factores(
            texto,
            getattr(nodo, "izquierda", None)
        )

        self.mostrar_factores(
            texto,
            getattr(nodo, "derecha", None)
        )

    def limpiar(self):
        for widget in self.padre.winfo_children():
            widget.destroy()