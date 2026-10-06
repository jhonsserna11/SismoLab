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
from src.gui.arboles import PantallaArboles
from src.gui.metricas import PantallaMetricas
from src.gui.versiones import PantallaVersiones
from src.gui.auditoria import PantallaAuditoria
from src.gui.configuracion import PantallaConfiguracion
from src.gui.historico import PantallaHistorico
from src.gui.cargas import PantallaCargas
from src.gui.consultas import PantallaConsultas


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

        # Las pantallas se crean después de crear self.contenido.
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
        self.pantalla_consultas = PantallaConsultas(
            self.contenido,
            self.escenario,
            self.actualizar_estado
        )

        self.pantalla_versiones = PantallaVersiones(
            self.contenido,
            self.escenario,
            self.actualizar_estado,
            self.actualizar_boton_estres
        )

        self.pantalla_auditoria = PantallaAuditoria(
            self.contenido,
            self.escenario,
            self.actualizar_estado
        )

        self.pantalla_configuracion = PantallaConfiguracion(
            self.contenido,
            self.escenario,
            self.actualizar_estado,
            self.actualizar_parametros
        )
        self.pantalla_cargas = PantallaCargas(
            self.contenido,
            self.escenario,
            self.actualizar_estado,
            self.actualizar_boton_estres
        )

        self.mostrar_resumen()
        self.actualizar_reloj()

    def crear_interfaz(self):

        # ===== BARRA SUPERIOR =====

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

        # ===== INFORMACIÓN Y CONTROLES =====

        controles = tk.Frame(self.header)
        controles.pack(
            side="right",
            padx=20
        )

        # Parámetros del escenario
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

        # Modo estrés
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

        self.boton_recuperar = tk.Button(
            controles,
            text="↻ Recuperar AVL",
            font=("Arial", 9),
            command=self.recuperar_arbol,
            state="disabled"
        )

        self.boton_recuperar.pack(
            side="left",
            padx=(0, 10)
        )

        # Avanzar reloj
        tk.Button(
            controles,
            text="⏩ Avanzar",
            font=("Arial", 9),
            command=self.mostrar_avanzar_reloj
        ).pack(
            side="left",
            padx=(0, 10)
        )

        # Reloj
        self.reloj_label = tk.Label(
            controles,
            text="",
            font=("Arial", 10, "bold")
        )
        self.reloj_label.pack(
            side="left"
        )

        # ===== CUERPO =====

        self.cuerpo = tk.Frame(self.ventana)
        self.cuerpo.pack(
            side="top",
            fill="both",
            expand=True
        )

        # ===== MENÚ LATERAL =====

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

        # ===== CONTENIDO =====

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

        # ===== BARRA DE ESTADO =====

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


        tk.Button(
            contenedor,
            text="Avanzar",
            font=("Arial", 10, "bold"),
            command=avanzar
        ).pack(
            side="right"
        )
    def cambiar_modo_estres(self):

        if self.escenario.modo_estres:
            return

        self.escenario.modo_estres = True

        self.boton_estres.config(
            text="⚡ Estrés: ON",
            state="disabled"
        )

        self.actualizar_estado(
            "Modo estrés activado"
        )
        self.actualizar_boton_estres()
        self.cambiar_seccion(self.seccion_actual)
    def actualizar_boton_estres(self):
        estado = self.escenario.modo_estres

        self.boton_estres.config(
            text=f"⚡ Estrés: {'ON' if estado else 'OFF'}",
            state="disabled" if estado else "normal"
        )

        self.boton_recuperar.config(
            state="normal" if estado else "disabled"
        )

    def recuperar_arbol(self):
        confirmar = messagebox.askyesno(
            "Recuperar AVL",
            "Se realizará la recuperación global del árbol AVL.\n\n"
            "Se corregirán los desbalances mediante rotaciones "
            "y se verificará la estructura al finalizar.\n\n"
            "¿Desea continuar?"
        )

        if not confirmar:
            return

        metricas = self.escenario.avl.metricas

        izquierdas_antes = metricas["giros_izquierda"]
        derechas_antes = metricas["giros_derecha"]

        try:
            rafaga_activa = self.pantalla_reportes.rafaga_activa
            rafaga_pausada = self.pantalla_reportes.rafaga_pausada
            if rafaga_activa and not rafaga_pausada:
                self.pantalla_reportes.pausar_rafaga()
            self.escenario.recuperarArbol()

        except ValueError as error:
            messagebox.showerror(
                "Recuperación fallida",
                str(error)
            )

            self.actualizar_boton_estres()
            self.cambiar_seccion(self.seccion_actual)
            return

        izquierdas_despues = metricas["giros_izquierda"]
        derechas_despues = metricas["giros_derecha"]

        giros_izquierda = (
            izquierdas_despues - izquierdas_antes
        )

        giros_derecha = (
            derechas_despues - derechas_antes
        )

        total_giros = (
            giros_izquierda + giros_derecha
        )

        self.actualizar_boton_estres()

        self.cambiar_seccion(
            self.seccion_actual
        )

        messagebox.showinfo(
            "Recuperación completada",
            "El árbol AVL fue recuperado correctamente.\n\n"
            f"Rotaciones a la izquierda: {giros_izquierda}\n"
            f"Rotaciones a la derecha: {giros_derecha}\n"
            f"Total de rotaciones: {total_giros}\n\n"
            "La auditoría confirmó que el árbol está "
            "válido y equilibrado.\n\n"
            "El sistema volvió a modo normal."
        )

    def crear_menu(self):

        opciones = [
            "Resumen",
            "Eventos",
            "Reportes",
            "Estaciones",
            "Zonas",
            "Historico",
            "Árboles",
            "Métricas",
            "Consultas",
            "Versiones",
            "Cargas",
            "Auditoría",
            "Configuración"
        ]

        self.botones_menu = {}
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
            self.botones_menu[opcion] = boton
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
        for boton in self.botones_menu.values():
            boton.config(bg=self.menu.cget("bg"))
        self.botones_menu[nombre].config(bg="#CDCDCD")

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
        elif nombre == "Árboles":
            self.pantalla_arboles.mostrar()
        elif nombre == "Historico":
            self.pantalla_historico.mostrar()
        elif nombre == "Métricas":
            self.pantalla_metricas.mostrar()
        elif nombre == "Consultas":
            self.pantalla_consultas.mostrar()
        elif nombre == "Versiones":
            self.pantalla_versiones.mostrar()
        elif nombre == "Cargas":
            self.pantalla_cargas.mostrar()
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

    def actualizar_parametros(self):
        self.parametros_label.config(
            text=(
                f"W: {self.escenario.W} h   |   "
                f"R: {self.escenario.R} km   |   "
                f"L: {self.escenario.L}   |   "
                f"T: {self.escenario.T} h"
            )
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
        self.actualizar_boton_estres()

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
        "data/escenario_pruebas.json",
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

    # El estado inicial no debe ser una acción de deshacer.
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