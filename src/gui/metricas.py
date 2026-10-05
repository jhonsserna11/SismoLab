import tkinter as tk


class PantallaMetricas:

    def __init__(self, padre, escenario, mostrar_estado):
        self.padre = padre
        self.escenario = escenario
        self.mostrar_estado = mostrar_estado

    def mostrar(self):
        self.limpiar()

        titulo = tk.Label(
            self.padre,
            text="Métricas",
            font=("Arial", 22, "bold")
        )
        titulo.pack(anchor="w", pady=(0, 5))

        subtitulo = tk.Label(
            self.padre,
            text="Indicadores del escenario y del árbol AVL",
            font=("Arial", 11)
        )
        subtitulo.pack(anchor="w", pady=(0, 20))

        contenedor_scroll = tk.Frame(self.padre)
        contenedor_scroll.pack(fill="both", expand=True)

        canvas = tk.Canvas(
            contenedor_scroll,
            highlightthickness=0
        )
        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        barra = tk.Scrollbar(
            contenedor_scroll,
            orient="vertical",
            command=canvas.yview
        )
        barra.pack(
            side="right",
            fill="y"
        )

        canvas.configure(
            yscrollcommand=barra.set
        )

        contenido = tk.Frame(canvas)

        ventana_contenido = canvas.create_window(
            (0, 0),
            window=contenido,
            anchor="nw"
        )

        def actualizar_scroll(evento):
            canvas.configure(
                scrollregion=canvas.bbox("all")
            )

        contenido.bind(
            "<Configure>",
            actualizar_scroll
        )

        def ajustar_ancho(evento):
            canvas.itemconfig(
                ventana_contenido,
                width=evento.width
            )

        canvas.bind(
            "<Configure>",
            ajustar_ancho
        )

        def desplazar(evento):
            canvas.yview_scroll(
                int(-1 * (evento.delta / 120)),
                "units"
            )

        canvas.bind(
            "<MouseWheel>",
            desplazar
        )

        contenido.bind(
            "<MouseWheel>",
            desplazar
        )

        indicadores = self.escenario.obtenerIndicadores()

        # Indicadores generales

        contenedor = tk.Frame(contenido)
        contenedor.pack(
            fill="x",
            padx=5
        )

        datos = [
            ("Eventos activos", indicadores["eventos_activos"]),
            ("Eventos históricos", indicadores["eventos_historicos"]),
            ("Altura AVL", indicadores["altura_avl"]),
            ("Hojas", indicadores["hojas"]),
            (
                "Eventos pendientes",
                indicadores["eventos_pendientes"]["cantidad"]
            ),
            (
                "Accesos costosos",
                indicadores["eventos_costosos"]["cantidad"]
            ),
        ]

        for columna, (nombre, valor) in enumerate(datos):
            self.crear_indicador(
                contenedor,
                nombre,
                valor,
                columna
            )

        # Recorridos del AVL

        tk.Label(
            contenido,
            text="Recorridos del AVL",
            font=("Arial", 14, "bold")
        ).pack(
            anchor="w",
            padx=5,
            pady=(30, 10)
        )

        recorridos = [
            ("Inorden", indicadores["inorden"]),
            ("Preorden", indicadores["preorden"]),
            ("Postorden", indicadores["postorden"]),
            ("Por niveles", indicadores["anchura"])
        ]

        for nombre, recorrido in recorridos:
            tk.Label(
                contenido,
                text=f"{nombre}:",
                font=("Arial", 10, "bold")
            ).pack(
                anchor="w",
                padx=5,
                pady=(5, 0)
            )

            texto_recorrido = " → ".join(
                f"({elemento.prioridad}, "
                f"{elemento.magnitud}, "
                f"{elemento.id_key})"
                for elemento in recorrido
            )

            tk.Label(
                contenido,
                text=texto_recorrido,
                font=("Arial", 10),
                justify="left",
                wraplength=1000
            ).pack(
                anchor="w",
                padx=5
            )

        # Métricas acumulativas

        metricas_acumulativas = indicadores["metricasAcumulativas"]

        tk.Label(
            contenido,
            text="Métricas acumulativas",
            font=("Arial", 14, "bold")
        ).pack(
            anchor="w",
            padx=5,
            pady=(30, 10)
        )

        nombres_acumulativas = {
            "correcciones_aceptadas": "Correcciones aceptadas",
            "reportes_descartados": "Reportes descartados",
            "conflictos": "Conflictos",
            "archivos_masivos": "Archivos masivos",
            "eventos_archivados": "Eventos archivados"
        }

        for nombre, valor in metricas_acumulativas.items():
            etiqueta = nombres_acumulativas.get(
                nombre,
                nombre
            )

            tk.Label(
                contenido,
                text=f"{etiqueta}: {valor}",
                font=("Arial", 10)
            ).pack(
                anchor="w",
                padx=5,
                pady=2
            )

        # Indicadores de eventos

        # Indicadores de eventos

        tk.Label(
            contenido,
            text="Indicadores de eventos",
            font=("Arial", 14, "bold")
        ).pack(
            anchor="w",
            padx=5,
            pady=(30, 10)
        )

        por_prioridad = indicadores["eventos_por_prioridad"]

        for prioridad, datos in por_prioridad.items():
            cantidad = datos["cantidad"]

            tk.Label(
                contenido,
                text=f"Prioridad {prioridad}: {cantidad}",
                font=("Arial", 10)
            ).pack(
                anchor="w",
                padx=5,
                pady=2
            )

        # Métricas AVL

        metricas_avl = indicadores["metricasAVL"]

        tk.Label(
            contenido,
            text="Métricas AVL",
            font=("Arial", 14, "bold")
        ).pack(
            anchor="w",
            padx=5,
            pady=(30, 10)
        )

        nombres_avl = {
            "casos_LL": "Casos LL",
            "casos_RR": "Casos RR",
            "casos_LR": "Casos LR",
            "casos_RL": "Casos RL",
            "giros_izquierda": "Giros simples a izquierda",
            "giros_derecha": "Giros simples a derecha"
        }

        for nombre, valor in metricas_avl.items():
            etiqueta = nombres_avl.get(
                nombre,
                nombre
            )

            tk.Label(
                contenido,
                text=f"{etiqueta}: {valor}",
                font=("Arial", 10)
            ).pack(
                anchor="w",
                padx=5,
                pady=2
            )

        self.mostrar_estado("Métricas actualizadas")

        def desplazar(evento):
            canvas.yview_scroll(
                int(-1 * (evento.delta / 120)),
                "units"
            )
        for widget in contenido.winfo_children():
            widget.bind("<MouseWheel>", desplazar)

        canvas.bind("<MouseWheel>", desplazar)
        contenido.bind("<MouseWheel>", desplazar)

        self.mostrar_estado("Métricas actualizadas")

    def crear_indicador(self, padre, nombre, valor, columna):
        tarjeta = tk.Frame(
            padre,
            bd=1,
            relief="solid",
            padx=20,
            pady=15
        )
        tarjeta.grid(
            row=0,
            column=columna,
            padx=5,
            sticky="nsew"
        )

        padre.columnconfigure(
            columna,
            weight=1
        )

        tk.Label(
            tarjeta,
            text=nombre,
            font=("Arial", 10)
        ).pack()

        tk.Label(
            tarjeta,
            text=str(valor),
            font=("Arial", 20, "bold")
        ).pack(pady=(5, 0))

    def limpiar(self):
        for widget in self.padre.winfo_children():
            widget.destroy()

    