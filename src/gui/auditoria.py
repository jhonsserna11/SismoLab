import tkinter as tk


class PantallaAuditoria:

    def __init__(self, padre, escenario, mostrar_estado):
        self.padre = padre
        self.escenario = escenario
        self.mostrar_estado = mostrar_estado


    def mostrar(self):
        self.limpiar()

        reporte = self.escenario.verificarEstructura()

        titulo = tk.Label(
            self.padre,
            text="Auditoría",
            font=("Arial", 22, "bold")
        )
        titulo.pack(anchor="w", pady=(0, 5))

        subtitulo = tk.Label(
            self.padre,
            text="Verificación de la estructura actual del escenario",
            font=("Arial", 11)
        )
        subtitulo.pack(anchor="w", pady=(0, 20))

        estado = "VÁLIDA" if reporte["valido"] else "CON INCONSISTENCIAS"
        equilibrio = (
            "EQUILIBRADO"
            if reporte["equilibrado"]
            else "DESBALANCEADO"
        )

        tk.Label(
            self.padre,
            text=f"Resultado: {estado}",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", pady=3)

        tk.Label(
            self.padre,
            text=f"Equilibrio AVL: {equilibrio}",
            font=("Arial", 12)
        ).pack(anchor="w", pady=3)

        tk.Label(
            self.padre,
            text=f"Modo: {reporte['modo']}",
            font=("Arial", 11)
        ).pack(anchor="w", pady=3)

        tk.Label(
            self.padre,
            text=f"Nodos visitados: {reporte['nodos_visitados']}",
            font=("Arial", 11)
        ).pack(anchor="w", pady=(3, 15))

        tk.Label(
            self.padre,
            text="Eventos inconsistentes",
            font=("Arial", 13, "bold")
        ).pack(anchor="w", pady=(5, 5))

        inconsistencias = tk.Text(
            self.padre,
            height=18,
            width=80,
            state="normal"
        )
        inconsistencias.pack(fill="both", expand=True)

        eventos = reporte.get("eventos_inconsistentes", [])

        if not eventos:
            inconsistencias.insert(
                "end",
                "No se encontraron inconsistencias en la estructura.\n"
            )
        else:
            for evento in eventos:
                inconsistencias.insert(
                    "end",
                    f"ID={evento.get('id', 'N/D')}\n"
                )

                for error in evento.get("errores", []):
                    inconsistencias.insert(
                        "end",
                        f"  ERROR: {error}\n"
                    )

                for advertencia in evento.get("advertencias", []):
                    inconsistencias.insert(
                        "end",
                        f"  ADVERTENCIA: {advertencia}\n"
                    )

                if "altura_recalculada" in evento:
                    inconsistencias.insert(
                        "end",
                        f"  Altura recalculada: "
                        f"{evento['altura_recalculada']}\n"
                    )

                if "factor_balance_recalculado" in evento:
                    inconsistencias.insert(
                        "end",
                        f"  Factor recalculado: "
                        f"{evento['factor_balance_recalculado']}\n"
                    )

                inconsistencias.insert("end", "\n")

        inconsistencias.config(state="disabled")

        self.mostrar_estado("Auditoría actualizada")


    def limpiar(self):
        for widget in self.padre.winfo_children():
            widget.destroy()