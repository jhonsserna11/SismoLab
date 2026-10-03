import tkinter as tk


class PantallaEstaciones:

    def __init__(self, padre, escenario, mostrar_estado):
        self.padre = padre
        self.escenario = escenario
        self.mostrar_estado = mostrar_estado

    def mostrar(self):
        self.limpiar()

        titulo = tk.Label(
            self.padre,
            text="Estaciones",
            font=("Arial", 22, "bold")
        )
        titulo.pack(anchor="w", pady=(0, 5))

        subtitulo = tk.Label(
            self.padre,
            text="Estaciones configuradas en el escenario",
            font=("Arial", 11)
        )
        subtitulo.pack(anchor="w", pady=(0, 20))

        estaciones = self.escenario.estaciones

        indicador = tk.Label(
            self.padre,
            text=f"{len(estaciones)} estaciones configuradas",
            font=("Arial", 12, "bold")
        )
        indicador.pack(anchor="w", pady=(0, 15))

        if not estaciones:
            tk.Label(
                self.padre,
                text="No hay estaciones configuradas.",
                font=("Arial", 12)
            ).pack(anchor="w")

            self.mostrar_estado("No hay estaciones configuradas")
            return

        contenedor = tk.Frame(self.padre)
        contenedor.pack(fill="x")

        for estacion in estaciones:
            self.crear_tarjeta(contenedor, estacion)

        self.mostrar_estado(
            f"Estaciones configuradas: {len(estaciones)}"
        )

    def crear_tarjeta(self, padre, estacion):
        tarjeta = tk.Frame(
            padre,
            bd=1,
            relief="solid",
            padx=20,
            pady=15
        )
        tarjeta.pack(fill="x", pady=5)

        tk.Label(
            tarjeta,
            text=estacion.id_estacion,
            font=("Arial", 14, "bold")
        ).pack(anchor="w")

        tk.Label(
            tarjeta,
            text=estacion.nombre,
            font=("Arial", 11)
        ).pack(anchor="w", pady=(5, 0))

    def limpiar(self):
        for widget in self.padre.winfo_children():
            widget.destroy()