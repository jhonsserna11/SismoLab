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
        titulo.pack(anchor="w", pady=(0, 3))

        subtitulo = tk.Label(
            self.padre,
            text="Visualización y comparación de las estructuras AVL y BST",
            font=("Arial", 11)
        )
        subtitulo.pack(anchor="w", pady=(0, 15))

        estado_frame = tk.Frame(self.padre)
        estado_frame.pack(fill="x", pady=(0, 12))

        self.crear_estado_general(estado_frame)

        contenedor = tk.Frame(self.padre)
        contenedor.pack(fill="both", expand=True)

        datos_arboles = self.escenario.obtener_nodos(
            self.escenario.avl,
            self.escenario.bst
        )

        datos_avl = datos_arboles["avl"]
        datos_bst = datos_arboles["bst"]

        panel_avl = self.crear_panel(
            contenedor,
            "🌳 Árbol AVL",
            self.escenario.avl,
            datos_avl,
            es_avl=True
        )

        panel_avl.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 6)
        )

        panel_bst = self.crear_panel(
            contenedor,
            "🌲 Árbol BST",
            self.escenario.bst,
            datos_bst,
            es_avl=False
        )

        panel_bst.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(6, 0)
        )

        self.mostrar_estado("Árboles actualizados")

    def crear_estado_general(self, padre):
        modo = self.escenario.modo_estres

        if modo:
            texto = "⚡ MODO ESTRÉS ACTIVO  •  El AVL puede presentar desbalance"
        else:
            texto = "✓ MODO NORMAL  •  El AVL mantiene el balance automáticamente"

        color = "#FFF3CD" if modo else "#E8F5E9"

        estado = tk.Label(
            padre,
            text=texto,
            bg=color,
            font=("Arial", 10, "bold"),
            anchor="w",
            padx=12,
            pady=7
        )

        estado.pack(fill="x")

    def crear_panel(self, padre, titulo, arbol, datos_arbol, es_avl):
        panel = tk.Frame(
            padre,
            bd=1,
            relief="solid",
            padx=12,
            pady=12
        )

        encabezado = tk.Frame(panel)
        encabezado.pack(fill="x", pady=(0, 8))

        tk.Label(
            encabezado,
            text=titulo,
            font=("Arial", 16, "bold")
        ).pack(side="left")

        if es_avl:
            estado = self.obtener_estado_avl(arbol)

            tk.Label(
                encabezado,
                text=estado,
                font=("Arial", 9, "bold")
            ).pack(side="right")

        informacion = tk.Frame(panel)
        informacion.pack(fill="x", pady=(0, 8))

        self.crear_dato(
            informacion,
            "Nodos",
            self.obtener_peso(arbol)
        )

        self.crear_dato(
            informacion,
            "Altura",
            arbol.altura()
        )

        self.crear_dato(
            informacion,
            "Hojas",
            arbol.hojas()
        )

        if es_avl:
            self.crear_dato(
                informacion,
                "Giros",
                self.obtener_giros(arbol)
            )

        tk.Label(
            panel,
            text="Estructura",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=(3, 5))

        area = tk.Frame(panel)
        area.pack(fill="both", expand=True)

        canvas = tk.Canvas(
            area,
            bg="white",
            highlightthickness=1,
            highlightbackground="#D0D0D0"
        )

        canvas.pack(
            fill="both",
            expand=True
        )

        if datos_arbol["raiz"] is None:
            canvas.create_text(
                200,
                120,
                text="Árbol vacío",
                font=("Arial", 12)
            )
            return panel

        canvas.bind(
            "<Configure>",
            lambda event,
            c=canvas,
            datos=datos_arbol,
            avl=es_avl:
                self.dibujar_arbol(c, datos, avl)
        )

        self.dibujar_arbol(
            canvas,
            datos_arbol,
            es_avl
        )

        return panel

    def crear_dato(self, padre, etiqueta, valor):
        bloque = tk.Frame(
            padre,
            bd=1,
            relief="solid",
            padx=10,
            pady=5
        )

        bloque.pack(
            side="left",
            padx=(0, 7)
        )

        tk.Label(
            bloque,
            text=etiqueta,
            font=("Arial", 8)
        ).pack()

        tk.Label(
            bloque,
            text=str(valor),
            font=("Arial", 11, "bold")
        ).pack()

    def obtener_peso(self, arbol):
        if hasattr(arbol, "peso"):
            return arbol.peso()

        return arbol.cantidad_nodos()

    def obtener_estado_avl(self, arbol):
        auditoria = arbol.verificarEstructura(
            self.escenario.modo_estres
        )

        if auditoria["equilibrado"]:
            return "✓ Balanceado"

        if self.escenario.modo_estres:
            return "⚡ Desbalanceado"

        return "⚠ Error de balance"

    def obtener_giros(self, arbol):
        metricas = getattr(arbol, "metricas", {})

        return (
            metricas.get("giros_izquierda", 0)
            + metricas.get("giros_derecha", 0)
        )

    def dibujar_arbol(self, canvas, datos_arbol, es_avl):
        canvas.delete("all")

        ancho = canvas.winfo_width()

        if ancho <= 1:
            ancho = 500

        raiz_id = datos_arbol["raiz"]
        nodos = datos_arbol["nodos"]

        nodos_por_id = {
            nodo["id"]: nodo
            for nodo in nodos
        }

        niveles = {}

        for nodo in nodos:
            nivel = nodo["profundidad"]

            niveles.setdefault(nivel, []).append(nodo)

        posiciones = {}

        max_nivel = max(niveles.keys(), default=0)

        separacion_vertical = 75

        for nivel, nodos_nivel in niveles.items():
            cantidad = len(nodos_nivel)

            if cantidad == 1:
                posiciones[nodos_nivel[0]["id"]] = (
                    ancho / 2,
                    45 + nivel * separacion_vertical
                )
                continue

            separacion_horizontal = ancho / (cantidad + 1)

            for indice, nodo in enumerate(nodos_nivel):
                x = separacion_horizontal * (indice + 1)
                y = 45 + nivel * separacion_vertical

                posiciones[nodo["id"]] = (x, y)

        self.dibujar_conexiones(
            canvas,
            nodos_por_id,
            posiciones,
            raiz_id
        )

        for nodo in nodos:
            x, y = posiciones[nodo["id"]]

            self.dibujar_nodo(
                canvas,
                nodo,
                x,
                y,
                es_avl
            )

    def dibujar_conexiones(
        self,
        canvas,
        nodos_por_id,
        posiciones,
        nodo_id
    ):
        nodo = nodos_por_id[nodo_id]

        x, y = posiciones[nodo_id]

        id_izq = nodo["izq"]
        id_der = nodo["der"]

        if id_izq is not None:
            hijo_x, hijo_y = posiciones[id_izq]

            canvas.create_line(
                x,
                y + 27,
                hijo_x,
                hijo_y - 27,
                width=2,
                fill="#888888"
            )

            self.dibujar_conexiones(
                canvas,
                nodos_por_id,
                posiciones,
                id_izq
            )

        if id_der is not None:
            hijo_x, hijo_y = posiciones[id_der]

            canvas.create_line(
                x,
                y + 27,
                hijo_x,
                hijo_y - 27,
                width=2,
                fill="#888888"
            )

            self.dibujar_conexiones(
                canvas,
                nodos_por_id,
                posiciones,
                id_der
            )
    def dibujar_nodo(self, canvas, nodo, x, y, es_avl):
        if es_avl:
            fondo = "#E8F0FE"
            borde = "#4169E1"
        else:
            fondo = "#F3F3F3"
            borde = "#666666"

        radio = 30

        tag = f"nodo_{nodo['id']}"

        canvas.create_oval(
            x - radio,
            y - radio,
            x + radio,
            y + radio,
            fill=fondo,
            outline=borde,
            width=2,
            tags=(tag,)
        )

        texto_clave = (
            f"P{nodo['prioridad']}  "
            f"M{nodo['magnitud']}  "
            f"ID {nodo['id']}"
        )

        canvas.create_text(
            x,
            y - 7,
            text=texto_clave,
            font=("Arial", 7, "bold"),
            tags=(tag,)
        )

        if es_avl:
            texto_extra = (
                f"Alt: {nodo['altura']}   "
                f"FB: {nodo['factor']}"
            )
        else:
            texto_extra = f"Alt: {nodo['altura']}"

        canvas.create_text(
            x,
            y + 9,
            text=texto_extra,
            font=("Arial", 7),
            tags=(tag,)
        )

        canvas.tag_bind(
            tag,
            "<Button-1>",
            lambda event, id_evento=nodo["id"]:
                self.mostrar_evento(id_evento)
        )

        canvas.tag_bind(
            tag,
            "<Enter>",
            lambda event, c=canvas:
                c.config(cursor="hand2")
        )

        canvas.tag_bind(
            tag,
            "<Leave>",
            lambda event, c=canvas:
                c.config(cursor="")
        )

    def mostrar_evento(self, id_evento):
        resultado = self.escenario.consultarEvento(id_evento)

        self.mostrar_estado(
            f"Evento {id_evento} seleccionado"
        )

    def limpiar(self):
        for widget in self.padre.winfo_children():
            widget.destroy()