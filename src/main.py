import tkinter as tk
from tkinter import messagebox
import json

from datetime import datetime

from src.logic.Escenario import Escenario
from src.gui.resumen import PantallaResumen
from src.gui.eventos import PantallaEventos
from src.gui.estaciones import PantallaEstaciones
from src.gui.zonas import PantallaZonas
from src.gui.reportes import PantallaReportes
from src.gui.historico import PantallaHistorico
from src.gui.arboles import PantallaArboles
from src.gui.metricas import PantallaMetricas
from src.gui.versiones import PantallaVersiones
from src.gui.auditoria import PantallaAuditoria
from src.gui.configuracion import PantallaConfiguracion


class SismoLabApp:

    def __init__(self, ventana, escenario):
        self.ventana = ventana
        self.escenario = escenario

        self.ventana.title("SismoLab AVL")
        self.ventana.geometry("1200x700")
        self.ventana.minsize(1000, 600)
        self.ventana.state("zoomed")

        self.seccion_actual = "Resumen"

        self.crear_interfaz()

        # Create screens after the content frame has been initialized.
        self.pantalla_resumen = PantallaResumen(
            self.contenido,
            self.escenario,
            self.actualizar_estado
        )

        self.pantalla_eventos = PantallaEventos(
            self.contenido,
            self.escenario,
            self.actualizar_estado
        )

        self.pantalla_estaciones = PantallaEstaciones(
            self.contenido,
            self.escenario,
            self.actualizar_estado
        )

        self.pantalla_zonas = PantallaZonas(
            self.contenido,
            self.escenario,
            self.actualizar_estado
        )

        self.pantalla_reportes = PantallaReportes(
            self.contenido,
            self.escenario,
            self.actualizar_estado
        )

        self.pantalla_historico = PantallaHistorico(
            self.contenido,
            self.escenario,
            self.actualizar_estado
        )

        self.pantalla_arboles = PantallaArboles(
            self.contenido,
            self.escenario,
            self.actualizar_estado
        )

        self.pantalla_metricas = PantallaMetricas(
            self.contenido,
            self.escenario,
            self.actualizar_estado
        )

        self.pantalla_versiones = PantallaVersiones(
            self.contenido,
            self.escenario,
            self.actualizar_estado
        )

        self.pantalla_auditoria = PantallaAuditoria(
            self.contenido,
            self.escenario,
            self.actualizar_estado
        )

        self.pantalla_configuracion = PantallaConfiguracion(
            self.contenido,
            self.escenario,
            self.actualizar_estado
        )

        self.mostrar_resumen()
        self.actualizar_reloj()

    def crear_interfaz(self):

        self.header = tk.Frame(
            self.ventana,
            height=70,
            bd=1,
            relief="solid"
        )
        self.header.pack(
            side="top",
            fill="x"
        )
        self.header.pack_propagate(False)

        self.titulo = tk.Label(
            self.header,
            text="SismoLab AVL",
            font=("Arial", 22, "bold")
        )
        self.titulo.pack(
            side="left",
            padx=25
        )

        controles = tk.Frame(self.header)
        controles.pack(
            side="right",
            padx=20
        )

        self.parametros_label = tk.Label(
            controles,
            text=(
                f"W: {self.escenario.W} h   |   "
                f"R: {self.escenario.R} km   |   "
                f"L: {self.escenario.L}   |   "
                f"T: {self.escenario.T} h"
            ),
            font=("Arial", 9)
        )
        self.parametros_label.pack(
            side="left",
            padx=(0, 15)
        )

        self.boton_estres = tk.Button(
            controles,
            text="⚡ Estrés: OFF",
            font=("Arial", 9),
            command=self.cambiar_modo_estres
        )
        self.boton_estres.pack(
            side="left",
            padx=(0, 10)
        )

        tk.Button(
            controles,
            text="⏩ Avanzar",
            font=("Arial", 9),
            command=self.mostrar_avanzar_reloj
        ).pack(
            side="left",
            padx=(0, 10)
        )

        self.reloj_label = tk.Label(
            controles,
            text="",
            font=("Arial", 10, "bold")
        )
        self.reloj_label.pack(
            side="left"
        )

        self.cuerpo = tk.Frame(self.ventana)
        self.cuerpo.pack(
            side="top",
            fill="both",
            expand=True
        )

        self.menu = tk.Frame(
            self.cuerpo,
            width=210,
            bd=1,
            relief="solid"
        )
        self.menu.pack(
            side="left",
            fill="y"
        )
        self.menu.pack_propagate(False)

        self.crear_menu()

        self.contenido = tk.Frame(
            self.cuerpo,
            padx=25,
            pady=25
        )
        self.contenido.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.estado_barra = tk.Label(
            self.ventana,
            text="Listo",
            anchor="w",
            bd=1,
            relief="sunken",
            padx=10
        )
        self.estado_barra.pack(
            side="bottom",
            fill="x"
        )

    def mostrar_avanzar_reloj(self):

        ventana = tk.Toplevel(self.ventana)
        ventana.title("Avanzar reloj")
        ventana.geometry("320x220")
        ventana.resizable(False, False)
        ventana.transient(self.ventana)
        ventana.grab_set()

        contenedor = tk.Frame(
            ventana,
            padx=25,
            pady=20
        )
        contenedor.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            contenedor,
            text="Avanzar reloj de simulación",
            font=("Arial", 14, "bold")
        ).pack(
            anchor="w",
            pady=(0, 15)
        )

        tk.Label(
            contenedor,
            text="Cantidad de horas:"
        ).pack(
            anchor="w"
        )

        horas_var = tk.IntVar(value=1)

        tk.Spinbox(
            contenedor,
            from_=1,
            to=720,
            textvariable=horas_var,
            width=10
        ).pack(
            anchor="w",
            pady=(5, 15)
        )

        def avanzar():

            try:
                horas = horas_var.get()

                if horas <= 0:
                    raise ValueError

                self.escenario.avanzarReloj(horas)

            except ValueError:
                messagebox.showerror(
                    "Valor inválido",
                    "La cantidad de horas debe ser un entero positivo.",
                    parent=ventana
                )
                return

            ventana.destroy()

            self.actualizar_reloj()

            self.mostrar_estado(
                "Reloj de simulación actualizado"
            )

        tk.Button(
            contenedor,
            text="Avanzar",
            font=("Arial", 10, "bold"),
            command=avanzar
        ).pack(
            side="right"
        )
    def cambiar_modo_estres(self):
        self.escenario.modo_estres = not self.escenario.modo_estres

        estado = (
            "ON"
            if self.escenario.modo_estres
            else "OFF"
        )

        self.boton_estres.config(
            text=f"⚡ Estrés: {estado}"
        )

        self.actualizar_estado(
            f"Modo estrés {'activado' if self.escenario.modo_estres else 'desactivado'}"
        )

    def crear_menu(self):

        opciones = [
            "Resumen",
            "Eventos",
            "Reportes",
            "Estaciones",
            "Zonas",
            "Histórico",
            "Árboles",
            "Métricas",
            "Versiones",
            "Auditoría",
            "Configuración"
        ]

        for opcion in opciones:

            boton = tk.Button(
                self.menu,
                text=opcion,
                anchor="w",
                padx=20,
                pady=8,
                relief="flat",
                command=lambda nombre=opcion:
                    self.cambiar_seccion(nombre)
            )

            boton.pack(
                fill="x"
            )

        separador = tk.Frame(
            self.menu,
            height=15
        )
        separador.pack(
            fill="x"
        )

        self.boton_deshacer = tk.Button(
            self.menu,
            text="↶  Deshacer",
            anchor="w",
            padx=20,
            pady=8,
            command=self.deshacer
        )
        self.boton_deshacer.pack(
            fill="x"
        )

    def cambiar_seccion(self, nombre):

        self.seccion_actual = nombre

        if nombre == "Resumen":
            self.pantalla_resumen.mostrar()
        elif nombre == "Eventos":
            self.pantalla_eventos.mostrar()
        elif nombre == "Estaciones":
            self.pantalla_estaciones.mostrar()
        elif nombre == "Zonas":
            self.pantalla_zonas.mostrar()
        elif nombre == "Reportes":
            self.pantalla_reportes.mostrar()
        elif nombre == "Histórico":
            self.pantalla_historico.mostrar()
        elif nombre == "Árboles":
            self.pantalla_arboles.mostrar()
        elif nombre == "Métricas":
            self.pantalla_metricas.mostrar()
        elif nombre == "Versiones":
            self.pantalla_versiones.mostrar()
        elif nombre == "Auditoría":
            self.pantalla_auditoria.mostrar()
        elif nombre == "Configuración":
            self.pantalla_configuracion.mostrar()
        else:
            self.mostrar_pantalla_provisional(nombre)

    def limpiar_contenido(self):

        for widget in self.contenido.winfo_children():
            widget.destroy()

    def mostrar_resumen(self):
        self.pantalla_resumen.mostrar()

    def mostrar_eventos(self):
        self.pantalla_eventos.mostrar()

    def mostrar_pantalla_provisional(self, nombre):

        self.limpiar_contenido()

        titulo = tk.Label(
            self.contenido,
            text=nombre,
            font=("Arial", 20, "bold")
        )
        titulo.pack(
            anchor="w"
        )

        mensaje = tk.Label(
            self.contenido,
            text="Esta sección será conectada al backend.",
            font=("Arial", 13)
        )
        mensaje.pack(
            anchor="w",
            pady=20
        )

        self.estado_barra.config(
            text=f"Sección actual: {nombre}"
        )

    def actualizar_estado(self, mensaje):

        self.estado_barra.config(
            text=mensaje
        )

    def actualizar_reloj(self):

        self.reloj_label.config(
            text=(
                f"UTC: "
                f"{self.escenario.reloj.strftime('%Y-%m-%d %H:%M:%S')}"
            )
        )

        estado = (
            "ON"
            if self.escenario.modo_estres
            else "OFF"
        )

        self.boton_estres.config(
            text=f"⚡ Estrés: {estado}"
        )

    def deshacer(self):

        resultado = self.escenario.deshacer()

        if resultado:

            self.estado_barra.config(
                text="✓ Última acción deshecha"
            )

            self.cambiar_seccion(
                self.seccion_actual
            )

            self.actualizar_reloj()

        else:

            self.estado_barra.config(
                text="No hay acciones para deshacer"
            )


def cargar_escenario_inicial():

    with open(
        "data/estado_inicial.json",
        "r",
        encoding="utf-8"
    ) as archivo:

        datos = json.load(archivo)

    config = datos["configuracion"]

    reloj = datetime.fromisoformat(
        config["reloj"].replace("Z", "+00:00")
    )

    escenario = Escenario(
        config["W"],
        config["R"],
        config["L"],
        config["T"],
        reloj
    )

    escenario.cargarEscenario(datos)

    # The initial state should not be undoable.
    escenario.pila_deshacer.clear()

    return escenario


def iniciar_interfaz():

    escenario = cargar_escenario_inicial()

    ventana = tk.Tk()

    app = SismoLabApp(
        ventana,
        escenario
    )

    ventana.mainloop()


if __name__ == "__main__":
    iniciar_interfaz()