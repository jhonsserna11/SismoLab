import tkinter as tk
from tkinter import messagebox

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
        area.pack(
            fill="both",
            expand=True
        )

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

        # Google Maps-style panning.
        canvas.bind(
            "<ButtonPress-1>",
            self.iniciar_desplazamiento
        )

        canvas.bind(
            "<B1-Motion>",
            self.desplazar
        )

        canvas.bind(
            "<ButtonRelease-1>",
            self.terminar_desplazamiento
        )

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

    def iniciar_desplazamiento(self, evento):
        self.canvas_arrastre = evento.widget
        self.canvas_arrastre.scan_mark(
            evento.x,
            evento.y
        )


    def desplazar(self, evento):
        self.canvas_arrastre.scan_dragto(
            evento.x,
            evento.y,
            gain=1
        )


    def terminar_desplazamiento(self, evento):
        self.canvas_arrastre = None

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

        posiciones = {}
        orden_inorden = []

        def recorrer_inorden(nodo_id):
            if nodo_id is None:
                return

            nodo = nodos_por_id[nodo_id]

            recorrer_inorden(nodo["izq"])

            orden_inorden.append(nodo_id)

            recorrer_inorden(nodo["der"])

        recorrer_inorden(raiz_id)

        cantidad_nodos = len(orden_inorden)

        if cantidad_nodos == 0:
            return

        separacion_vertical = 75

        ancho_arbol = max(
            ancho,
            cantidad_nodos * 90
        )

        if cantidad_nodos == 1:
            separacion_horizontal = ancho_arbol / 2
        else:
            separacion_horizontal = ancho_arbol / (cantidad_nodos + 1)

        for indice, nodo_id in enumerate(orden_inorden):
            nodo = nodos_por_id[nodo_id]

            nivel = nodo["profundidad"]

            x = separacion_horizontal * (indice + 1)
            y = 45 + nivel * separacion_vertical

            posiciones[nodo_id] = (x, y)

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
        altura_maxima = max(
            nodo["profundidad"]
            for nodo in nodos
        )

        alto_arbol = (
            45
            + (altura_maxima + 1) * separacion_vertical
            + 45
        )

        canvas.configure(
            scrollregion=(
                0,
                0,
                ancho_arbol,
                alto_arbol
            )
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
        try:
            datos = self.escenario.consultarEvento(id_evento)

            ventana = tk.Toplevel(self.padre)
            ventana.title(f"Evento {id_evento}")
            ventana.geometry("480x650")
            ventana.resizable(False, False)

            tk.Label(
                ventana,
                text=f"Evento {id_evento}",
                font=("Arial", 18, "bold")
            ).pack(
                anchor="w",
                padx=20,
                pady=(20, 5)
            )

            tk.Label(
                ventana,
                text="Información del evento y del nodo AVL",
                font=("Arial", 10)
            ).pack(
                anchor="w",
                padx=20,
                pady=(0, 15)
            )

            contenido = tk.Frame(ventana)
            contenido.pack(
                fill="both",
                expand=True,
                padx=20
            )

            informacion = [
                ("ID", id_evento),
                ("Prioridad", datos["prioridad"]),
                ("Magnitud", datos["magnitud"]),
                ("Profundidad", datos["profundidad"]),
                ("Zona X", datos["zonax"]),
                ("Zona Y", datos["zonay"]),
                ("Fecha", datos["fecha"]),
                ("Revisión", datos["revision"]),
                ("Estado", datos["estado"]),
                ("Zona poblada", datos["poblada"]),
                ("Clave AVL", datos["clave"]),
                ("Profundidad nodo", datos["profundidadNodo"]),
                ("Altura nodo", datos["altura"]),
                ("Factor de balance", datos["factor_balance"]),
                (
                    "Asociado",
                    datos["asociaciones"]["asociado"]
                ),
            ]

            for nombre, valor in informacion:
                fila = tk.Frame(contenido)
                fila.pack(
                    fill="x",
                    pady=3
                )

                tk.Label(
                    fila,
                    text=f"{nombre}:",
                    font=("Arial", 9, "bold"),
                    width=22,
                    anchor="w"
                ).pack(side="left")

                tk.Label(
                    fila,
                    text=str(valor),
                    font=("Arial", 9),
                    anchor="w"
                ).pack(
                    side="left",
                    fill="x",
                    expand=True
                )

            tk.Label(
                contenido,
                text="Estaciones",
                font=("Arial", 11, "bold")
            ).pack(
                anchor="w",
                pady=(12, 5)
            )

            estaciones = datos["estaciones"]

            texto_estaciones = (
                ", ".join(str(estacion) for estacion in estaciones)
                if estaciones
                else "Ninguna"
            )

            tk.Label(
                contenido,
                text=texto_estaciones,
                font=("Arial", 9),
                justify="left",
                wraplength=420
            ).pack(
                anchor="w"
            )

            tk.Label(
                contenido,
                text="Candidatos de asociación",
                font=("Arial", 11, "bold")
            ).pack(
                anchor="w",
                pady=(12, 5)
            )

            candidatos = datos["asociaciones"]["candidatos"]

            texto_candidatos = (
                ", ".join(str(candidato) for candidato in candidatos)
                if candidatos
                else "Ninguno"
            )

            tk.Label(
                contenido,
                text=texto_candidatos,
                font=("Arial", 9),
                justify="left",
                wraplength=420
            ).pack(
                anchor="w"
            )

            tk.Button(
                ventana,
                text="Cerrar",
                command=ventana.destroy
            ).pack(
                pady=15
            )

            self.mostrar_estado(
                f"Evento {id_evento} seleccionado"
            )

        except Exception as error:
            messagebox.showerror(
                "Error al consultar evento",
                str(error)
            )
    def limpiar(self):
        for widget in self.padre.winfo_children():
            widget.destroy()