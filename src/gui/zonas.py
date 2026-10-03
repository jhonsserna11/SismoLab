import tkinter as tk


class PantallaZonas:

    def __init__(self, padre, escenario, mostrar_estado):
        self.padre = padre
        self.escenario = escenario
        self.mostrar_estado = mostrar_estado

    def mostrar(self):
        self.limpiar()

        titulo = tk.Label(
            self.padre,
            text="Zonas",
            font=("Arial", 22, "bold")
        )
        titulo.pack(anchor="w", pady=(0, 5))

        subtitulo = tk.Label(
            self.padre,
            text="Zonas configuradas en el escenario",
            font=("Arial", 11)
        )
        subtitulo.pack(anchor="w", pady=(0, 20))

        zonas = self.escenario.zonas

        indicador = tk.Label(
            self.padre,
            text=f"{len(zonas)} zonas configuradas",
            font=("Arial", 12, "bold")
        )
        indicador.pack(anchor="w", pady=(0, 15))

        if not zonas:
            tk.Label(
                self.padre,
                text="No hay zonas configuradas.",
                font=("Arial", 12)
            ).pack(anchor="w")

            self.mostrar_estado("No hay zonas configuradas")
            return

        contenedor = tk.Frame(self.padre)
        contenedor.pack(fill="x")

        for zona in zonas:
            self.crear_tarjeta(contenedor, zona)

        self.mostrar_estado(
            f"Zonas configuradas: {len(zonas)}"
        )

    def crear_tarjeta(self, padre, zona):
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
            text=zona.nombre,
            font=("Arial", 14, "bold")
        ).pack(anchor="w")

        tk.Label(
            tarjeta,
            text=f"ID: {zona.id}",
            font=("Arial", 10)
        ).pack(anchor="w", pady=(5, 0))

        tk.Label(
            tarjeta,
            text=(
                f"X: {zona.x_min} – {zona.x_max}    "
                f"Y: {zona.y_min} – {zona.y_max}"
            ),
            font=("Arial", 10)
        ).pack(anchor="w", pady=(3, 0))

        poblada = "Sí" if zona.poblada else "No"

        tk.Label(
            tarjeta,
            text=f"Zona poblada: {poblada}",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(3, 0))

    def limpiar(self):
        for widget in self.padre.winfo_children():
            widget.destroy()