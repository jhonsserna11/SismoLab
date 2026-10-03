import tkinter as tk


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
            text="Eventos archivados",
            font=("Arial", 11)
        )
        subtitulo.pack(anchor="w", pady=(0, 20))

        eventos = self.escenario.historico

        indicador = tk.Label(
            self.padre,
            text=f"{len(eventos)} eventos históricos",
            font=("Arial", 12, "bold")
        )
        indicador.pack(anchor="w", pady=(0, 15))

        if not eventos:
            tk.Label(
                self.padre,
                text="No hay eventos archivados.",
                font=("Arial", 12)
            ).pack(anchor="w")

            self.mostrar_estado("No hay eventos históricos")
            return

        for evento in eventos:
            self.crear_tarjeta(evento)

        self.mostrar_estado(
            f"Eventos históricos: {len(eventos)}"
        )

    def crear_tarjeta(self, evento):
        tarjeta = tk.Frame(
            self.padre,
            bd=1,
            relief="solid",
            padx=20,
            pady=15
        )
        tarjeta.pack(fill="x", pady=5)

        tk.Label(
            tarjeta,
            text=f"Evento {evento.id}",
            font=("Arial", 14, "bold")
        ).pack(anchor="w")

        datos = vars(evento)

        for nombre, valor in datos.items():
            tk.Label(
                tarjeta,
                text=f"{nombre}: {valor}",
                font=("Arial", 10)
            ).pack(anchor="w", pady=(2, 0))

    def limpiar(self):
        for widget in self.padre.winfo_children():
            widget.destroy()