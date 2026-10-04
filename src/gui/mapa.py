import tkinter as tk
from src.domain.Zona import Zona


class MapaSismologico:

    def __init__(self, padre, escenario):
        self.padre = padre
        self.escenario = escenario
        self.minimo = Zona.ESCENARIO_MIN
        self.maximo = Zona.ESCENARIO_MAX

        self.leyenda_creada = False

        self.ancho = 530
        self.alto = 530
        self.margen = 50

        self.contenedor = tk.Frame(padre)
        self.canvas = tk.Canvas(
            self.contenedor,
            width= 530,
            height= 530,
            bg="whitesmoke",
            highlightthickness=1
        )

    def mostrar(self):
        self.contenedor.pack(anchor="nw", pady=5)

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        if not self.leyenda_creada:
            self.crear_leyenda(self.contenedor)
            self.leyenda_creada = True

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
        self.dibujar_cuadricula()
        self.dibujar_ejes()
        self.dibujar_zonas()
        self.dibujar_eventos()

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

    def crear_leyenda(self, padre):
        leyenda = tk.Frame(
            padre,
            width=150,
            padx=10,
            pady=10
        )
        leyenda.pack(
            side="right",
            fill="y"
        )
        leyenda.pack_propagate(False)

        tk.Label(
            leyenda,
            text="Prioridad",
            font=("Arial", 9, "bold")
        ).pack(anchor="w", pady=(0, 5))

        self.crear_elemento_leyenda(
            leyenda,
            "#FFD700",
            "P1 — Baja"
        )

        self.crear_elemento_leyenda(
            leyenda,
            "#FF4500",
            "P2 — Media"
        )

        self.crear_elemento_leyenda(
            leyenda,
            "#800020",
            "P3 — Alta"
        )

    def crear_elemento_leyenda(self, padre, color, texto):
        fila = tk.Frame(padre)
        fila.pack(anchor="w", pady=2)

        tk.Label(
            fila,
            width=2,
            height=1,
            bg=color,
            relief="solid",
            bd=0
        ).pack(side="left", padx=(0, 7))

        tk.Label(
            fila,
            text=texto,
            font=("Arial", 9)
        ).pack(side="left")

    def dibujar_eventos(self):
        eventos = self.escenario.obtenerDatosMapa()

        for evento in eventos:
            x = self.convertir_x(evento["x"])
            y = self.convertir_y(evento["y"])

            prioridad = evento["prioridad"]

            if prioridad == 1:
                radio = 8
                color = "#FFD700"
            elif prioridad == 2:
                radio = 12
                color = "#FF4500"
            else:
                radio = 18
                color = "#800020"

            tag = f"evento_{evento['id']}"

            self.canvas.create_oval(
                x - radio,
                y - radio,
                x + radio,
                y + radio,
                fill=color,
                #outline="black",
                width=1,
                tags=(tag,)
            )

            self.canvas.create_text(
                x,
                y - radio - 10,
                text=str(evento["id"]),
                tags=(tag,)
            )

            self.canvas.tag_bind(
                tag,
                "<Button-1>",
                lambda event, id_evento=evento["id"]:
                    self.mostrar_evento(id_evento)
            )

            self.canvas.tag_bind(
                tag,
                "<Enter>",
                lambda event: self.canvas.config(cursor="hand2")
            )

            self.canvas.tag_bind(
                tag,
                "<Leave>",
                lambda event: self.canvas.config(cursor="")
            )

    def dibujar_cuadricula(self):
        for valor in range(100, 1000, 100):
            x = self.convertir_x(valor)
            y = self.convertir_y(valor)

            self.canvas.create_line(
                x,
                self.margen,
                x,
                self.alto - self.margen,
                fill="#D9D9D9",
                width=1
            )

            self.canvas.create_line(
                self.margen,
                y,
                self.ancho - self.margen,
                y,
                fill="#D9D9D9",
                width=1
            )