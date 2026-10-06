import tkinter as tk
from tkinter import messagebox

from datetime import datetime, timezone


class PantallaConsultas:

    def __init__(self, padre, escenario, mostrar_estado):
        self.padre = padre
        self.escenario = escenario
        self.mostrar_estado = mostrar_estado

    def mostrar(self):
        self.limpiar()

        titulo = tk.Label(
            self.padre,
            text="Consultas y análisis",
            font=("Arial", 22, "bold")
        )
        titulo.pack(anchor="w", pady=(0, 5))

        subtitulo = tk.Label(
            self.padre,
            text="Consultas sobre eventos activos e históricos",
            font=("Arial", 11)
        )
        subtitulo.pack(anchor="w", pady=(0, 20))

        contenedor_scroll = tk.Frame(self.padre)
        contenedor_scroll.pack(fill="both", expand=True)

        canvas = tk.Canvas(
            contenedor_scroll,
            highlightthickness=0
        )
        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        barra = tk.Scrollbar(
            contenedor_scroll,
            orient="vertical",
            command=canvas.yview
        )
        barra.pack(
            side="right",
            fill="y"
        )

        canvas.configure(
            yscrollcommand=barra.set
        )

        contenido = tk.Frame(canvas)

        ventana_contenido = canvas.create_window(
            (0, 0),
            window=contenido,
            anchor="nw"
        )

        def actualizar_scroll(evento):
            canvas.configure(
                scrollregion=canvas.bbox("all")
            )

        contenido.bind(
            "<Configure>",
            actualizar_scroll
        )

        def ajustar_ancho(evento):
            canvas.itemconfig(
                ventana_contenido,
                width=evento.width
            )

        canvas.bind(
            "<Configure>",
            ajustar_ancho
        )

        def desplazar(evento):
            canvas.yview_scroll(
                int(-1 * (evento.delta / 120)),
                "units"
            )

        canvas.bind(
            "<MouseWheel>",
            desplazar
        )

        contenido.bind(
            "<MouseWheel>",
            desplazar
        )

        # =====================================================
        # TOP PENDING EVENTS
        # =====================================================

        tarjeta_pendientes = tk.Frame(
            contenido,
            bd=1,
            relief="solid",
            padx=15,
            pady=12
        )
        tarjeta_pendientes.pack(
            fill="x",
            pady=(0, 15)
        )
        tk.Label(
            tarjeta_pendientes,
            text="Primeros eventos pendientes",
            font=("Arial", 14, "bold")
        ).pack(
            anchor="w",
            padx=5,
            pady=(5, 10)
        )

        tk.Label(
            tarjeta_pendientes,
            text="Cantidad de eventos (k):"
        ).pack(
            anchor="w",
            padx=5
        )

        k_var = tk.StringVar(value="5")

        tk.Entry(
            tarjeta_pendientes,
            textvariable=k_var,
            width=15
        ).pack(
            anchor="w",
            padx=5,
            pady=(3, 8)
        )

        resultado_pendientes = tk.Label(
            tarjeta_pendientes,
            text="",
            justify="left",
            anchor="w",
            font=("Arial", 10),
            wraplength=1000
        )
        resultado_pendientes.pack(
            anchor="w",
            padx=5,
            pady=(5, 20)
        )

        def consultar_pendientes():
            try:
                k = int(k_var.get())

                resultado = self.escenario.consultarPrimerosPendientes(k)

                texto = (
                    f"Nodos AVL examinados: "
                    f"{resultado['nodos_avl_examinados']}\n\n"
                )

                if not resultado["eventos"]:
                    texto += "No hay eventos pendientes."
                else:
                    texto += "Eventos:\n"

                    for evento in resultado["eventos"]:
                        texto += (
                            f"ID: {evento['id']} | "
                            f"Prioridad: {evento['prioridad']} | "
                            f"Magnitud: {evento['magnitud']} | "
                            f"Estado: {evento['estado']}\n"
                        )

                resultado_pendientes.config(
                    text=texto
                )

                self.mostrar_estado(
                    "Consulta de eventos pendientes realizada"
                )

            except (ValueError, TypeError) as error:
                messagebox.showerror(
                    "Consulta inválida",
                    str(error)
                )

        tk.Button(
            tarjeta_pendientes,
            text="Consultar",
            command=consultar_pendientes
        ).pack(
            anchor="w",
            padx=5,
            pady=(0, 20)
        )

        self.mostrar_estado("Consultas listas")

        # =====================================================
        # EVENTS WITHIN A MAGNITUDE RANGE
        # =====================================================

        tarjeta_magnitud = tk.Frame(
            contenido,
            bd=1,
            relief="solid",
            padx=15,
            pady=12
        )
        tarjeta_magnitud.pack(
            fill="x",
            pady=(0, 15)
        )
        tk.Label(
            tarjeta_magnitud,
            text="Eventos por intervalo de magnitud",
            font=("Arial", 14, "bold")
        ).pack(
            anchor="w",
            padx=5,
            pady=(20, 10)
        )

        tk.Label(
            tarjeta_magnitud,
            text="Magnitud mínima:"
        ).pack(
            anchor="w",
            padx=5
        )

        magnitud_min_var = tk.StringVar(value="4.0")

        tk.Entry(
            tarjeta_magnitud,
            textvariable=magnitud_min_var,
            width=15
        ).pack(
            anchor="w",
            padx=5,
            pady=(3, 8)
        )

        tk.Label(
            tarjeta_magnitud,
            text="Magnitud máxima:"
        ).pack(
            anchor="w",
            padx=5
        )

        magnitud_max_var = tk.StringVar(value="6.0")

        tk.Entry(
            tarjeta_magnitud,
            textvariable=magnitud_max_var,
            width=15
        ).pack(
            anchor="w",
            padx=5,
            pady=(3, 8)
        )

        resultado_magnitud = tk.Label(
            tarjeta_magnitud,
            text="",
            justify="left",
            anchor="w",
            font=("Arial", 10),
            wraplength=1000
        )
        resultado_magnitud.pack(
            anchor="w",
            padx=5,
            pady=(5, 10)
        )

        def consultar_magnitud():
            try:
                minimo = magnitud_min_var.get()
                maximo = magnitud_max_var.get()

                resultado = self.escenario.consultarPorMagnitud(
                    minimo,
                    maximo
                )

                texto = (
                    f"Intervalo: "
                    f"[{resultado['intervalo'][0]}, "
                    f"{resultado['intervalo'][1]}]\n"
                    f"Nodos AVL examinados: "
                    f"{resultado['nodos_avl_examinados']}\n\n"
                )

                if not resultado["eventos"]:
                    texto += "No hay eventos dentro del intervalo."
                else:
                    texto += "Eventos:\n"

                    for evento in resultado["eventos"]:
                        texto += (
                            f"ID: {evento['id']} | "
                            f"Prioridad: {evento['prioridad']} | "
                            f"Magnitud: {evento['magnitud']} | "
                            f"Estado: {evento['estado']}\n"
                        )

                resultado_magnitud.config(
                    text=texto
                )

                self.mostrar_estado(
                    "Consulta por magnitud realizada"
                )

            except (ValueError, TypeError) as error:
                messagebox.showerror(
                    "Consulta inválida",
                    str(error)
                )

        tk.Button(
            tarjeta_magnitud,
            text="Consultar",
            command=consultar_magnitud
        ).pack(
            anchor="w",
            padx=5,
            pady=(0, 20)
        )

        tarjeta_profundidad = tk.Frame(
            contenido,
            bd=1,
            relief="solid",
            padx=15,
            pady=12
        )
        tarjeta_profundidad.pack(
            fill="x",
            pady=(0, 15)
        )

        tk.Label(
            tarjeta_profundidad,
            text="Eventos por profundidad y fechas",
            font=("Arial", 16, "bold")
        ).pack(anchor="w", pady=(20, 3))

        tk.Label(
            tarjeta_profundidad,
            text="Consulta eventos con profundidad menor o igual al límite dentro de un intervalo inclusivo de fechas.",
            font=("Arial", 10)
        ).pack(anchor="w", pady=(0, 8))


        formulario = tk.Frame(contenido)
        formulario.pack(fill="x", pady=(0, 8))

        profundidad_var = tk.StringVar(value="100")

        tk.Label(
            tarjeta_profundidad,
            text="Profundidad máxima (km)",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(0, 3))

        tk.Entry(
            tarjeta_profundidad,
            textvariable=profundidad_var,
            width=15
        ).pack(anchor="w")

        tk.Label(
            tarjeta_profundidad,
            text="Fecha inicial",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(12, 5))

        fecha_inicio_frame = tk.Frame(tarjeta_profundidad)
        fecha_inicio_frame.pack(fill="x")

        anio_inicio_var = tk.StringVar(value="2026")
        mes_inicio_var = tk.StringVar(value="1")
        dia_inicio_var = tk.StringVar(value="1")

        self.crear_spinbox(
            fecha_inicio_frame,
            "Año",
            anio_inicio_var,
            2000,
            self.escenario.reloj.year
        )

        self.crear_spinbox(
            fecha_inicio_frame,
            "Mes",
            mes_inicio_var,
            1,
            12
        )

        self.crear_spinbox(
            fecha_inicio_frame,
            "Día",
            dia_inicio_var,
            1,
            31
        )

        hora_inicio_frame = tk.Frame(tarjeta_profundidad)
        hora_inicio_frame.pack(fill="x", pady=(8, 0))

        hora_inicio_var = tk.StringVar(value="0")
        minuto_inicio_var = tk.StringVar(value="0")
        segundo_inicio_var = tk.StringVar(value="0")

        self.crear_spinbox(
            hora_inicio_frame,
            "Hora",
            hora_inicio_var,
            0,
            23
        )

        self.crear_spinbox(
            hora_inicio_frame,
            "Minuto",
            minuto_inicio_var,
            0,
            59
        )

        self.crear_spinbox(
            hora_inicio_frame,
            "Segundo",
            segundo_inicio_var,
            0,
            59
        )

        tk.Label(
            tarjeta_profundidad,
            text="Fecha final",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(15, 5))

        fecha_fin_frame = tk.Frame(tarjeta_profundidad)
        fecha_fin_frame.pack(fill="x")

        anio_fin_var = tk.StringVar(value=self.escenario.reloj.year)
        mes_fin_var = tk.StringVar(value=self.escenario.reloj.month)
        dia_fin_var = tk.StringVar(value=self.escenario.reloj.day)

        self.crear_spinbox(
            fecha_fin_frame,
            "Año",
            anio_fin_var,
            2000,
            self.escenario.reloj.year
        )

        self.crear_spinbox(
            fecha_fin_frame,
            "Mes",
            mes_fin_var,
            1,
            12
        )

        self.crear_spinbox(
            fecha_fin_frame,
            "Día",
            dia_fin_var,
            1,
            31
        )

        hora_fin_frame = tk.Frame(tarjeta_profundidad)
        hora_fin_frame.pack(fill="x", pady=(8, 0))

        hora_fin_var = tk.StringVar(value=self.escenario.reloj.hour)
        minuto_fin_var = tk.StringVar(value=self.escenario.reloj.minute)
        segundo_fin_var = tk.StringVar(value=self.escenario.reloj.second)

        self.crear_spinbox(
            hora_fin_frame,
            "Hora",
            hora_fin_var,
            0,
            23
        )

        self.crear_spinbox(
            hora_fin_frame,
            "Minuto",
            minuto_fin_var,
            0,
            59
        )

        self.crear_spinbox(
            hora_fin_frame,
            "Segundo",
            segundo_fin_var,
            0,
            59
        )
        resultados_frame = None
        def ejecutar_consulta_profundidad():
            try:
                profundidad = float(profundidad_var.get())

                fecha_inicio = datetime(
                    int(anio_inicio_var.get()),
                    int(mes_inicio_var.get()),
                    int(dia_inicio_var.get()),
                    int(hora_inicio_var.get()),
                    int(minuto_inicio_var.get()),
                    int(segundo_inicio_var.get()),
                    tzinfo=timezone.utc
                )

                fecha_fin = datetime(
                    int(anio_fin_var.get()),
                    int(mes_fin_var.get()),
                    int(dia_fin_var.get()),
                    int(hora_fin_var.get()),
                    int(minuto_fin_var.get()),
                    int(segundo_fin_var.get()),
                    tzinfo=timezone.utc
                )

                resultado = self.escenario.consultarPorProfundidadYFechas(
                    profundidad,
                    fecha_inicio,
                    fecha_fin
                )

                nonlocal resultados_frame

                if resultados_frame is not None:
                    resultados_frame.destroy()
                resultados_frame = tk.Frame(tarjeta_profundidad)
                resultados_frame.pack(fill="x", pady=(10, 0))

                tk.Label(
                    resultados_frame,
                    text=f"Nodos AVL examinados: {resultado['nodos_avl_examinados']}",
                    font=("Arial", 10, "bold")
                ).pack(anchor="w")

                if not resultado["eventos"]:
                    tk.Label(
                        resultados_frame,
                        text="No se encontraron eventos.",
                        font=("Arial", 10)
                    ).pack(anchor="w", pady=5)
                    return

                for evento in resultado["eventos"]:
                    tk.Label(
                        resultados_frame,
                        text=(
                            f"ID: {evento['id']} | "
                            f"Magnitud: {evento['magnitud']} | "
                            f"Profundidad: {evento['profundidad']} | "
                            f"Estado: {evento['estado']}"
                        ),
                        font=("Arial", 10)
                    ).pack(anchor="w", pady=2)

                self.mostrar_estado(
                    "Consulta de profundidad y fechas realizada"
                )

            except (ValueError, TypeError) as error:
                messagebox.showerror(
                    "Datos inválidos",
                    str(error)
                )

        tk.Button(
            tarjeta_profundidad,
            text="Consultar",
            font=("Arial", 10, "bold"),
            command=ejecutar_consulta_profundidad
        ).pack(anchor="w", pady=(10, 0))

        tarjeta_asociaciones = tk.Frame(
            contenido,
            bd=1,
            relief="solid",
            padx=15,
            pady=12
        )
        tarjeta_asociaciones.pack(
            fill="x",
            pady=(0, 15)
        )
        tk.Label(
            tarjeta_asociaciones,
            text="Asociaciones de un evento",
            font=("Arial", 16, "bold")
        ).pack(anchor="w", pady=(20, 3))

        tk.Label(
            tarjeta_asociaciones,
            text="Consulta candidatos, referencia elegida y eventos que utilizan este evento como referencia.",
            font=("Arial", 10)
        ).pack(anchor="w", pady=(0, 8))

        formulario_asociacion = tk.Frame(tarjeta_asociaciones)
        formulario_asociacion.pack(fill="x", pady=(0, 8))

        id_asociacion_var = tk.StringVar()

        tk.Label(
            formulario_asociacion,
            text="ID del evento",
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(0, 3))

        tk.Entry(
            formulario_asociacion,
            textvariable=id_asociacion_var,
            width=15
        ).pack(anchor="w")

        resultados_asociacion = None

        def ejecutar_consulta_asociacion():
            nonlocal resultados_asociacion

            if resultados_asociacion is not None:
                resultados_asociacion.destroy()

            try:
                id_evento = int(id_asociacion_var.get())

                resultado = self.escenario.consultarAsociaciones(
                    id_evento
                )

                resultados_asociacion = tk.Frame(tarjeta_asociaciones)
                resultados_asociacion.pack(
                    fill="x",
                    pady=(10, 0)
                )

                evento = resultado["evento"]

                tk.Label(
                    resultados_asociacion,
                    text=(
                        f"Evento consultado: {evento['id']} | "
                        f"Estado: {evento['estado']}"
                    ),
                    font=("Arial", 10, "bold")
                ).pack(anchor="w")

                tk.Label(
                    resultados_asociacion,
                    text="Candidatos:",
                    font=("Arial", 10, "bold")
                ).pack(anchor="w", pady=(8, 2))

                if resultado["candidatos"]:
                    for candidato in resultado["candidatos"]:
                        tk.Label(
                            resultados_asociacion,
                            text=(
                                f"ID: {candidato['id']} | "
                                f"Estado: {candidato['estado']}"
                            ),
                            font=("Arial", 10)
                        ).pack(anchor="w", pady=1)
                else:
                    tk.Label(
                        resultados_asociacion,
                        text="No tiene candidatos.",
                        font=("Arial", 10)
                    ).pack(anchor="w")

                tk.Label(
                    resultados_asociacion,
                    text="Referencia elegida:",
                    font=("Arial", 10, "bold")
                ).pack(anchor="w", pady=(8, 2))

                referencia = resultado["referencia_elegida"]

                if referencia is not None:
                    tk.Label(
                        resultados_asociacion,
                        text=(
                            f"ID: {referencia['id']} | "
                            f"Estado: {referencia['estado']}"
                        ),
                        font=("Arial", 10)
                    ).pack(anchor="w")
                else:
                    tk.Label(
                        resultados_asociacion,
                        text="No tiene referencia elegida.",
                        font=("Arial", 10)
                    ).pack(anchor="w")

                tk.Label(
                    resultados_asociacion,
                    text="Eventos que lo utilizan como referencia:",
                    font=("Arial", 10, "bold")
                ).pack(anchor="w", pady=(8, 2))

                if resultado["referenciado_por"]:
                    for evento_referenciado in resultado["referenciado_por"]:
                        tk.Label(
                            resultados_asociacion,
                            text=(
                                f"ID: {evento_referenciado['id']} | "
                                f"Estado: {evento_referenciado['estado']}"
                            ),
                            font=("Arial", 10)
                        ).pack(anchor="w", pady=1)
                else:
                    tk.Label(
                        resultados_asociacion,
                        text="Ningún evento lo utiliza como referencia.",
                        font=("Arial", 10)
                    ).pack(anchor="w")

                tk.Label(
                    resultados_asociacion,
                    text=(
                        f"Nodos AVL examinados: "
                        f"{resultado['nodos_avl_examinados']}"
                    ),
                    font=("Arial", 10, "bold")
                ).pack(anchor="w", pady=(10, 0))

                self.mostrar_estado(
                    "Consulta de asociaciones realizada"
                )

            except (ValueError, TypeError) as error:
                messagebox.showerror(
                    "Datos inválidos",
                    str(error)
                )

        tk.Button(
            formulario_asociacion,
            text="Consultar",
            font=("Arial", 10, "bold"),
            command=ejecutar_consulta_asociacion
        ).pack(anchor="w", pady=(10, 0))


        tarjeta_costosos = tk.Frame(
            contenido,
            bd=1,
            relief="solid",
            padx=15,
            pady=12
        )
        tarjeta_costosos.pack(
            fill="x",
            pady=(0, 15)
        )
        tk.Label(
            tarjeta_costosos,
            text="Eventos de prioridad alta con acceso costoso",
            font=("Arial", 16, "bold")
        ).pack(anchor="w", pady=(20, 3))

        tk.Label(
            tarjeta_costosos,
            text="Muestra eventos de prioridad alta cuya profundidad en el AVL supera el límite configurado.",
            font=("Arial", 10)
        ).pack(anchor="w", pady=(0, 8))

        resultados_costosos = None

        def ejecutar_consulta_costosos():
            nonlocal resultados_costosos

            if resultados_costosos is not None:
                resultados_costosos.destroy()

            try:
                resultado = self.escenario.consultarEventosCostosos()

                resultados_costosos = tk.Frame(tarjeta_costosos)
                resultados_costosos.pack(
                    fill="x",
                    pady=(10, 0)
                )

                tk.Label(
                    resultados_costosos,
                    text=(
                        f"Nodos AVL examinados: "
                        f"{resultado['nodos_avl_examinados']}"
                    ),
                    font=("Arial", 10, "bold")
                ).pack(anchor="w")

                tk.Label(
                    resultados_costosos,
                    text=f"Límite de profundidad: {resultado['limite']}",
                    font=("Arial", 10)
                ).pack(anchor="w", pady=(2, 0))

                if not resultado["eventos"]:
                    tk.Label(
                        resultados_costosos,
                        text="No hay eventos de prioridad alta con acceso costoso.",
                        font=("Arial", 10)
                    ).pack(anchor="w", pady=5)
                    self.mostrar_estado(
                        "Consulta de eventos costosos realizada"
                    )
                    return

                tk.Label(
                    resultados_costosos,
                    text=f"Cantidad de eventos: {resultado['cantidad']}",
                    font=("Arial", 10, "bold")
                ).pack(anchor="w", pady=(8, 3))

                for evento in resultado["eventos"]:
                    tk.Label(
                        resultados_costosos,
                        text=(
                            f"ID: {evento['id']} | "
                            f"Magnitud: {evento['magnitud']} | "
                            f"Profundidad del hipocentro: {evento['profundidad']} | "
                            f"Prioridad: {evento['prioridad']} | "
                            f"Profundidad del nodo: {evento['profundidad_nodo']} | "
                            f"Nodos visitados en su busqueda por clave: "
                            f"{evento['nodos_visitados_busqueda']} | "
                            f"Estado: {evento['estado']}"
                        ),
                        font=("Arial", 10)
                    ).pack(anchor="w", pady=2)

                self.mostrar_estado(
                    "Consulta de eventos costosos realizada"
                )

            except (ValueError, TypeError) as error:
                messagebox.showerror(
                    "Error en la consulta",
                    str(error)
                )

        tk.Button(
            tarjeta_costosos,
            text="Consultar",
            font=("Arial", 10, "bold"),
            command=ejecutar_consulta_costosos
        ).pack(anchor="w", pady=(10, 0))
    def limpiar(self):
        for widget in self.padre.winfo_children():
            widget.destroy()
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