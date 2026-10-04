import tkinter as tk
from src.gui.mapa import MapaSismologico


class PantallaResumen:

    def __init__(self, padre, escenario, mostrar_estado):

        self.padre = padre
        self.escenario = escenario
        self.mostrar_estado = mostrar_estado

    def mostrar(self):

        self.limpiar()

        indicadores_datos  = self.escenario.obtenerIndicadores()

        titulo = tk.Label(
            self.padre,
            text="Resumen del escenario",
            font=("Arial", 15, "bold")
        )
        titulo.pack(
            anchor="w",
            pady=(0, 20)
        )

        barra_indicadores = tk.Frame(self.padre)
        barra_indicadores.pack(
            fill="x",
            pady=(0, 15)
        )

        self.crear_indicador(
            barra_indicadores,
            "📍",
            "Activos",
            indicadores_datos["eventos_activos"]
        )

        self.crear_indicador(
            barra_indicadores,
            "📖",
            "Históricos",
            indicadores_datos["eventos_historicos"]
        )

        self.crear_indicador(
            barra_indicadores,
            "🌳",
            "Altura AVL",
            indicadores_datos["altura_avl"]
        )

        self.crear_indicador(
            barra_indicadores,
            "🍃",
            "Hojas",
            indicadores_datos["hojas"]
        )

        self.crear_indicador(
            barra_indicadores,
            "📋",
            "Pendientes",
            indicadores_datos["eventos_pendientes"]["cantidad"]
        )

        self.crear_indicador(
            barra_indicadores,
            "⚠️",
            "Costoso",
            indicadores_datos["eventos_costosos"]["cantidad"]
        )

        self.mostrar_estado("Resumen actualizado")

        contenedor_mapa = tk.Frame(self.padre)
        
        contenedor_mapa.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(10, 20)
        )

        tk.Label(
            contenedor_mapa,
            text="Mapa sísmico",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", pady=(0, 10))

        self.mapa = MapaSismologico(
            contenedor_mapa,
            self.escenario
        )

        self.mapa.mostrar()

    def crear_indicador(
        self,
        padre,
        icono,
        nombre,
        valor,
    ):
        marco = tk.Frame(
            padre,
            bd=1,
            relief="solid",
            padx=7,
            pady=5
        )

        marco.pack(
            side="left",
            fill="x",
            expand=True,
            padx=3
        )

        icono_label = tk.Label(
            marco,
            text=icono,
            font=("Arial", 11)
        )
        icono_label.pack(side="left")

        nombre_label = tk.Label(
            marco,
            text=nombre,
            font=("Arial", 9)
        )
        nombre_label.pack(side="left", padx=4)

        valor_label = tk.Label(
            marco,
            text=str(valor),
            font=("Arial", 11, "bold")
        )
        valor_label.pack(side="right")
    def limpiar(self):

        for widget in self.padre.winfo_children():
            widget.destroy()