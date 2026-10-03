import tkinter as tk


class PantallaArboles:

    def __init__(self, padre, escenario, mostrar_estado):
        self.padre = padre
        self.escenario = escenario
        self.mostrar_estado = mostrar_estado

    def mostrar(self):
        self.limpiar()

        titulo = tk.Label(
            self.padre,
            text="Árboles",
            font=("Arial", 22, "bold")
        )
        titulo.pack(anchor="w", pady=(0, 5))

        subtitulo = tk.Label(
            self.padre,
            text="Comparación entre AVL y BST",
            font=("Arial", 11)
        )
        subtitulo.pack(anchor="w", pady=(0, 20))

        contenedor = tk.Frame(self.padre)
        contenedor.pack(fill="both", expand=True)

        panel_avl = self.crear_panel(
            contenedor,
            "Árbol AVL",
            self.escenario.avl
        )
        panel_avl.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        panel_bst = self.crear_panel(
            contenedor,
            "Árbol BST",
            self.escenario.bst
        )
        panel_bst.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10, 0)
        )

        self.mostrar_estado("Árboles actualizados")

    def crear_panel(self, padre, titulo, arbol):
        panel = tk.Frame(
            padre,
            bd=1,
            relief="solid",
            padx=15,
            pady=15
        )

        tk.Label(
            panel,
            text=titulo,
            font=("Arial", 16, "bold")
        ).pack(anchor="w", pady=(0, 10))

        raiz = getattr(arbol, "raiz", None)

        if raiz is None:
            tk.Label(
                panel,
                text="Árbol vacío.",
                font=("Arial", 11)
            ).pack(anchor="w")

            return panel

        informacion = tk.Frame(panel)
        informacion.pack(fill="x", pady=(0, 15))

        altura = arbol.altura()
        peso = arbol.peso()

        tk.Label(
            informacion,
            text=f"Nodos: {peso}",
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        tk.Label(
            informacion,
            text=f"Altura: {altura}",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(3, 0))

        tk.Label(
            panel,
            text="Estructura",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", pady=(0, 5))

        estructura = tk.Text(
            panel,
            height=12,
            width=35,
            state="normal"
        )
        estructura.pack(
            fill="both",
            expand=True
        )

        self.mostrar_nodos(
            estructura,
            raiz
        )

        estructura.config(state="disabled")

        return panel

    def mostrar_nodos(self, texto, nodo, nivel=0, lado="Raíz"):
        if nodo is None:
            return

        sangria = "    " * nivel

        clave = nodo.key

        texto.insert(
            "end",
            f"{sangria}{lado}: "
            f"ID={clave.id_key}, "
            f"M={clave.magnitud}, "
            f"P={clave.prioridad}\n"
        )

        if nodo.izquierda is not None:
            self.mostrar_nodos(
                texto,
                nodo.izquierda,
                nivel + 1,
                "Izquierda"
            )

        if nodo.derecha is not None:
            self.mostrar_nodos(
                texto,
                nodo.derecha,
                nivel + 1,
                "Derecha"
            )

    def limpiar(self):
        for widget in self.padre.winfo_children():
            widget.destroy()