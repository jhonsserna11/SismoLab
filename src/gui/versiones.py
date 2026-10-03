import tkinter as tk
import os


class PantallaVersiones:

    def __init__(self, padre, escenario, mostrar_estado):
        self.padre = padre
        self.escenario = escenario
        self.mostrar_estado = mostrar_estado

    def mostrar(self):
        self.limpiar()

        titulo = tk.Label(
            self.padre,
            text="Versiones",
            font=("Arial", 22, "bold")
        )
        titulo.pack(anchor="w", pady=(0, 5))

        subtitulo = tk.Label(
            self.padre,
            text="Versiones guardadas del escenario",
            font=("Arial", 11)
        )
        subtitulo.pack(anchor="w", pady=(0, 20))

        carpeta = "data/versiones"

        if not os.path.exists(carpeta):
            tk.Label(
                self.padre,
                text="No existe la carpeta de versiones.",
                font=("Arial", 12)
            ).pack(anchor="w")

            self.mostrar_estado("No hay versiones disponibles")
            return

        archivos = [
            archivo
            for archivo in os.listdir(carpeta)
            if archivo.endswith(".json")
        ]

        tk.Label(
            self.padre,
            text=f"{len(archivos)} versiones guardadas",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", pady=(0, 15))

        if not archivos:
            tk.Label(
                self.padre,
                text="No hay versiones guardadas.",
                font=("Arial", 12)
            ).pack(anchor="w")

            self.mostrar_estado("No hay versiones guardadas")
            return

        for archivo in sorted(archivos):
            self.crear_tarjeta(archivo)

        self.mostrar_estado(
            f"Versiones disponibles: {len(archivos)}"
        )

    def crear_tarjeta(self, archivo):
        tarjeta = tk.Frame(
            self.padre,
            bd=1,
            relief="solid",
            padx=20,
            pady=12
        )
        tarjeta.pack(fill="x", pady=5)

        tk.Label(
            tarjeta,
            text=archivo,
            font=("Arial", 11, "bold")
        ).pack(anchor="w")

    def limpiar(self):
        for widget in self.padre.winfo_children():
            widget.destroy()