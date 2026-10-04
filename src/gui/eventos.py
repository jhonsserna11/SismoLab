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
        titulo.pack(anchor="w", pady=(0, 5))

        subtitulo = tk.Label(
            self.padre,
            text="Catálogo de eventos ordenado por clave AVL (P, M, I)",
            font=("Arial", 11)
        )
        subtitulo.pack(anchor="w", pady=(0, 15))

        barra = tk.Frame(self.padre)
        barra.pack(fill="x", pady=(0, 15))

        tk.Label(
            barra,
            text="Consultar por ID:",
            font=("Arial", 10, "bold")
        ).pack(side="left")

        self.id_busqueda = tk.StringVar()

        tk.Entry(
            barra,
            textvariable=self.id_busqueda,
            width=15
        ).pack(side="left", padx=(8, 5))

        tk.Button(
            barra,
            text="Buscar",
            command=self.buscar_evento
        ).pack(side="left")

        tk.Button(
            barra,
            text="+ Nuevo evento",
            font=("Arial", 10, "bold"),
            command=self.mostrar_formulario
        ).pack(side="right")

        encabezado = tk.Frame(
            self.padre,
            bd=1,
            relief="solid"
        )
        encabezado.pack(fill="x")

        columnas = [
            ("Prioridad", 12),
            ("Magnitud", 12),
            ("ID", 12),
            ("Estado", 25),
            ("Corregir", 10)
        ]

        for nombre, ancho in columnas:
            tk.Label(
                encabezado,
                text=nombre,
                font=("Arial", 10, "bold"),
                width=ancho,
                anchor="w",
                padx=10,
                pady=8
            ).pack(side="left")

        eventos = self.escenario.avl.inOrder()

        if not eventos:
            tk.Label(
                self.padre,
                text="No hay eventos activos.",
                font=("Arial", 12)
            ).pack(anchor="w", pady=15)

            self.mostrar_estado("No hay eventos activos")
            return

        for clave in eventos:
            nodo = self.escenario.avl.encontrarNodo(clave.id_key)

            if nodo is None:
                continue

            evento = nodo.evento

            fila = tk.Frame(
                self.padre,
                bd=1,
                relief="solid"
            )
            fila.pack(fill="x", pady=1)

            datos = [
                str(clave.prioridad),
                str(clave.magnitud),
                str(clave.id_key),
                str(evento.estado)
            ]

            for dato, (_, ancho) in zip(datos, columnas[:4]):
                boton = tk.Button(
                    fila,
                    text=dato,
                    width=ancho,
                    anchor="w",
                    padx=10,
                    relief="flat",
                    command=lambda id_evento=evento.id:
                        self.mostrar_consulta(id_evento)
                )
                boton.pack(side="left")

            boton_corregir = tk.Button(
                fila,
                text="✎",
                width=columnas[4][1],
                command=lambda id_evento=evento.id:
                    self.mostrar_formulario_correccion(id_evento)
            )
            boton_corregir.pack(side="left")

        self.mostrar_estado(
            f"Eventos activos: {len(eventos)}"
        )

    def buscar_evento(self):
        texto = self.id_busqueda.get().strip()

        if not texto:
            return

        try:
            id_evento = int(texto)

        except ValueError:
            messagebox.showerror(
                "ID inválido",
                "El identificador debe ser un número entero."
            )
            return

        self.mostrar_consulta(id_evento)


    def mostrar_consulta(self, id_evento):
        try:
            datos = self.escenario.consultarEvento(id_evento)

        except ValueError as error:
            messagebox.showerror(
                "Evento no encontrado",
                str(error)
            )
            return

        ventana = tk.Toplevel(self.padre)
        ventana.title(f"Consulta del evento {id_evento}")
        ventana.geometry("650x800")
        ventana.minsize(600, 550)

        titulo = tk.Label(
            ventana,
            text=f"Evento {id_evento}",
            font=("Arial", 20, "bold")
        )
        titulo.pack(anchor="w", padx=25, pady=(20, 5))

        estado = datos["status"]

        tk.Label(
            ventana,
            text=f"Estado del registro: {estado.upper()}",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", padx=25, pady=(0, 15))

        # Archived and deleted records have no active-event details.
        if estado != "activo":
            tk.Label(
                ventana,
                text=(
                    "Este evento no pertenece actualmente "
                    "al catálogo activo."
                ),
                font=("Arial", 11)
            ).pack(anchor="w", padx=25, pady=10)

            return

        contenido = tk.Frame(ventana)
        contenido.pack(fill="both", expand=True, padx=25, pady=10)

        datos_generales = [
            ("ID", id_evento),
            ("Magnitud", datos["magnitud"]),
            ("Profundidad", f'{datos["profundidad"]} km'),
            ("Coordenadas", f'({datos["zonax"]}, {datos["zonay"]})'),
            ("Fecha y hora", datos["fecha"]),
            ("Revisión", datos["revision"]),
            ("Prioridad", datos["prioridad"]),
            ("Clave AVL", f'({datos["clave"][0]}, {datos["clave"][1]}, {datos["clave"][2]})'),
            ("Estado de atención", datos["estado"]),
            ("Poblada", "Sí" if datos["poblada"] else "No"),
            ("Profundidad del nodo", datos["profundidadNodo"]),
            ("Altura del nodo", datos["altura"]),
            ("Factor de balance", datos["factor_balance"]),
        ]

        for nombre, valor in datos_generales:
            fila = tk.Frame(contenido)
            fila.pack(fill="x", pady=3)

            tk.Label(
                fila,
                text=f"{nombre}:",
                font=("Arial", 10, "bold"),
                width=22,
                anchor="w"
            ).pack(side="left")

            tk.Label(
                fila,
                text=str(valor),
                font=("Arial", 10),
                anchor="w"
            ).pack(side="left")

        tk.Label(
            contenido,
            text="Estaciones:",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(15, 3))

        for estacion in datos["estaciones"]:
            tk.Label(
                contenido,
                text=f"• {estacion}",
                font=("Arial", 10)
            ).pack(anchor="w", padx=15)

        tk.Label(
            contenido,
            text="Asociaciones:",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(15, 3))

        candidatos = datos["asociaciones"]["candidatos"]
        asociado = datos["asociaciones"]["asociado"]

        tk.Label(
            contenido,
            text=f"Candidatos: {candidatos}",
            font=("Arial", 10)
        ).pack(anchor="w", padx=15)

        tk.Label(
            contenido,
            text=f"Asociado: {asociado if asociado is not None else 'Ninguno'}",
            font=("Arial", 10)
        ).pack(anchor="w", padx=15)

        botones = tk.Frame(ventana)
        botones.pack(pady=15)

        tk.Button(
            botones,
            text="Cerrar",
            command=ventana.destroy
        ).pack(side="left", padx=5)

    def mostrar_formulario_correccion(self, id_evento):
        try:
            datos = self.escenario.consultarEvento(id_evento)

        except ValueError as error:
            messagebox.showerror(
                "Error",
                str(error),
                parent=self.padre
            )
            return

        if datos["status"] != "activo":
            messagebox.showerror(
                "Corrección no disponible",
                "Solo se pueden corregir eventos activos.",
                parent=self.padre
            )
            return

        formulario = tk.Toplevel(self.padre)
        formulario.title(f"Corregir evento {id_evento}")
        formulario.geometry("520x800")
        formulario.resizable(False, False)
        formulario.transient(self.padre)
        formulario.grab_set()

        contenedor = tk.Frame(
            formulario,
            padx=30,
            pady=25
        )
        contenedor.pack(fill="both", expand=True)

        tk.Label(
            contenedor,
            text=f"Corregir evento {id_evento}",
            font=("Arial", 20, "bold")
        ).pack(anchor="w", pady=(0, 5))

        tk.Label(
            contenedor,
            text=(
                f"Revisión actual: {datos['revision']}  →  "
                f"nueva revisión: {datos['revision'] + 1}"
            ),
            font=("Arial", 10)
        ).pack(anchor="w", pady=(0, 20))

        formulario_campos = tk.Frame(contenedor)
        formulario_campos.pack(fill="x")

        magnitud_var = tk.StringVar(
            value=str(datos["magnitud"])
        )

        profundidad_var = tk.StringVar(
            value=str(datos["profundidad"])
        )

        x_var = tk.StringVar(
            value=str(datos["zonax"])
        )

        y_var = tk.StringVar(
            value=str(datos["zonay"])
        )

        self.crear_campo(
            formulario_campos,
            "Magnitud",
            magnitud_var
        )

        self.crear_campo(
            formulario_campos,
            "Profundidad (km)",
            profundidad_var
        )

        self.crear_campo(
            formulario_campos,
            "Coordenada X",
            x_var
        )

        self.crear_campo(
            formulario_campos,
            "Coordenada Y",
            y_var
        )

        tk.Label(
            formulario_campos,
            text="Agregar estación",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(15, 5))

        estaciones_var = tk.StringVar()

        opciones_estaciones = [
            estacion.id_estacion
            for estacion in self.escenario.estaciones
        ]

        if opciones_estaciones:
            estaciones_var.set(opciones_estaciones[0])

            tk.OptionMenu(
                formulario_campos,
                estaciones_var,
                *opciones_estaciones
            ).pack(anchor="w")
        else:
            estaciones_var.set("")

            tk.Label(
                formulario_campos,
                text="No hay estaciones adicionales disponibles."
            ).pack(anchor="w")

        tk.Label(
            formulario_campos,
            text="Fecha y hora de ocurrencia",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(18, 8))

        fecha_frame = tk.Frame(formulario_campos)
        fecha_frame.pack(fill="x")

        anio_var = tk.IntVar(value=datos["fecha"].year)
        mes_var = tk.IntVar(value=datos["fecha"].month)
        dia_var = tk.IntVar(value=datos["fecha"].day)
        hora_var = tk.IntVar(value=datos["fecha"].hour)
        minuto_var = tk.IntVar(value=datos["fecha"].minute)
        segundo_var = tk.IntVar(value=datos["fecha"].second)

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

        hora_frame = tk.Frame(formulario_campos)
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
            formulario_campos,
            text=(
                "La ocurrencia debe ser anterior o igual "
                "al reloj de simulación."
            ),
            font=("Arial", 9)
        ).pack(anchor="w", pady=(8, 0))

        botones = tk.Frame(contenedor)
        botones.pack(fill="x", pady=(25, 0))

        tk.Button(
            botones,
            text="Cancelar",
            command=formulario.destroy
        ).pack(side="left")

        tk.Button(
            botones,
            text="Corregir",
            font=("Arial", 10, "bold"),
            command=lambda: self.guardar_correccion(
                id_evento,
                formulario,
                magnitud_var,
                profundidad_var,
                x_var,
                y_var,
                anio_var,
                mes_var,
                dia_var,
                hora_var,
                minuto_var,
                segundo_var,
                estaciones_var
            )
        ).pack(side="right")

        
    
    def guardar_correccion(
        self,
        id_evento,
        formulario,
        magnitud_var,
        profundidad_var,
        x_var,
        y_var,
        anio_var,
        mes_var,
        dia_var,
        hora_var,
        minuto_var,
        segundo_var,
        estaciones_var
    ):
        try:
            magnitud = float(magnitud_var.get())
            profundidad = float(profundidad_var.get())
            x = float(x_var.get())
            y = float(y_var.get())

        except ValueError:
            messagebox.showerror(
                "Datos inválidos",
                "Magnitud, profundidad y coordenadas "
                "deben ser valores numéricos.",
                parent=formulario
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
                parent=formulario
            )
            return

        if fecha > self.escenario.reloj:
            messagebox.showerror(
                "Fecha inválida",
                "La ocurrencia no puede ser posterior "
                "al reloj de simulación.",
                parent=formulario
            )
            return

        estacion = estaciones_var.get()

        try:
            estaciones = None if not estacion else [estacion]

            self.escenario.corregirEvento(
                id_evento,
                magnitud=magnitud,
                profundidad=profundidad,
                zonax=x,
                zonay=y,
                fecha=fecha,
                estaciones=estaciones
            )

        except Exception as error:
            messagebox.showerror(
                "No se pudo corregir el evento",
                str(error),
                parent=formulario
            )
            return

        messagebox.showinfo(
            "Evento corregido",
            f"El evento {id_evento} fue corregido correctamente.",
            parent=formulario
        )

        formulario.destroy()

        self.mostrar()

        self.mostrar_estado(
            f"Evento {id_evento} corregido correctamente"
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