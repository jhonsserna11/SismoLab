import json
import tkinter as tk

from tkinter import filedialog, messagebox


class PantallaCargas:

    def __init__(self, padre, escenario, mostrar_estado, actualizar_boton_estres):
        self.padre = padre
        self.escenario = escenario
        self.mostrar_estado = mostrar_estado
        self.actualizar_boton_estres = actualizar_boton_estres

    def mostrar(self):
        self.limpiar()

        titulo = tk.Label(
            self.padre,
            text="Cargas y estado",
            font=("Arial", 22, "bold")
        )
        titulo.pack(anchor="w", pady=(0, 5))

        subtitulo = tk.Label(
            self.padre,
            text="Carga escenarios desde archivos JSON o guarda el estado actual",
            font=("Arial", 11)
        )
        subtitulo.pack(anchor="w", pady=(0, 20))

        cargar_frame = tk.Frame(
            self.padre,
            bd=1,
            relief="solid",
            padx=15,
            pady=12
        )
        cargar_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        tk.Label(
            cargar_frame,
            text="Cargar archivo",
            font=("Arial", 12, "bold")
        ).pack(anchor="w")

        tk.Label(
            cargar_frame,
            text="Selecciona un archivo JSON para reconstruir el escenario según su tipo de carga.",
            font=("Arial", 10)
        ).pack(anchor="w", pady=(8, 10))

        tk.Button(
            cargar_frame,
            text="Cargar archivo",
            command=self.cargar_archivo
        ).pack(anchor="e")


        guardar_frame = tk.Frame(
            self.padre,
            bd=1,
            relief="solid",
            padx=15,
            pady=12
        )
        guardar_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        tk.Label(
            guardar_frame,
            text="Guardar estado",
            font=("Arial", 12, "bold")
        ).pack(anchor="w")

        tk.Label(
            guardar_frame,
            text="Exporta el estado completo del escenario a un archivo JSON.",
            font=("Arial", 10)
        ).pack(anchor="w", pady=(8, 10))

        tk.Button(
            guardar_frame,
            text="Guardar estado",
            command=self.guardar_estado
        ).pack(anchor="e")

    def cargar_archivo(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar archivo de carga",
            filetypes=[
                ("Archivos JSON", "*.json"),
                ("Todos los archivos", "*.*")
            ]
        )

        if not ruta:
            return

        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)

            tipo = datos.get("tipo_carga")

            if tipo == "inserciones":
                self.escenario.cargarInserciones(datos)

            elif tipo == "topologia":
                self.escenario.cargarTopologia(datos)

            elif tipo == "escenario":
                self.escenario.cargarEscenario(datos)

            else:
                raise ValueError(
                    "El archivo no contiene un tipo de carga válido."
                )

            self.actualizar_boton_estres()

            nombre_archivo = ruta.split("/")[-1]

            self.mostrar_estado(
                f"Archivo '{nombre_archivo}' cargado como {tipo}"
            )

            messagebox.showinfo(
                "Carga completada",
                f"El archivo fue cargado correctamente.\n\n"
                f"Tipo de carga: {tipo}"
            )

            self.mostrar()

        except Exception as error:
            messagebox.showerror(
                "Error al cargar archivo",
                str(error)
            )

    def guardar_estado(self):
        try:
            datos = self.escenario.guardarEscenario()

            ruta = filedialog.asksaveasfilename(
                title="Guardar estado del escenario",
                defaultextension=".json",
                filetypes=[
                    ("Archivos JSON", "*.json"),
                    ("Todos los archivos", "*.*")
                ]
            )

            if not ruta:
                return

            with open(ruta, "w", encoding="utf-8") as archivo:
                json.dump(
                    datos,
                    archivo,
                    indent=4,
                    ensure_ascii=False
                )

            self.mostrar_estado(
                "Estado del escenario guardado correctamente"
            )

            messagebox.showinfo(
                "Guardado completado",
                "El estado del escenario fue guardado correctamente."
            )

        except Exception as error:
            messagebox.showerror(
                "Error al guardar estado",
                str(error)
            )
    def limpiar(self):
        for widget in self.padre.winfo_children():
            widget.destroy()