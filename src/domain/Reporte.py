# Represents a reported event revision and its associated data.
class Reporte:
    def __init__(self, id_evento, nRevision, magnitud, profundidad, zonax, zonay, fecha, estacion):
        self.id_evento = id_evento
        self.nRevision = nRevision
        self.magnitud = magnitud
        self.profundidad = profundidad
        self.zonax = zonax
        self.zonay = zonay
        self.fecha = fecha
        self.estacion = estacion

    def consultarReporte(self):
        return {
            "id_evento": self.id_evento,
            "nRevision": self.nRevision,
            "magnitud": self.magnitud,
            "profundidad": self.profundidad,
            "zonax": self.zonax,
            "zonay": self.zonay,
            "fecha": self.fecha,
            "estacion": self.estacion
        }
