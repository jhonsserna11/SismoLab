import tkinter as tk


class PantallaResumen:

    def __init__(self, padre, escenario, mostrar_estado):

        self.padre = padre
        self.escenario = escenario
        self.mostrar_estado = mostrar_estado

    def mostrar(self):

        self.limpiar()

        indicadores = self.escenario.obtenerIndicadores()

        titulo = tk.Label(
            self.padre,
            text="Resumen del escenario",
            font=("Arial", 20, "bold")
        )
        titulo.pack(
            anchor="w",
            pady=(0, 20)
        )

        info = tk.Frame(self.padre)
        info.pack(fill="x")

        self.crear_indicador(
            info,
            "Eventos activos",
            indicadores["eventos_activos"],
            0,
            0
        )

        self.crear_indicador(
            info,
            "Eventos históricos",
            indicadores["eventos_historicos"],
            0,
            1
        )

        self.crear_indicador(
            info,
            "Altura AVL",
            indicadores["altura_avl"],
            0,
            2
        )

        self.crear_indicador(
            info,
            "Hojas",
            indicadores["hojas"],
            1,
            0
        )

        self.crear_indicador(
            info,
            "Pendientes",
            indicadores["eventos_pendientes"]["cantidad"],
            1,
            1
        )

        self.crear_indicador(
            info,
            "Acceso costoso",
            indicadores["eventos_costosos"]["cantidad"],
            1,
            2
        )

        estado = (
            "Activado"
            if self.escenario.modo_estres
            else "Normal"
        )

        modo = tk.Label(
            self.padre,
            text=f"Modo de ejecución: {estado}",
            font=("Arial", 13)
        )
        modo.pack(
            anchor="w",
            pady=25
        )

        parametros = tk.Label(
            self.padre,
            text=(
                f"W = {self.escenario.W} h    |    "
                f"R = {self.escenario.R} km    |    "
                f"L = {self.escenario.L}    |    "
                f"T = {self.escenario.T} h"
            ),
            font=("Arial", 12)
        )
        parametros.pack(anchor="w")

        self.mostrar_estado("Resumen actualizado")

    def crear_indicador(
        self,
        padre,
        nombre,
        valor,
        fila,
        columna
    ):

        marco = tk.Frame(
            padre,
            bd=1,
            relief="solid",
            padx=20,
            pady=15
        )

        marco.grid(
            row=fila,
            column=columna,
            padx=8,
            pady=8,
            sticky="nsew"
        )

        padre.grid_columnconfigure(
            columna,
            weight=1
        )

        nombre_label = tk.Label(
            marco,
            text=nombre,
            font=("Arial", 11)
        )
        nombre_label.pack()

        valor_label = tk.Label(
            marco,
            text=str(valor),
            font=("Arial", 20, "bold")
        )
        valor_label.pack(
            pady=(5, 0)
        )

    def limpiar(self):

        for widget in self.padre.winfo_children():
            widget.destroy()