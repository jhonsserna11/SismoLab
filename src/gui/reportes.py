import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from datetime import datetime, timezone


class PantallaReportes:

    def __init__(self, padre, escenario, mostrar_estado):
        self.padre = padre
        self.escenario = escenario
        self.mostrar_estado = mostrar_estado

        self.rafaga_activa = False
        self.rafaga_pausada = False
        self.rafaga_id = None
        self.segundos_restantes = 5
        self.panel_rafaga = None
        self.label_contador_rafaga = None

    def mostrar(self):
        self.limpiar()

        titulo = tk.Label(
            self.padre,
            text="Reportes",
            font=("Arial", 22, "bold")
        )
        titulo.pack(anchor="w", pady=(0, 5))

        subtitulo = tk.Label(
            self.padre,
            text="Cola de reportes pendientes",
            font=("Arial", 11)
        )
        subtitulo.pack(anchor="w", pady=(0, 20))

        reportes = list(self.escenario.cola_reportes)

        indicador = tk.Label(
            self.padre,
            text=f"{len(reportes)} reportes pendientes",
            font=("Arial", 12, "bold")
        )
        indicador.pack(anchor="w", pady=(0, 15))

        if not reportes:
            tk.Label(
                self.padre,
                text="No hay reportes pendientes.",
                font=("Arial", 12)
            ).pack(anchor="w")

            self.mostrar_estado("No hay reportes pendientes")
            return

        contenedor_cola = tk.Frame(self.padre)
        contenedor_cola.pack(
            fill="x",
            pady=(5, 20)
        )
        barra_acciones = tk.Frame(self.padre)
        barra_acciones.pack(fill="x", pady=(0, 10))

        boton_procesar = tk.Button(
            barra_acciones,
            text="▶ Procesar siguiente",
            command=self.procesar_siguiente
        )
        boton_procesar.pack(side="left")

        boton_rafaga = tk.Button(
            barra_acciones,
            text="▶ Iniciar Ráfaga",
            command=self.iniciar_rafaga
        )
        boton_rafaga.pack(side="left", padx=(10, 0))

        boton_preparar = tk.Button(
            barra_acciones,
            text="＋ Preparar reporte",
            command=self.preparar_reporte
        )
        boton_preparar.pack(side="right")

        canvas = tk.Canvas(
            contenedor_cola,
            height=260,
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            contenedor_cola,
            orient="horizontal",
            command=canvas.xview
        )

        contenido = tk.Frame(canvas)

        contenido.bind(
            "<Configure>",
            lambda event: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window(
            (0, 0),
            window=contenido,
            anchor="nw"
        )

        canvas.configure(
            xscrollcommand=scrollbar.set
        )

        canvas.pack(
            fill="x",
            expand=True
        )

        scrollbar.pack(
            fill="x"
        )

        if self.rafaga_activa:
            self.mostrar_panel_rafaga()

        for posicion, reporte in enumerate(reportes, start=1):

            self.crear_tarjeta(
                contenido,
                reporte,
                posicion,
                posicion == 1
            )

            if posicion < len(reportes):
                tk.Label(
                    contenido,
                    text="←",
                    font=("Arial", 20, "bold")
                ).pack(
                    side="left",
                    padx=8
                )

        self.mostrar_estado(
            f"Reportes pendientes: {len(reportes)}"
        )

    def procesar_siguiente(self):
        resultado = self.escenario.procesarSiguienteReporte()

        if resultado is None:
            messagebox.showinfo(
                "Procesar reporte",
                "No hay reportes pendientes."
            )
            return

        rotaciones = resultado["rotaciones"]

        rotaciones_mostradas = [
            f"{tipo}: {cantidad}"
            for tipo, cantidad in rotaciones.items()
            if cantidad > 0
        ]

        if rotaciones_mostradas:
            texto_rotaciones = "\n".join(rotaciones_mostradas)
        else:
            texto_rotaciones = "Ninguna"

        messagebox.showinfo(
            "Resultado del reporte",
            f"Evento: {resultado['evento']}\n\n"
            f"Estación: {resultado['estacion']}\n"
            f"Revisión: {resultado['revision']}\n\n"
            f"Decisión: {resultado['decision']}\n\n"
            f"Rotaciones producidas:\n"
            f"{texto_rotaciones}"
        )

        self.mostrar()

    def iniciar_rafaga(self):
        if self.rafaga_activa:
            return

        if not self.escenario.cola_reportes:
            self.mostrar_estado("No hay reportes pendientes para iniciar una ráfaga.")
            return

        self.rafaga_activa = True
        self.rafaga_pausada = False

        self.procesar_reporte_rafaga()

    def pausar_rafaga(self):
        if not self.rafaga_activa:
            return

        self.rafaga_pausada = True

        if self.rafaga_id is not None:
            self.padre.after_cancel(self.rafaga_id)
            self.rafaga_id = None

        if self.label_contador_rafaga is not None:
            self.label_contador_rafaga.config(
                text=f"Ráfaga pausada — {self.segundos_restantes} s restantes"
            )
        self.mostrar_controles_rafaga()

    def reanudar_rafaga(self):
        if not self.rafaga_activa or not self.rafaga_pausada:
            return
        self.rafaga_pausada = False
        self.actualizar_contador_rafaga()
        self.mostrar_controles_rafaga()

    def terminar_rafaga(self):
        if self.rafaga_id is not None:
            self.padre.after_cancel(self.rafaga_id)
            self.rafaga_id = None

        self.rafaga_activa = False
        self.rafaga_pausada = False
        self.segundos_restantes = 5

        self.ocultar_panel_rafaga()
        self.mostrar()

    def procesar_reporte_rafaga(self):
        if not self.rafaga_activa or self.rafaga_pausada:
            return

        if not self.escenario.cola_reportes:
            self.terminar_rafaga()
            return

        resultado = self.escenario.procesarSiguienteReporte()

        self.mostrar()

        self.mostrar_resultado_rafaga(resultado)

        if not self.escenario.cola_reportes:
            self.terminar_rafaga()
            return

        self.segundos_restantes = 5
        self.actualizar_contador_rafaga()

    def mostrar_panel_rafaga(self):
        self.panel_rafaga = tk.Frame(
            self.padre,
            bd=1,
            relief="solid",
            padx=15,
            pady=12
        )
        self.panel_rafaga.pack(
            fill="x",
            pady=(0, 15)
        )

        titulo = tk.Label(
            self.panel_rafaga,
            text="Reporte actual procesado:",
            font=("Arial", 14, "bold")
        )
        titulo.pack(anchor="w")

        self.label_resultado_rafaga = tk.Label(
            self.panel_rafaga,
            text="",
            font=("Arial", 11),
            justify="left"
        )
        self.label_resultado_rafaga.pack(
            anchor="w",
            pady=(10, 5)
        )

        self.label_contador_rafaga = tk.Label(
            self.panel_rafaga,
            text="",
            font=("Arial", 11, "bold")
        )
        self.label_contador_rafaga.pack(
            anchor="w",
            pady=(5, 10)
        )

        self.mostrar_controles_rafaga()

    def mostrar_resultado_rafaga(self, resultado):
        if self.panel_rafaga is None:
            self.mostrar_panel_rafaga()

        rotaciones = resultado["rotaciones"]

        rotaciones_mostradas = [
            f"{tipo}: {cantidad}"
            for tipo, cantidad in rotaciones.items()
            if cantidad > 0
        ]

        if rotaciones_mostradas:
            texto_rotaciones = ", ".join(rotaciones_mostradas)
        else:
            texto_rotaciones = "Ninguna"

        texto = (
            f"Estación: {resultado['estacion']}\n"
            f"Evento: {resultado['evento']}\n"
            f"Revisión: {resultado['revision']}\n"
            f"Decisión: {resultado['decision']}\n"
            f"Rotaciones producidas: {texto_rotaciones}"
        )

        self.label_resultado_rafaga.config(
            text=texto
        )

    def mostrar_controles_rafaga(self):
        if self.panel_rafaga is None:
            return

        for widget in self.panel_rafaga.winfo_children():
            if getattr(widget, "es_controles_rafaga", False):
                widget.destroy()

        controles = tk.Frame(self.panel_rafaga)
        controles.pack(
            fill="x",
            pady=(5, 0)
        )

        controles.es_controles_rafaga = True

        if self.rafaga_pausada:
            boton_pausa = tk.Button(
                controles,
                text="▶ Reanudar",
                command=self.reanudar_rafaga
            )
        else:
            boton_pausa = tk.Button(
                controles,
                text="⏸ Pausar",
                command=self.pausar_rafaga
            )

        boton_pausa.pack(side="left")

        boton_terminar = tk.Button(
            controles,
            text="⏹ Terminar ráfaga",
            command=self.terminar_rafaga
        )
        boton_terminar.pack(
            side="left",
            padx=(10, 0)
        )    

    def ocultar_panel_rafaga(self):
        if self.panel_rafaga is not None:
            self.panel_rafaga.destroy()
            self.panel_rafaga = None

        self.label_resultado_rafaga = None
        self.label_contador_rafaga = None

    def actualizar_contador_rafaga(self):
        if not self.rafaga_activa or self.rafaga_pausada:
            return

        if self.segundos_restantes <= 0:
            self.procesar_reporte_rafaga()
            return

        if self.label_contador_rafaga is not None:
            self.label_contador_rafaga.config(
                text=f"Próximo procesamiento en: {self.segundos_restantes} s"
            )

        self.segundos_restantes -= 1

        self.rafaga_id = self.padre.after(
            1000,
            self.actualizar_contador_rafaga
        )


    def crear_tarjeta(self, padre, reporte, posicion, siguiente):

        if siguiente:
            fondo = "#EEF4FF"
            borde = "#4169E1"
        else:
            fondo = "#F7F7F7"
            borde = "#BDBDBD"

        tarjeta = tk.Frame(
            padre,
            bg=fondo,
            bd=1,
            relief="solid",
            highlightbackground=borde,
            highlightcolor=borde,
            highlightthickness=1,
            padx=18,
            pady=12
        )

        tarjeta.pack(
            side="left",
            padx=5
        )

        if siguiente:
            tk.Label(
                tarjeta,
                text="SIGUIENTE",
                bg=fondo,
                fg="#4169E1",
                font=("Arial", 9, "bold")
            ).pack(anchor="w", pady=(0, 5))

        tk.Label(
            tarjeta,
            text=f"Evento: {reporte.id_evento}",
            bg=fondo,
            font=("Arial", 10)
        ).pack(anchor="w", pady=(8, 0))

        tk.Label(
            tarjeta,
            text=f"Estación: {reporte.estacion}",
            bg=fondo,
            font=("Arial", 10)
        ).pack(anchor="w")

        tk.Label(
            tarjeta,
            text=f"Revisión: {reporte.nRevision}",
            bg=fondo,
            font=("Arial", 10)
        ).pack(anchor="w")

        tk.Label(
            tarjeta,
            text=f"Magnitud: {reporte.magnitud}",
            bg=fondo,
            font=("Arial", 10)
        ).pack(anchor="w")

    def preparar_reporte(self):
        ventana = tk.Toplevel(self.padre)
        ventana.title("Preparar reporte")
        ventana.geometry("450x600")
        ventana.resizable(False, False)

        tk.Label(
            ventana,
            text="Preparar reporte",
            font=("Arial", 18, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        tk.Label(
            ventana,
            text="El reporte será agregado a la cola FIFO.",
            font=("Arial", 10)
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )

        formulario = tk.Frame(ventana)

        formulario.pack(
            fill="x",
            padx=20
        )

        campos = {}

        datos = [
            ("ID evento", "id_evento"),
            ("Revisión", "revision"),
            ("Magnitud", "magnitud"),
            ("Profundidad", "profundidad"),
            ("Coordenada X", "zonax"),
            ("Coordenada Y", "zonay"),
            
        ]

        for texto, clave in datos:
            fila = tk.Frame(formulario)
            fila.pack(
                fill="x",
                pady=4
            )

            tk.Label(
                fila,
                text=texto,
                width=18,
                anchor="w"
            ).pack(side="left")

            entrada = tk.Entry(fila)
            entrada.pack(
                side="left",
                fill="x",
                expand=True
            )

            campos[clave] = entrada

        tk.Label(
            formulario,
            text="Fecha y hora",
            font=("Arial", 10, "bold")
        ).pack(
            anchor="w",
            pady=(12, 4)
        )
        fila_fecha = tk.Frame(formulario)
        fila_fecha.pack(
            fill="x",
            pady=4
        )
        tk.Label(fila_fecha, text="Día").pack(side="left")

        entrada_dia = tk.Entry(fila_fecha, width=5)
        entrada_dia.pack(side="left", padx=(5, 10))

        tk.Label(fila_fecha, text="Mes").pack(side="left")

        entrada_mes = tk.Entry(fila_fecha, width=5)
        entrada_mes.pack(side="left", padx=(5, 10))

        tk.Label(fila_fecha, text="Año").pack(side="left")

        entrada_anio = tk.Entry(fila_fecha, width=7)
        entrada_anio.pack(side="left", padx=(5, 0))

        fila_hora = tk.Frame(formulario)
        fila_hora.pack(
            fill="x",
            pady=4
        )
        tk.Label(fila_hora, text="Hora").pack(side="left")

        entrada_hora = tk.Entry(fila_hora, width=5)
        entrada_hora.pack(side="left", padx=(5, 10))

        tk.Label(fila_hora, text="Min").pack(side="left")

        entrada_minuto = tk.Entry(fila_hora, width=5)
        entrada_minuto.pack(side="left", padx=(5, 10))

        tk.Label(fila_hora, text="Seg").pack(side="left")

        entrada_segundo = tk.Entry(fila_hora, width=5)
        entrada_segundo.pack(side="left", padx=(5, 0))

        campos["dia"] = entrada_dia
        campos["mes"] = entrada_mes
        campos["anio"] = entrada_anio
        campos["hora"] = entrada_hora
        campos["minuto"] = entrada_minuto
        campos["segundo"] = entrada_segundo

        fila_estacion = tk.Frame(formulario)
        fila_estacion.pack(
            fill="x",
            pady=4
        )

        tk.Label(
            fila_estacion,
            text="Estación",
            width=18,
            anchor="w"
        ).pack(side="left")

        estaciones = [
            estacion.id_estacion
            for estacion in self.escenario.estaciones
        ]

        selector_estacion = ttk.Combobox(
            fila_estacion,
            values=estaciones,
            state="readonly"
        )
        selector_estacion.pack(
            side="left",
            fill="x",
            expand=True
        )

        if estaciones:
            selector_estacion.current(0)

        campos["estacion"] = selector_estacion

        boton_encolar = tk.Button(
            ventana,
            text="＋ Encolar reporte",
            command=lambda: self.encolar_desde_formulario(
                ventana,
                campos
            )
        )
        boton_encolar.pack(
            pady=20
        )

    def encolar_desde_formulario(self, ventana, campos):
        try:
            if any(
                not campos[clave].get().strip()
                for clave in [
                    "id_evento",
                    "revision",
                    "magnitud",
                    "profundidad",
                    "zonax",
                    "zonay",
                    "dia",
                    "mes",
                    "anio",
                    "hora",
                    "minuto",
                    "segundo"
                ]
            ):
                raise ValueError("Todos los campos son obligatorios.")

            id_evento = int(campos["id_evento"].get())
            revision = int(campos["revision"].get())
            magnitud = float(campos["magnitud"].get())
            profundidad = float(campos["profundidad"].get())
            zonax = float(campos["zonax"].get())
            zonay = float(campos["zonay"].get())

            dia = int(campos["dia"].get())
            mes = int(campos["mes"].get())
            anio = int(campos["anio"].get())
            hora = int(campos["hora"].get())
            minuto = int(campos["minuto"].get())
            segundo = int(campos["segundo"].get())

            fecha = datetime(
                anio,
                mes,
                dia,
                hora,
                minuto,
                segundo,
                tzinfo=timezone.utc
            )

            estacion = campos["estacion"].get()

            if not estacion:
                raise ValueError("Debe seleccionar una estación.")

            self.escenario.prepararReporte(
                id_evento,
                revision,
                magnitud,
                profundidad,
                zonax,
                zonay,
                fecha,
                estacion
            )

            ventana.destroy()
            self.mostrar()

        except ValueError:
            messagebox.showerror(
                "Reporte inválido",
                "Verifique los datos ingresados. "
                "Todos los campos deben estar completos y tener un formato válido."
            )

        except TypeError:
            messagebox.showerror(
                "Reporte inválido",
                "Hay un dato con un formato incorrecto."
            )

    def limpiar(self):
        for widget in self.padre.winfo_children():
            widget.destroy()