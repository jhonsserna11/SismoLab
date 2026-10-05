import tkinter as tk
from tkinter import messagebox

class PantallaConfiguracion:

    def __init__(self, padre, escenario, mostrar_estado, actualizar_parametros):
        self.padre = padre
        self.escenario = escenario
        self.mostrar_estado = mostrar_estado
        self.actualizar_parametros = actualizar_parametros

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

        self.crear_parametro(contenedor, "Ventana W", self.escenario.W)
        self.crear_parametro(contenedor, "Radio R", self.escenario.R)
        self.crear_parametro(contenedor, "Profundidad L", self.escenario.L)
        self.crear_parametro(contenedor, "Antigüedad T", self.escenario.T)

        tk.Label(
            self.padre,
            text="Modo de operación",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", pady=(30, 10))

        tk.Button(
            self.padre,
            text="Aplicar cambios",
            command=self.aplicar_cambios
        ).pack(anchor="w", pady=(15, 0))

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

        entrada = tk.Entry(
            tarjeta,
            justify="center",
            font=("Arial", 14)
        )
        entrada.insert(0, str(valor))
        entrada.pack(pady=(5, 0))

        if nombre == "Ventana W":
            self.entrada_W = entrada
        elif nombre == "Radio R":
            self.entrada_R = entrada
        elif nombre == "Profundidad L":
            self.entrada_L = entrada
        elif nombre == "Antigüedad T":
            self.entrada_T = entrada

  
    def aplicar_cambios(self):
        try:
            nuevo_W = float(self.entrada_W.get())
            nuevo_R = float(self.entrada_R.get())
            nuevo_T = float(self.entrada_T.get())

            try:
                nuevo_L = int(self.entrada_L.get())
            except ValueError:
                raise ValueError("L debe ser un entero no negativo.")

            self.escenario.actualizarW(nuevo_W)
            self.escenario.actualizarR(nuevo_R)
            self.escenario.actualizarL(nuevo_L)
            self.escenario.actualizarT(nuevo_T)

            self.actualizar_parametros()

            self.mostrar_estado("Parámetros actualizados correctamente")
            self.mostrar()

        except ValueError as error:
            messagebox.showerror(
                "Error de configuración",
                str(error)
            )


    def limpiar(self):
        for widget in self.padre.winfo_children():
            widget.destroy()