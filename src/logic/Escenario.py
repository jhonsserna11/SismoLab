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

    
    def _esMejorCandidato(self, candidatoA, candidatoB):
        if candidatoA is None:
            return candidatoB
        if candidatoB is None:
            return candidatoA

        if candidatoA["cantidad"] > candidatoB["cantidad"]:
            return candidatoA

        if candidatoA["cantidad"] < candidatoB["cantidad"]:
            return candidatoB

        profundidadA = self.avl.nivel_de_un_nodo(candidatoA["nodo"].key)
        profundidadB = self.avl.nivel_de_un_nodo(candidatoB["nodo"].key)

        if profundidadA > profundidadB:
            return candidatoA

        if profundidadA < profundidadB:
            return candidatoB

        if candidatoA["nodo"].key.id_key > candidatoB["nodo"].key.id_key:
            return candidatoA
        return candidatoB

    def obtenerRamaArchivable(self):
        return self._obtenerRamaArchivable(self.avl.raiz)
    def _obtenerRamaArchivable(self, subraiz:Nodo):
        if self.avl.raiz is None:
            return None

        if subraiz is None:
            return {
                "elegible": True,
                "cantidad": 0,
                "mejor": None
            }

        subizq = self._obtenerRamaArchivable(subraiz.izq)
        subder = self._obtenerRamaArchivable(subraiz.der)

        cantidad = 1 + subizq["cantidad"] + subder["cantidad"]

        subraiz_cumple = (
            subraiz.key.prioridad == 1
            and self.calcularAntiguedad(subraiz.evento.fechaHora) > self.T
        )

        elegible = (
            subraiz_cumple
            and subizq["elegible"]
            and subder["elegible"]
        )

        mejor = self._esMejorCandidato(
            subizq["mejor"],
            subder["mejor"]
        )

        if elegible:
            candidato_actual = {
                "nodo": subraiz,
                "cantidad": cantidad
            }

            mejor = self._esMejorCandidato(
                mejor,
                candidato_actual
            )

        return {
            "elegible": elegible,
            "cantidad": cantidad,
            "mejor": mejor
        }

    def calcularAntiguedad(self, fechaEvento:datetime):
        diferencia = self.reloj - fechaEvento
        return diferencia.total_seconds()/3600

    def _obtenerNodosSubarbol(self, subraiz:Nodo):
        if subraiz.esHoja():
            return [subraiz]
        nodos = []
        nodos.append(subraiz)
        izq = self._obtenerNodosSubarbol(subraiz.izq)
        der = self._obtenerNodosSubarbol(subraiz.der)
        for nodo in izq: nodos.append(nodo)
        for nodo in der: nodos.append(nodo)
        return nodos

    def archivarRama(self, subraiz:Nodo):
        if subraiz is None:
            raise ValueError("No hay rama elegible para archivar")
        nodos = self._obtenerNodosSubarbol(subraiz)
        for nodo in nodos:
            self.historico.append(nodo.evento) 
            self.avl.eliminar(nodo.key, self.modo_estres)

        

        


