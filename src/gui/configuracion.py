import tkinter as tk


class PantallaConfiguracion:

    def __init__(self, padre, escenario, mostrar_estado):
        self.padre = padre
        self.escenario = escenario
        self.mostrar_estado = mostrar_estado

    def mostrar(self):
        self.limpiar()

        titulo = tk.Label(
            self.padre,
            text="Configuración",
            font=("Arial", 22, "bold")
        )
        titulo.pack(anchor="w", pady=(0, 5))

        subtitulo = tk.Label(
            self.padre,
            text="Parámetros actuales de la simulación",
            font=("Arial", 11)
        )
        subtitulo.pack(anchor="w", pady=(0, 20))

        contenedor = tk.Frame(self.padre)
        contenedor.pack(fill="x")

        self.crear_parametro(
            contenedor,
            "Ventana W",
            f"{self.escenario.W} horas"
        )

        self.crear_parametro(
            contenedor,
            "Radio R",
            f"{self.escenario.R} km"
        )

        self.crear_parametro(
            contenedor,
            "Profundidad L",
            str(self.escenario.L)
        )

        self.crear_parametro(
            contenedor,
            "Antigüedad T",
            f"{self.escenario.T} horas"
        )

        tk.Label(
            self.padre,
            text="Modo de operación",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", pady=(30, 10))

        modo = (
            "Modo estrés ACTIVADO"
            if self.escenario.modo_estres
            else "Modo normal"
        )

        tk.Label(
            self.padre,
            text=modo,
            font=("Arial", 12, "bold")
        ).pack(anchor="w")

        tk.Label(
            self.padre,
            text=(
                "Los parámetros se encuentran definidos "
                "por el escenario actual."
            ),
            font=("Arial", 10)
        ).pack(anchor="w", pady=(8, 0))

        self.mostrar_estado("Configuración actualizada")

    def crear_parametro(self, padre, nombre, valor):
        tarjeta = tk.Frame(
            padre,
            bd=1,
            relief="solid",
            padx=20,
            pady=15
        )
        tarjeta.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        tk.Label(
            tarjeta,
            text=nombre,
            font=("Arial", 10)
        ).pack()

        tk.Label(
            tarjeta,
            text=valor,
            font=("Arial", 16, "bold")
        ).pack(pady=(5, 0))

    def limpiar(self):
        for widget in self.padre.winfo_children():
            widget.destroy()