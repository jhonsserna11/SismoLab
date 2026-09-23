from datetime import datetime, timezone
from math import sqrt
from decimal import Decimal, InvalidOperation

class Evento:

    def __init__(self, id_evento:int, magnitud:float, profundidad:float, zonax:float, zonay:float, 
                fecha:datetime, revision:int, estaciones:list[str]):

        if type(id_evento) is int and 1<=id_evento<=999999:
            self.id = id_evento
        else:
            raise ValueError("Id fuera del rango permitido")

        if isinstance(magnitud, (float, int)) and -2.0<=magnitud<=10.0:
            self.magnitud = self._validar_undecimal(magnitud)
        else:
            raise ValueError("Magnitud fuera del rango permitido")

        if isinstance(profundidad, (float, int)) and 0.0<=profundidad<=700.0:
            self.profundidad = self._validar_undecimal(profundidad)
        else:
            raise ValueError("Profundidad fuera del rango permitido")

        if (isinstance(zonax, (float, int)) and isinstance(zonay, (float, int))) and (0.0<=zonax<=1000.0 and 0.0<=zonay<=1000.0):
            self.zonax = self._validar_undecimal(zonax)
            self.zonay = self._validar_undecimal(zonay)
        else:
            raise ValueError("epicentro fuera del rango permitido")

        if type(revision) is int and revision>0:
            self.revision = revision
        else:
            raise ValueError("revision debe ser positivo")

        if type(estaciones) is list:
            self.estaciones = []
            for estacion in estaciones:
                if type(estacion) is str and len(estacion)>0:
                    self.estaciones.append(estacion)
                else:
                    raise ValueError("Estación debe ser tipo str")
        else:
            raise ValueError("Parametro estaciones debe ser una lista")
            
        if type(fecha) is datetime and (fecha.tzinfo is timezone.utc and fecha.microsecond == 0):
            self.fechaHora = fecha
        else:
            raise ValueError("Fecha no tiene estructura válida")
        
        self.estado = "Pendiente"

    def _validar_undecimal(self, decimal):
        try:
            d = Decimal(str(decimal))
        
            molde = Decimal('0.1')
            if d.as_tuple().exponent == 0:
                d = d.quantize(molde)
            if d.as_tuple().exponent != -1:
                raise ValueError(f"el valor {d} debe tener solo un decimal")
            return d
        except InvalidOperation:
            raise TypeError(f"el valor {decimal} no es válido")

        
    def calcularPrioridad(self, poblada:bool)->int:
        if self.magnitud >= 6.0 or (self.magnitud >= 4.5 and self.profundidad <= 30.0 and poblada):
            return 3
        elif self.magnitud >= 4.5:
            return 2
        else:
            return 1

    def esCandidato(self, eventoB:"Evento", w, r):
        if self.magnitud > eventoB.magnitud:
            diferencia = (eventoB.fechaHora - self.fechaHora).total_seconds() / 3600
            distancia = sqrt(((self.zonax - eventoB.zonax)**2) + ((self.zonay - eventoB.zonay)**2))
            if 0<diferencia<= w and distancia <= r:
                return True
            else:
                return False
        else:
            return False

