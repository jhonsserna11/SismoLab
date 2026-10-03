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

        indicadores = self.escenario.obtenerIndicadores()

        contenedor = tk.Frame(self.padre)
        contenedor.pack(fill="x")

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

        metricas_acumulativas = indicadores["metricasAcumulativas"]

        tk.Label(
            self.padre,
            text="Métricas acumulativas",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", pady=(30, 10))

        for nombre, valor in metricas_acumulativas.items():
            tk.Label(
                self.padre,
                text=f"{nombre}: {valor}",
                font=("Arial", 10)
            ).pack(anchor="w", pady=2)

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