import tkinter as tk
from tkinter import messagebox


class PantallaHistorico:

    def __init__(self, padre, escenario, mostrar_estado):
        self.padre = padre
        self.escenario = escenario
        self.mostrar_estado = mostrar_estado

    def mostrar(self):
        self.limpiar()

        titulo = tk.Label(
            self.padre,
            text="Histórico",
            font=("Arial", 22, "bold")
        )
        titulo.pack(anchor="w", pady=(0, 5))

        subtitulo = tk.Label(
            self.padre,
            text="Eventos archivados y archivo de ramas antiguas",
            font=("Arial", 11)
        )
        subtitulo.pack(anchor="w", pady=(0, 20))

        acciones = tk.Frame(
            self.padre,
            bd=1,
            relief="solid",
            padx=15,
            pady=12
        )
        acciones.pack(fill="x", pady=(0, 15))

        tk.Label(
            acciones,
            text="Archivo de eventos antiguos",
            font=("Arial", 12, "bold")
        ).pack(anchor="w")

        tk.Label(
            acciones,
            text=(
                "Busca automáticamente la mejor rama elegible "
                "según antigüedad y prioridad."
            ),
            font=("Arial", 10)
        ).pack(anchor="w", pady=(5, 10))

        tk.Button(
            acciones,
            text="Archivar rama de eventos antiguos",
            command=self.preparar_archivo
        ).pack(anchor="w")

        tk.Label(
            self.padre,
            text="Eventos archivados",
            font=("Arial", 13, "bold")
        ).pack(anchor="w", pady=(5, 8))

        historico = self.escenario.historico

        tk.Label(
            self.padre,
            text=f"{len(historico)} eventos archivados",
            font=("Arial", 11)
        ).pack(anchor="w", pady=(0, 10))

        if not historico:
            tk.Label(
                self.padre,
                text="No hay eventos archivados.",
                font=("Arial", 11)
            ).pack(anchor="w")

            self.mostrar_estado("No hay eventos archivados")
            return

        contenedor = tk.Frame(self.padre)
        contenedor.pack(fill="both", expand=True)

        canvas = tk.Canvas(
            contenedor,
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            contenedor,
            orient="vertical",
            command=canvas.yview
        )

        lista = tk.Frame(canvas)

        lista.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window(
            (0, 0),
            window=lista,
            anchor="nw"
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        for evento in historico:
            self.crear_tarjeta_evento(evento, lista)

        self.mostrar_estado(
            f"Eventos archivados: {len(historico)}"
        )

    def crear_tarjeta_evento(self, evento, padre):
        tarjeta = tk.Frame(
            padre,
            bd=1,
            relief="solid",
            padx=12,
            pady=10
        )
        tarjeta.pack(fill="x", pady=5)

        tk.Label(
            tarjeta,
            text=f"Evento {evento.id}",
            font=("Arial", 12, "bold")
        ).pack(anchor="w")

        tk.Label(
            tarjeta,
            text=f"Magnitud: {evento.magnitud}"
        ).pack(anchor="w")

        tk.Label(
            tarjeta,
            text=f"Profundidad: {evento.profundidad}"
        ).pack(anchor="w")

        tk.Label(
            tarjeta,
            text=f"Ubicación: ({evento.zonax}, {evento.zonay})"
        ).pack(anchor="w")

        tk.Label(
            tarjeta,
            text=f"Fecha y hora: {evento.fechaHora}"
        ).pack(anchor="w")

        tk.Label(
            tarjeta,
            text=f"Revisión: {evento.revision}"
        ).pack(anchor="w")

        tk.Label(
            tarjeta,
            text=f"Estaciones: {', '.join(evento.estaciones)}"
        ).pack(anchor="w")

        tk.Label(
            tarjeta,
            text="Estado: Archivado"
        ).pack(anchor="w")

    def preparar_archivo(self):
        resultado = self.escenario.obtenerRamaArchivable()

        if resultado is None or resultado["mejor"] is None:
            messagebox.showinfo(
                "Archivar rama",
                "No existe una rama elegible para archivar."
            )
            return

        candidato = resultado["mejor"]
        nodo = candidato["nodo"]

        nodos = self.escenario._obtenerNodosSubarbol(nodo)

        ids = [
            str(nodo.key.id_key)
            for nodo in nodos
        ]

        texto_ids = ", ".join(ids)

        confirmar = messagebox.askyesno(
            "Confirmar archivo",
            f"Rama seleccionada para archivo\n\n"
            f"Cantidad de eventos: {len(nodos)}\n\n"
            f"Eventos afectados:\n"
            f"{texto_ids}\n\n"
            f"Todos tienen prioridad baja y una antigüedad "
            f"mayor a {self.escenario.T} horas.\n\n"
            f"¿Desea archivar esta rama?"
        )

        if not confirmar:
            return

        try:
            self.escenario.archivarRama(nodo)

            self.mostrar_estado(
                f"Rama archivada: {len(nodos)} eventos"
            )

            self.mostrar()

        except Exception as error:
            messagebox.showerror(
                "Error al archivar",
                str(error)
            )
    def limpiar(self):
        for widget in self.padre.winfo_children():
            widget.destroy()