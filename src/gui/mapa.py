import tkinter as tk
from src.domain.Zona import Zona


class MapaSismologico:

    def __init__(self, padre, escenario):
        self.padre = padre
        self.escenario = escenario
        self.minimo = Zona.ESCENARIO_MIN
        self.maximo = Zona.ESCENARIO_MAX

        self.ancho = 450
        self.alto = 450
        self.margen = 50

        self.canvas = tk.Canvas(
            padre,
            width=self.ancho,
            height=self.alto,
            bg="whitesmoke",
            highlightthickness=1
        )

    def mostrar(self):
        self.canvas.pack(fill="both", expand=True)

        self.dibujar_mapa()

    def dibujar_mapa(self):
        self.canvas.delete("all")

        x0 = self.margen
        y0 = self.margen
        x1 = self.ancho - self.margen
        y1 = self.alto - self.margen

        self.canvas.create_rectangle(
            x0,
            y0,
            x1,
            y1,
            outline="black",
            width=2
        )

        self.dibujar_ejes()
        self.dibujar_zonas()

    def convertir_x(self, x):
        escala = ( (self.ancho - 2 * self.margen) / (self.maximo - self.minimo) )
        return self.margen + (x - self.minimo) * escala

    def convertir_y(self, y):
        escala = ( (self.alto - 2 * self.margen) / (self.maximo - self.minimo) )
        return (
            self.alto - self.margen - (y - self.minimo) * escala
        )

    def dibujar_ejes(self):
        x0 = self.margen
        y0 = self.margen
        x1 = self.ancho - self.margen
        y1 = self.alto - self.margen

        self.canvas.create_text(
            x0,
            y1 + 18,
            text="0.0, 0.0",
            anchor="w"
        )

        self.canvas.create_text(
            x1,
            y1 + 18,
            text="1000.0, 0.0",
            anchor="e"
        )

        self.canvas.create_text(
            x0,
            y0 - 12,
            text="0.0, 1000.0",
            anchor="w"
        )

        self.canvas.create_text(
            x1,
            y0 - 12,
            text="1000.0, 1000.0",
            anchor="e"
        )

    def dibujar_zonas(self):
        for zona in self.escenario.zonas:

            x_min = self.convertir_x(zona.x_min)
            x_max = self.convertir_x(zona.x_max)

            y_min = self.convertir_y(zona.y_min)
            y_max = self.convertir_y(zona.y_max)

            self.canvas.create_rectangle(
                x_min,
                y_max,
                x_max,
                y_min,
                outline="gray",
                width=1
            )

            centro_x = (x_min + x_max) / 2
            centro_y = (y_min + y_max) / 2

            self.canvas.create_text(
                centro_x,
                centro_y,
                text=zona.nombre
            )