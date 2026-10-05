import tkinter as tk
from tkinter import messagebox

class PantallaVersiones:

    def __init__(self, padre, escenario, mostrar_estado, actualizar_boton_estres):
        self.padre = padre
        self.escenario = escenario
        self.mostrar_estado = mostrar_estado
        self.actualizar_boton_estres = actualizar_boton_estres

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
            text="Guarda y restaura estados completos del escenario",
            font=("Arial", 11)
        )
        subtitulo.pack(anchor="w", pady=(0, 20))

        guardar_frame = tk.Frame(
            self.padre,
            bd=1,
            relief="solid",
            padx=15,
            pady=12
        )
        guardar_frame.pack(fill="x", pady=(0, 15))

        tk.Label(
            guardar_frame,
            text="Guardar escenario actual",
            font=("Arial", 12, "bold")
        ).pack(anchor="w")

        tk.Label(
            guardar_frame,
            text="Nombre de la versión:",
            font=("Arial", 10)
        ).pack(anchor="w", pady=(8, 3))

        entrada_frame = tk.Frame(guardar_frame)
        entrada_frame.pack(fill="x")

        self.entrada_nombre = tk.Entry(
            entrada_frame,
            font=("Arial", 10)
        )
        self.entrada_nombre.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 8)
        )

        tk.Button(
            entrada_frame,
            text="Guardar versión",
            command=self.guardar_version
        ).pack(side="right")

        tk.Label(
            self.padre,
            text="Versiones guardadas",
            font=("Arial", 13, "bold")
        ).pack(anchor="w", pady=(5, 8))

        contenedor = tk.Frame(
            self.padre,
            bd=1,
            relief="solid"
        )
        contenedor.pack(
            fill="both",
            expand=True
        )

        canvas = tk.Canvas(
            contenedor,
            highlightthickness=0
        )
        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = tk.Scrollbar(
            contenedor,
            orient="vertical",
            command=canvas.yview
        )
        scrollbar.pack(side="right", fill="y")

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        lista = tk.Frame(canvas)

        canvas_window = canvas.create_window(
            (0, 0),
            window=lista,
            anchor="nw"
        )

        lista.bind(
            "<Configure>",
            lambda event:
                canvas.configure(
                    scrollregion=canvas.bbox("all")
                )
        )

        canvas.bind(
            "<Configure>",
            lambda event:
                canvas.itemconfigure(
                    canvas_window,
                    width=event.width
                )
        )

        versiones = self.escenario.listarVersiones()

        if not versiones:
            tk.Label(
                lista,
                text="No hay versiones guardadas.",
                font=("Arial", 11)
            ).pack(
                anchor="w",
                padx=15,
                pady=15
            )
        else:
            for nombre in versiones:
                self.crear_tarjeta(
                    lista,
                    nombre
                )

        self.mostrar_estado(
            f"Versiones disponibles: {len(versiones)}"
        )
    def crear_tarjeta(self, padre, nombre):
        tarjeta = tk.Frame(
            padre,
            bd=1,
            relief="solid",
            padx=15,
            pady=10
        )
        tarjeta.pack(
            fill="x",
            padx=8,
            pady=5
        )

        tk.Label(
            tarjeta,
            text=nombre,
            font=("Arial", 11, "bold")
        ).pack(
            side="left"
        )

        tk.Button(
            tarjeta,
            text="Restaurar",
            command=lambda:
                self.confirmar_restauracion(nombre)
        ).pack(
            side="right"
        )

    def confirmar_restauracion(self, nombre):
        confirmar = messagebox.askyesno(
            "Restaurar versión",
            f"¿Confirmar restablecimiento de la versión\n"
            f"'{nombre}'?"
        )

        if not confirmar:
            return

        try:
            self.escenario.cargarVersion(nombre)
            self.actualizar_boton_estres()

            self.mostrar_estado(
                f"Versión '{nombre}' restaurada correctamente"
            )
            messagebox.showinfo(
                "Versión restaurada exitosamente",
                f"La versión {nombre} fue cargada con éxito."
            )

            self.mostrar()

        except Exception as error:
            messagebox.showerror(
                "Error al restaurar",
                str(error)
            )

    def guardar_version(self):
        nombre = self.entrada_nombre.get().strip()

        if not nombre:
            messagebox.showwarning(
                "Nombre requerido",
                "Ingresa un nombre para la versión."
            )
            return

        try:
            resultado = self.escenario.guardarVersion(nombre)

            nombre_guardado = resultado["nombre"]

            self.mostrar_estado(
                f"Versión '{nombre_guardado}' guardada correctamente"
            )
            messagebox.showinfo(
                "Versión guardada exitosamente",
                f"La versión {nombre} fue guardada con éxito."
            )

            self.mostrar()

        except Exception as error:
            messagebox.showerror(
                "No se pudo guardar la versión",
                str(error)
            )
    def limpiar(self):
        for widget in self.padre.winfo_children():
            widget.destroy()