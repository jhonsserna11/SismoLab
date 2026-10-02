from src.structures.Avl import Avl
from src.structures.Bst import Bst
from src.structures.Nodo import Nodo, Key

from src.domain.Evento import Evento
from src.domain.Zona import Zona

from src.logic.Persistencia import Persistencia

from collections import deque
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from copy import deepcopy

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

        self.metricas = {
            "correcciones_aceptadas": 0,
            "reportes_descartados": 0,
            "conflictos": 0,
            "archivos_masivos": 0,
            "eventos_archivados": 0,
        }

    def actualizarW(self, valor):
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ValueError("W debe ser un número positivo")
        self._guardar_estado()
        self.W = float(valor)
    def actualizarR(self, valor):
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ValueError("R debe ser un número positivo")
        self._guardar_estado()
        self.R = float(valor)
    def actualizarL(self, valor):
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ValueError("L debe ser un número positivo")
        self._guardar_estado()
        self.L = float(valor)
    def actualizarT(self, valor):
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ValueError("T debe ser un número positivo")
        self._guardar_estado()
        self.T = float(valor)

    def crearEvento(self, idEvento, magnitud, profundidad, zonax, zonay, fecha, estacion):
        try:
            if not self._IdUnica(idEvento):
                raise ValueError("El identificador ingresado ya existe.")

            evento = Evento(idEvento, magnitud, profundidad, zonax, zonay, fecha, 1, estacion)
            self._guardar_estado()
            self._crearEvento(evento)
        except ValueError as e:
            print("error: ", e)
    def _crearEvento(self, evento:Evento):
        prioridad = evento.calcularPrioridad(self._esPoblada(evento.zonax, evento.zonay))
        key = Key(prioridad, evento.magnitud, evento.id)
        self.avl.insertar(key, evento, self.modo_estres)
        self.bst.insertar(key, evento)


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
        self._guardar_estado()
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
    def _normalizar_decimal(self, valor):
        return Decimal(str(valor))

    def _datos_iguales(self, evento: Evento, reporte):
        return (
            evento.magnitud == self._normalizar_decimal(reporte.magnitud) and
            evento.profundidad == self._normalizar_decimal(reporte.profundidad) and
            evento.zonax == self._normalizar_decimal(reporte.zonax) and
            evento.zonay == self._normalizar_decimal(reporte.zonay) and
            evento.fechaHora == reporte.fecha
        )

    def _datos_validos_reporte(self, reporte):
        try:
            if not isinstance(reporte.fecha, datetime):
                raise ValueError("Fecha no tiene estructura válida")
            if reporte.fecha.tzinfo is not timezone.utc or reporte.fecha.microsecond != 0:
                raise ValueError("Fecha no tiene estructura válida")

            Evento(
                reporte.id_evento,
                reporte.magnitud,
                reporte.profundidad,
                reporte.zonax,
                reporte.zonay,
                reporte.fecha,
                reporte.nRevision,
                [reporte.estacion]
            )
            return True
        except (ValueError, TypeError):
            return False

    def  _confirmarEvento(self, evento: Evento, reporte):
        if reporte.estacion not in evento.estaciones:
            evento.estaciones.append(reporte.estacion)
        return {"estado": "confirmado", "accion": "confirmar"}

    def _actualizarEventoReporte(self, nodo: Nodo, reporte):
        evento = nodo.evento
        id_original = evento.id
        revision_original = evento.revision
        estaciones_originales = evento.estaciones.copy()
        datos_originales = {
            "magnitud": evento.magnitud,
            "profundidad": evento.profundidad,
            "zonax": evento.zonax,
            "zonay": evento.zonay,
            "fechaHora": evento.fechaHora,
            "estado": evento.estado,
            "key": nodo.key,
        }

        try:
            evento_nuevo = Evento(
                id_original,
                reporte.magnitud,
                reporte.profundidad,
                reporte.zonax,
                reporte.zonay,
                reporte.fecha,
                reporte.nRevision,
                estaciones_originales + ([reporte.estacion] if reporte.estacion not in estaciones_originales else [])
            )

            evento_nuevo.estado = "Pendiente"

            nueva_key = Key(
                evento_nuevo.calcularPrioridad(self._esPoblada(evento_nuevo.zonax, evento_nuevo.zonay)),
                evento_nuevo.magnitud,
                evento_nuevo.id
            )

            nodo_bst = self.bst.buscar(nodo.key)
            if nodo_bst is None:
                raise RuntimeError("AVL y BST están desincronizados")

            if nodo.key != nueva_key:
                self.avl.eliminar(nodo.key, self.modo_estres)
                self.bst.eliminar(nodo.key)

                self.avl.insertar(nueva_key, evento_nuevo, self.modo_estres)
                self.bst.insertar(nueva_key, evento_nuevo)
            else:
                nodo.evento = evento_nuevo
                nodo.key = nueva_key

                nodo_bst.evento = evento_nuevo
                nodo_bst.key = nueva_key

            self.metricas["correcciones_aceptadas"] += 1
            return {"estado": "actualizado", "accion": "sustituir"}
        except (ValueError, TypeError):
            nodo.evento = evento
            nodo.key = datos_originales["key"]
            evento.magnitud = datos_originales["magnitud"]
            evento.profundidad = datos_originales["profundidad"]
            evento.zonax = datos_originales["zonax"]
            evento.zonay = datos_originales["zonay"]
            evento.fechaHora = datos_originales["fechaHora"]
            evento.estado = datos_originales["estado"]
            evento.revision = revision_original
            evento.estaciones = estaciones_originales
            self.metricas["reportes_descartados"] += 1
            return {"estado": "desconocido", "accion": "rechazar"}

    def _reactivarEventoArchivado(self, reporte):
        for evento in self.historico:
            if evento.id == reporte.id_evento:
                estaciones_reactivadas = evento.estaciones.copy()
                if reporte.estacion not in estaciones_reactivadas:
                    estaciones_reactivadas.append(reporte.estacion)

                nuevo_evento = Evento(
                    evento.id,
                    reporte.magnitud,
                    reporte.profundidad,
                    reporte.zonax,
                    reporte.zonay,
                    reporte.fecha,
                    reporte.nRevision,
                    estaciones_reactivadas 
                )
                nuevo_evento.estado = "Pendiente"
                self.historico.remove(evento)
                self._crearEvento(nuevo_evento)
                return {"estado": "reactivado", "accion": "reactivar"}
        return {"estado": "archivado", "accion": "descartar"}

    def procesarReporte(self, reporte):
        if not self._datos_validos_reporte(reporte):
            self.metricas["reportes_descartados"] += 1
            return {"estado": "desconocido", "accion": "rechazar"}

        if reporte.id_evento in self.eliminados:
            self.metricas["reportes_descartados"] += 1
            return {"estado": "eliminado", "accion": "rechazar"}

        nodo = self.avl.encontrarNodo(reporte.id_evento)
        if nodo is not None:
            evento = nodo.evento

            if reporte.nRevision < evento.revision:
                self.metricas["reportes_descartados"] += 1
                return {"estado": "antiguo", "accion": "descartar"}

            if reporte.nRevision > evento.revision:
                return self._actualizarEventoReporte(nodo, reporte)

            if self._datos_iguales(evento, reporte):
                return self._confirmarEvento(evento, reporte)

            self.metricas["conflictos"] += 1
            return {"estado": "conflicto", "accion": "rechazar"}

        for evento in self.historico:
            if evento.id == reporte.id_evento:
                if reporte.nRevision > evento.revision:
                    return self._reactivarEventoArchivado(reporte)
                self.metricas["reportes_descartados"] += 1
                return {"estado": "archivado", "accion": "descartar"}

        if not self._IdUnica(reporte.id_evento):
            self.metricas["reportes_descartados"] += 1
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
        if not self.cola_reportes:
            return None
        self._guardar_estado()
        
        reporte = self.desencolarSiguienteReporte()
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
        self._guardar_estado()

        evento = nodo.evento
        key = nodo.key

        nodo_bst = self.bst.buscar(key)
        if nodo_bst is None:
            raise RuntimeError("AVL y BST están desincronizados")   

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
            nodo_bst.evento = nuevo_evento
        else:
            self.avl.eliminar(key, self.modo_estres)
            self.bst.eliminar(key)

            self.avl.insertar(nueva_key, nuevo_evento, self.modo_estres)
            self.bst.insertar(nueva_key, nuevo_evento)
        self.metricas["correcciones_aceptadas"] += 1
    """  """
    def marcarRevisado(self, idEvento):
        nodo = self.avl.encontrarNodo(idEvento)

        if nodo is None:
            raise ValueError("El id de evento ingresado no existe")
        self._guardar_estado()
        nodo.evento.marcarRevisado()

    def eliminacionIndividual(self, key:Key):
        if type(key) is not Key:
            raise ValueError("La key ingresada es invalida (debe ser type Key)")
        nodo = self.avl.encontrarNodo(key.id_key)
        if nodo is None:
            raise ValueError("el evento a eliminar no existe o no está activo - (id incorrecto)")
        self._guardar_estado()
        self.avl.eliminar(key, self.modo_estres)
        self.bst.eliminar(key)
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
        self._guardar_estado()
        for nodo in nodos:
            evento = nodo.evento
            key = nodo.key
            self.historico.append(evento)
            self.avl.eliminar(key, self.modo_estres)
            self.bst.eliminar(key)
            self.metricas["eventos_archivados"] += 1
        self.metricas["archivos_masivos"] += 1

        
    def recuperarArbol(self):
        self._guardar_estado()
        #pausar procesamiento de reportes

        self.avl.recuperar()

        #llamar bloque auditoria
        #recibo OK

        self.modo_estres = False

    def obtenerIndicadores(self):
        return {
            "metricasAcumulativas": self.metricas,
            "metricasAVL": self.avl.metricas,
            "eventos_activos": self.avl.peso(),
            "eventos_historicos": len(self.historico),
            "altura_avl": self.avl.altura(),
            "hojas": self.avl.hojas(),
            "inorden": self.avl.inOrder(),
            "preorden": self.avl.pre_order(),
            "postorden": self.avl.post_order(),
            "anchura": self.avl.anchura(),
            "eventos_por_prioridad": self._indicadorEventosPorPrioridad(),
            "eventos_pendientes": self._indicadorEventosPendientes(),
            "eventos_costosos": self._indicadorEventosCostosos()
        }

    def _datosIndicadorEvento(self, nodo, profundidad=None):
        evento = nodo.evento

        datos = {
            "id": evento.id,
            "magnitud": evento.magnitud,
            "profundidad": evento.profundidad,
            "zonax": evento.zonax,
            "zonay": evento.zonay,
            "fecha": evento.fechaHora,
            "prioridad": nodo.key.prioridad,
            "estado": evento.estado
        }

        if profundidad is not None:
            datos["profundidad_nodo"] = profundidad

        return datos
    
    def _indicadorEventosPorPrioridad(self):
        grupos = self.avl.eventos_por_prioridad()

        return {
            prioridad: {
                "cantidad": len(nodos),
                "eventos": [
                    self._datosIndicadorEvento(nodo) for nodo in nodos
                ]
            }
            for prioridad, nodos in grupos.items()
        }

    def _indicadorEventosPendientes(self):
        pendientes = self.avl.eventos_pendientes()

        return {
                "cantidad": len(pendientes),
                "eventos": [
                      self._datosIndicadorEvento(nodo) for nodo in pendientes
                   ]
           }

    def _indicadorEventosCostosos(self):
        eventos = []

        for nodo, profundidad in self.avl.nodos_con_profundidad():
            if nodo.key.prioridad == 3 and profundidad > self.L:
                eventos.append((nodo, profundidad))

        return {
            "cantidad": len(eventos),
            "eventos": [
                self._datosIndicadorEvento(nodo, profundidad)
                for nodo, profundidad in eventos
            ]
        }

    def deshacer(self):
        if not self.pila_deshacer:
            return False
        estado = self.pila_deshacer.pop()
        self._restaurarEstado(estado)
        return True
    def _restaurarEstado(self, estado):
        self.avl = estado["avl"]
        self.bst = estado["bst"]
        self.estaciones = estado["estaciones"]
        self.zonas = estado["zonas"]
        self.historico = estado["historico"]
        self.eliminados = estado["eliminados"]

        self.W = estado["W"]
        self.R = estado["R"]
        self.L = estado["L"]
        self.T = estado["T"]

        self.modo_estres = estado["modo_estres"]
        self.reloj = estado["reloj"]

        self.metricas = estado["metricas"]
        self.cola_reportes = estado["cola_reportes"]

    def _guardar_estado(self):
        estado = {
            "avl": deepcopy(self.avl),
            "bst": deepcopy(self.bst),
            "estaciones": deepcopy(self.estaciones),
            "zonas": deepcopy(self.zonas),
            "historico": deepcopy(self.historico),
            "eliminados": deepcopy(self.eliminados),
            "W": self.W,
            "R": self.R,
            "L": self.L,
            "T": self.T,
            "modo_estres": self.modo_estres,
            "metricas": deepcopy(self.metricas),
            "cola_reportes": deepcopy(self.cola_reportes),
            "reloj": deepcopy(self.reloj)
            }
        self.pila_deshacer.append(estado)


    def cargarInserciones(self, datos:dict):
        persistencia = Persistencia()

        resultado = persistencia.cargarInserciones(datos, self.zonas)

        nuevo_avl = resultado.get("avl")
        nuevo_bst = resultado.get("bst")

        if not isinstance(nuevo_avl, Avl):
            raise RuntimeError("La carga por inserciones no produjo un AVL válido.")

        if not isinstance(nuevo_bst, Bst):
            raise RuntimeError("La carga por inserciones no produjo un BST válido.")

        self._guardar_estado()

        self.avl = nuevo_avl
        self.bst = nuevo_bst
        self.historico = []
        self.eliminados = set()

        return {
            "tipo": "inserciones",
            "avl": persistencia._serializarArbol(self.avl),
            "bst": persistencia._serializarArbol(self.bst)
        }

    def cargarTopologia(self, datos:dict):
        persistencia = Persistencia()

        resultado = persistencia.cargarTopologia(datos, self.zonas)

        if not self.modo_estres and not resultado["balanceado"]:
            raise ValueError("la topologia del arbol esta desbalanceada: no puede cargarse en modo normal")
        
        self._guardar_estado()

        self.avl = resultado["avl"]
        return {
            "tipo": "topologia",
            "avl": persistencia._serializarArbol(self.avl)
        }
