import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timezone


class PantallaEventos:
    def __init__(self, padre, escenario, mostrar_estado):
        self.padre = padre
        self.escenario = escenario
        self.mostrar_estado = mostrar_estado

    def mostrar(self):
        self.limpiar()

        titulo = tk.Label(
            self.padre,
            text="Eventos activos",
            font=("Arial", 22, "bold")
        )
        titulo.pack(anchor="w", pady=(0, 15))

        barra = tk.Frame(self.padre)
        barra.pack(fill="x", pady=(0, 20))

        tk.Button(
            barra,
            text="+ Nuevo evento",
            font=("Arial", 10, "bold"),
            command=self.mostrar_formulario
        ).pack(side="right")

        claves = self.escenario.avl.inOrder()

        if not claves:
            tk.Label(
                self.padre,
                text="No hay eventos activos.",
                font=("Arial", 12)
            ).pack(anchor="w")

            self.mostrar_estado("No hay eventos activos")
            return

        for clave in claves:
            nodo = self.escenario.avl.encontrarNodo(clave.id_key)

            if nodo is None:
                continue

            evento = nodo.evento

            texto = (
                f"ID: {evento.id}    "
                f"M: {evento.magnitud}    "
                f"H: {evento.profundidad} km    "
                f"P: {clave.prioridad}"
            )

            tk.Label(
                self.padre,
                text=texto,
                font=("Arial", 11),
                bd=1,
                relief="solid",
                padx=15,
                pady=12
            ).pack(fill="x", pady=5)

        self.mostrar_estado(
            f"Eventos activos: {len(claves)}"
        )

    def mostrar_formulario(self):
        ventana = tk.Toplevel(self.padre)
        ventana.title("Nuevo evento")
        ventana.geometry("520x650")
        ventana.resizable(False, False)
        ventana.transient(self.padre)
        ventana.grab_set()

        contenedor = tk.Frame(
            ventana,
            padx=30,
            pady=25
        )
        contenedor.pack(fill="both", expand=True)

        tk.Label(
            contenedor,
            text="Nuevo evento",
            font=("Arial", 20, "bold")
        ).pack(anchor="w", pady=(0, 20))

        formulario = tk.Frame(contenedor)
        formulario.pack(fill="x")

        id_var = tk.StringVar()
        magnitud_var = tk.StringVar()
        profundidad_var = tk.StringVar()
        x_var = tk.StringVar()
        y_var = tk.StringVar()

        self.crear_campo(
            formulario,
            "ID del evento",
            id_var
        )

        self.crear_campo(
            formulario,
            "Magnitud",
            magnitud_var
        )

        self.crear_campo(
            formulario,
            "Profundidad (km)",
            profundidad_var
        )

        self.crear_campo(
            formulario,
            "Coordenada X",
            x_var
        )

        self.crear_campo(
            formulario,
            "Coordenada Y",
            y_var
        )

        tk.Label(
            formulario,
            text="Estación",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(12, 5))

        estaciones = self.escenario.estaciones

        opciones_estaciones = [
            estacion.id_estacion
            for estacion in estaciones
        ]

        estacion_var = tk.StringVar()

        if opciones_estaciones:
            estacion_var.set(opciones_estaciones[0])

        tk.OptionMenu(
            formulario,
            estacion_var,
            *opciones_estaciones
        ).pack(anchor="w")

        # -------------------------
        # Fecha y hora
        # -------------------------

        tk.Label(
            formulario,
            text="Fecha y hora de ocurrencia",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(18, 8))

        fecha_frame = tk.Frame(formulario)
        fecha_frame.pack(fill="x")

        anio_var = tk.IntVar(
            value=self.escenario.reloj.year
        )
        mes_var = tk.IntVar(
            value=self.escenario.reloj.month
        )
        dia_var = tk.IntVar(
            value=self.escenario.reloj.day
        )

        hora_var = tk.IntVar(
            value=self.escenario.reloj.hour
        )
        minuto_var = tk.IntVar(
            value=self.escenario.reloj.minute
        )
        segundo_var = tk.IntVar(
            value=self.escenario.reloj.second
        )

        self.crear_spinbox(
            fecha_frame,
            "Año",
            anio_var,
            2000,
            self.escenario.reloj.year
        )

        self.crear_spinbox(
            fecha_frame,
            "Mes",
            mes_var,
            1,
            12
        )

        self.crear_spinbox(
            fecha_frame,
            "Día",
            dia_var,
            1,
            31
        )

        hora_frame = tk.Frame(formulario)
        hora_frame.pack(fill="x", pady=(10, 0))

        self.crear_spinbox(
            hora_frame,
            "Hora",
            hora_var,
            0,
            23
        )

        self.crear_spinbox(
            hora_frame,
            "Minuto",
            minuto_var,
            0,
            59
        )

        self.crear_spinbox(
            hora_frame,
            "Segundo",
            segundo_var,
            0,
            59
        )

        tk.Label(
            formulario,
            text=(
                "La ocurrencia debe ser anterior o igual "
                "al reloj de simulación."
            ),
            font=("Arial", 9)
        ).pack(anchor="w", pady=(8, 0))

        # -------------------------
        # Botones
        # -------------------------

        botones = tk.Frame(contenedor)
        botones.pack(fill="x", pady=(25, 0))

        tk.Button(
            botones,
            text="Cancelar",
            command=ventana.destroy
        ).pack(side="left")

        tk.Button(
            botones,
            text="Crear evento",
            font=("Arial", 10, "bold"),
            command=lambda: self.crear_evento(
                ventana,
                id_var,
                magnitud_var,
                profundidad_var,
                x_var,
                y_var,
                estacion_var,
                anio_var,
                mes_var,
                dia_var,
                hora_var,
                minuto_var,
                segundo_var
            )
        ).pack(side="right")

    def crear_campo(self, padre, texto, variable):
        tk.Label(
            padre,
            text=texto,
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(6, 3))

        tk.Entry(
            padre,
            textvariable=variable,
            width=40
        ).pack(anchor="w")

    def crear_spinbox(
        self,
        padre,
        texto,
        variable,
        minimo,
        maximo
    ):
        frame = tk.Frame(padre)
        frame.pack(side="left", expand=True)

        tk.Label(
            frame,
            text=texto,
            font=("Arial", 9)
        ).pack()

        tk.Spinbox(
            frame,
            from_=minimo,
            to=maximo,
            textvariable=variable,
            width=7
        ).pack(pady=(4, 0))

    def crear_evento(
        self,
        ventana,
        id_var,
        magnitud_var,
        profundidad_var,
        x_var,
        y_var,
        estacion_var,
        anio_var,
        mes_var,
        dia_var,
        hora_var,
        minuto_var,
        segundo_var
    ):
        try:
            id_evento = int(id_var.get())
            magnitud = float(magnitud_var.get())
            profundidad = float(profundidad_var.get())
            x = float(x_var.get())
            y = float(y_var.get())

        except ValueError:
            messagebox.showerror(
                "Datos inválidos",
                "ID, magnitud, profundidad y coordenadas "
                "deben ser valores numéricos.",
                parent=ventana
            )
            return

        try:
            fecha = datetime(
                anio_var.get(),
                mes_var.get(),
                dia_var.get(),
                hora_var.get(),
                minuto_var.get(),
                segundo_var.get(),
                tzinfo=timezone.utc
            )

        except ValueError:
            messagebox.showerror(
                "Fecha inválida",
                "La fecha seleccionada no es válida.",
                parent=ventana
            )
            return

        if fecha > self.escenario.reloj:
            messagebox.showerror(
                "Fecha inválida",
                "La ocurrencia no puede ser posterior "
                "al reloj de simulación.",
                parent=ventana
            )
            return

        estacion = estacion_var.get()

        if not estacion:
            messagebox.showerror(
                "Estación requerida",
                "Debes seleccionar una estación.",
                parent=ventana
            )
            return

        try:
            estaciones = [estacion]
            self.escenario.crearEvento(
                id_evento,
                magnitud,
                profundidad,
                x,
                y,
                fecha,
                estaciones
            )

        except Exception as error:
            messagebox.showerror(
                "No se pudo crear el evento",
                str(error),
                parent=ventana
            )
            return

        messagebox.showinfo(
            "Evento creado",
            f"El evento {id_evento} fue creado correctamente.",
            parent=ventana
        )

        ventana.destroy()

        self.mostrar()
        self.mostrar_estado(
            f"Evento {id_evento} creado correctamente"
        )

    def limpiar(self):
        for widget in self.padre.winfo_children():
            widget.destroy()