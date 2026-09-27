from src.structures.Avl import Avl
from src.structures.Bst import Bst
from src.structures.Nodo import Nodo, Key

from src.domain.Evento import Evento
from src.domain.Zona import Zona

from collections import deque
from datetime import datetime, timezone, timedelta

class Escenario:
    def __init__(self, w, r, l, t, reloj):
        self.avl = Avl()
        self.bst = Bst()

        self.estaciones = []
        self.zonas: list[Zona] = []

        self.historico: list[Evento] = []
        self.eliminados = set()

        self.W = w #48 
        self.R = r #40
        self.L = l #3
        self.T = t #72

        self.modo_estres = False
        self.reloj = reloj

        self.pila_deshacer = []
        self.cola_reportes = deque()

    def actualizarW(self, valor):
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ValueError("W debe ser un número positivo")
        self.W = float(valor)

    def actualizarR(self, valor):
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ValueError("R debe ser un número positivo")
        self.R = float(valor)

    def crearEvento(self, idEvento, magnitud, profundidad, zonax, zonay, fecha, estacion):
        try:
            if not self._IdUnica(idEvento):
                raise ValueError("El identificador ingresado ya existe.")

            evento = Evento(idEvento, magnitud, profundidad, zonax, zonay, fecha, 1, estacion)
            self._crearEvento(evento)
        except ValueError as e:
            print("error: ", e)
    def _crearEvento(self, evento:Evento):
        prioridad = evento.calcularPrioridad(self._esPoblada(evento.zonax, evento.zonay))
        key = Key(prioridad, evento.magnitud, evento.id)
        self.avl.insertar(key, evento, self.modo_estres)


    def _IdUnica(self, id)->bool:
        if type(id) is not int:
            raise ValueError("el id ingresado debe ser numero entero")
        if type(self.avl.encontrarNodo(id)) is Nodo:
            return False
        for e in self.historico:
            if e.id == id:
                return False
        if id in self.eliminados:
            return False

        return True
  
    def _esPoblada(self, zonax, zonay)->bool:
        for zona in self.zonas:
            if zona.contiene(zonax, zonay) and zona.es_poblada():
                return True
        return False

    def avanzarReloj(self, horas):
        if type(horas) is not int:
            raise ValueError("cantidad de horas debe ser tipo int")
        
        self.reloj += timedelta(hours=horas)


    def _buscarCandidatos(self, eventoB):
        candidatos = []

        if self.avl.raiz is None:
            return candidatos

        cola = deque([self.avl.raiz])

        while cola:
            nodo = cola.popleft()

            eventoA = nodo.evento

            if eventoA.esCandidato(eventoB, self.W, self.R):
                candidatos.append(eventoA)

            if nodo.izq is not None:
                cola.append(nodo.izq)

            if nodo.der is not None:
                cola.append(nodo.der)

        return candidatos
    def _agregarCandidatosArchivados(self, eventoB, candidatos):
        for eventoA in self.historico:
            if eventoA.esCandidato(eventoB, self.W, self.R):
                candidatos.append(eventoA)

    def _seleccionarCandidato(self, candidatos, eventoB):
        if not candidatos:
            return None

        mejor = candidatos[0]

        for candidato in candidatos[1:]:
            if candidato.magnitud > mejor.magnitud:
                mejor = candidato

            elif candidato.magnitud == mejor.magnitud:
                diferencia_candidato = (
                    eventoB.fechaHora - candidato.fechaHora
                ).total_seconds()

                diferencia_mejor = (
                    eventoB.fechaHora - mejor.fechaHora
                ).total_seconds()

                if diferencia_candidato < diferencia_mejor:
                    mejor = candidato

                elif diferencia_candidato == diferencia_mejor:
                    if candidato.id < mejor.id:
                        mejor = candidato

        return mejor

    def _obtenerAsociaciones(self, eventoB):
        candidatos = self._buscarCandidatos(eventoB)

        self._agregarCandidatosArchivados(
            eventoB,
            candidatos
        )

        asociado = self._seleccionarCandidato(
            candidatos,
            eventoB
        )

        return {
            "candidatos": candidatos,
            "asociado": asociado
        }


    def encolarReporte(self, reporte):
        self.cola_reportes.append(reporte)

    def desencolarSiguienteReporte(self):
        if not self.cola_reportes:
            return None
        return self.cola_reportes.popleft()

    def consultarColaReportes(self):
        return list(self.cola_reportes)
# dhdhdhdhdhdh
    def _datos_iguales(self, evento: Evento, reporte):
        return (
            evento.magnitud == reporte.magnitud and
            evento.profundidad == reporte.profundidad and
            evento.zonax == reporte.zonax and
            evento.zonay == reporte.zonay and
            evento.fechaHora == reporte.fecha
        )

    def _datos_validos_reporte(self, reporte):
        if not isinstance(reporte.id_evento, int) or not (1 <= reporte.id_evento <= 999999):
            return False
        if not isinstance(reporte.nRevision, int) or reporte.nRevision <= 0:
            return False
        if not isinstance(reporte.magnitud, (int, float)):
            return False
        if not isinstance(reporte.profundidad, (int, float)):
            return False
        if not isinstance(reporte.zonax, (int, float)):
            return False
        if not isinstance(reporte.zonay, (int, float)):
            return False
        if not isinstance(reporte.fecha, datetime):
            return False
        if not isinstance(reporte.estacion, str) or not reporte.estacion:
            return False
        return True

    def  _confirmarEvento(self, evento: Evento, reporte):
        if reporte.estacion not in evento.estaciones:
            evento.estaciones.append(reporte.estacion)
        evento.revision = reporte.nRevision
        return {"estado": "confirmado", "accion": "confirmar"}

    def _actualizarEventoReporte(self, nodo: Nodo, reporte):
        evento = nodo.evento
        evento.magnitud = reporte.magnitud
        evento.profundidad = reporte.profundidad
        evento.zonax = reporte.zonax
        evento.zonay = reporte.zonay
        evento.fechaHora = reporte.fecha
        evento.revision = reporte.nRevision
        if reporte.estacion not in evento.estaciones:
            evento.estaciones.append(reporte.estacion)

        nueva_key = Key(
            evento.calcularPrioridad(self._esPoblada(evento.zonax, evento.zonay)),
            evento.magnitud,
            evento.id
        )

        if nodo.key != nueva_key:
            self.avl.eliminar(nodo.key, self.modo_estres)
            self.avl.insertar(nueva_key, evento, self.modo_estres)
        else:
            nodo.key = nueva_key

        return {"estado": "actualizado", "accion": "sustituir"}

    def _reactivarEventoArchivado(self, reporte):
        for evento in self.historico:
            if evento.id == reporte.id_evento:
                nuevo_evento = Evento(
                    evento.id,
                    reporte.magnitud,
                    reporte.profundidad,
                    reporte.zonax,
                    reporte.zonay,
                    reporte.fecha,
                    reporte.nRevision,
                    [reporte.estacion] if reporte.estacion not in evento.estaciones else evento.estaciones.copy()
                )
                self.historico.remove(evento)
                self._crearEvento(nuevo_evento)
                return {"estado": "reactivado", "accion": "reactivar"}
        return {"estado": "archivado", "accion": "descartar"}

    def procesarReporte(self, reporte):
        if not self._datos_validos_reporte(reporte):
            return {"estado": "desconocido", "accion": "rechazar"}

        if reporte.id_evento in self.eliminados:
            return {"estado": "eliminado", "accion": "rechazar"}

        nodo = self.avl.encontrarNodo(reporte.id_evento)
        if nodo is not None:
            evento = nodo.evento

            if reporte.nRevision < evento.revision:
                return {"estado": "antiguo", "accion": "descartar"}

            if reporte.nRevision > evento.revision:
                return self._actualizarEventoReporte(nodo, reporte)

            if self._datos_iguales(evento, reporte):
                return self._confirmarEvento(evento, reporte)

            return {"estado": "conflicto", "accion": "rechazar"}

        for evento in self.historico:
            if evento.id == reporte.id_evento:
                if reporte.nRevision > evento.revision:
                    return self._reactivarEventoArchivado(reporte)
                return {"estado": "archivado", "accion": "descartar"}

        if not self._IdUnica(reporte.id_evento):
            return {"estado": "desconocido", "accion": "rechazar"}

        evento_nuevo = Evento(
            reporte.id_evento,
            reporte.magnitud,
            reporte.profundidad,
            reporte.zonax,
            reporte.zonay,
            reporte.fecha,
            reporte.nRevision,
            [reporte.estacion]
        )
        self._crearEvento(evento_nuevo)
        return {"estado": "registrado", "accion": "registrar"}

    def procesarSiguienteReporte(self):
        reporte = self.desencolarSiguienteReporte()
        if reporte is None:
            return None
        return self.procesarReporte(reporte)

# dhdhdhdhdh

    def consultarEvento(self, idEvento:int):
        for evento in self.historico:
            if evento.id == idEvento:
                return {"status": "archivado"}
        if idEvento in self.eliminados:
            return {"status": "eliminado"}

        nodo = self.avl.encontrarNodo(idEvento)
        if nodo is None:
            raise ValueError("el id ingresado no existe")
        return self._consultarEvento(nodo)

    def _consultarEvento(self, nodo:Nodo):
        evento = nodo.evento
        prioridad = nodo.key.prioridad
        profundidad = self.avl.nivel_de_un_nodo(nodo.key)
        datos = self.avl.obtenerDatosNodo(nodo)

        poblada = self._esPoblada(evento.zonax, evento.zonay)
        asociaciones = self._obtenerAsociaciones(evento)
        return {
            "status": "activo",
            "magnitud": evento.magnitud,
            "profundidad": evento.profundidad,
            "zonax": evento.zonax,
            "zonay": evento.zonay,
            "fecha": evento.fechaHora,
            "revision": evento.revision,
            "estaciones": evento.estaciones,
            "poblada": poblada,
            "prioridad": prioridad,
            "clave": nodo.key.mostrarValores(),
            "estado": evento.estado,
            "profundidadNodo": profundidad,
            "altura": datos["altura"],
            "factor_balance": datos["factor"],
            "asociaciones": {
                "candidatos": [candidato.id for candidato in asociaciones["candidatos"]],
                "asociado": asociaciones["asociado"].id if asociaciones["asociado"] is not None else None
            }
        }


    def corregirEvento(self, idEvento:int, magnitud=None, profundidad=None, zonax=None, zonay=None, fecha=None, estaciones=None):
        nodo = self.avl.encontrarNodo(idEvento)
        if nodo is None:
            raise ValueError("El id de evento ingresado no existe")
        else:
            return self._corregirEvento(idEvento, nodo, magnitud, profundidad, zonax, zonay, fecha, estaciones)
    def _corregirEvento(self, idEvento, nodo:Nodo, magnitud=None, profundidad=None, zonax=None, zonay=None, fecha=None, estaciones=None):
        evento = nodo.evento
        key = nodo.key

        nueva_magnitud = evento.magnitud if magnitud is None else magnitud
        nueva_profundidad = evento.profundidad if profundidad is None else profundidad
        nueva_zonax = evento.zonax if zonax is None else zonax
        nueva_zonay = evento.zonay if zonay is None else zonay
        nueva_fecha = evento.fechaHora if fecha is None else fecha

        nueva_estacion = []

        if estaciones is None:
            for estacion in evento.estaciones:
                nueva_estacion.append(estacion)
        else:
            for estacion in estaciones:
                nueva_estacion.append(estacion)

        nueva_revision = evento.revision + 1

        nuevo_evento = Evento(
            idEvento,
            nueva_magnitud,
            nueva_profundidad,
            nueva_zonax,
            nueva_zonay,
            nueva_fecha,
            nueva_revision,
            nueva_estacion
        )

        nueva_key = Key(
            nuevo_evento.calcularPrioridad(
                self._esPoblada(
                    nuevo_evento.zonax,
                    nuevo_evento.zonay
                )
            ),
            nuevo_evento.magnitud,
            nuevo_evento.id
        )

        if key == nueva_key:
            nodo.evento = nuevo_evento
        else:
            self.avl.eliminar(key, self.modo_estres)
            self.avl.insertar(nueva_key, nuevo_evento, self.modo_estres)

    """  """
    def marcarRevisado(self, idEvento):
        nodo = self.avl.encontrarNodo(idEvento)

        if nodo is None:
            raise ValueError("El id de evento ingresado no existe")

        nodo.evento.marcarRevisado()

    def eliminacionIndividual(self, key:Key):
        nodo = self.avl.encontrarNodo(key.id_key)

        if nodo is None:
            raise ValueError("el evento a eliminar no existe o no está activo - (id incorrecto)")
        self.avl.eliminar(key, self.modo_estres)
        self.eliminados.add(key.id_key)
        
    

