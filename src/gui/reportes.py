import tkinter as tk


class PantallaReportes:

    def __init__(self, padre, escenario, mostrar_estado):
        self.padre = padre
        self.escenario = escenario
        self.mostrar_estado = mostrar_estado

    def mostrar(self):
        self.limpiar()

        titulo = tk.Label(
            self.padre,
            text="Reportes",
            font=("Arial", 22, "bold")
        )
        titulo.pack(anchor="w", pady=(0, 5))

        subtitulo = tk.Label(
            self.padre,
            text="Cola de reportes pendientes",
            font=("Arial", 11)
        )
        subtitulo.pack(anchor="w", pady=(0, 20))

        reportes = list(self.escenario.cola_reportes)

        indicador = tk.Label(
            self.padre,
            text=f"{len(reportes)} reportes pendientes",
            font=("Arial", 12, "bold")
        )
        indicador.pack(anchor="w", pady=(0, 15))

        if not reportes:
            tk.Label(
                self.padre,
                text="No hay reportes pendientes.",
                font=("Arial", 12)
            ).pack(anchor="w")

            self.mostrar_estado("No hay reportes pendientes")
            return

        for posicion, reporte in enumerate(reportes, start=1):
            self.crear_tarjeta(
                reporte,
                posicion
            )

        self.mostrar_estado(
            f"Reportes pendientes: {len(reportes)}"
        )

    def crear_tarjeta(self, reporte, posicion):
        tarjeta = tk.Frame(
            self.padre,
            bd=1,
            relief="solid",
            padx=20,
            pady=15
        )
        tarjeta.pack(fill="x", pady=5)

        tk.Label(
            tarjeta,
            text=f"Reporte #{posicion}",
            font=("Arial", 14, "bold")
        ).pack(anchor="w")

        datos = vars(reporte)

        for nombre, valor in datos.items():
            tk.Label(
                tarjeta,
                text=f"{nombre}: {valor}",
                font=("Arial", 10)
            ).pack(anchor="w", pady=(2, 0))

    def limpiar(self):
        for widget in self.padre.winfo_children():
            widget.destroy()