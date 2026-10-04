from src.structures.Avl import Avl
from src.structures.Bst import Bst
from src.structures.Nodo import Nodo, Key

from src.domain.Evento import Evento
from src.domain.Zona import Zona
from src.domain.Reporte import Reporte

from src.logic.Persistencia import Persistencia

from collections import deque
from datetime import datetime, timezone, timedelta
from decimal import Decimal
from decimal import Decimal, InvalidOperation
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
        if not isinstance(valor, (int)) or valor <= 0:
            raise ValueError("W debe ser un número positivo")
        self._guardar_estado()
        self.W = float(valor)
    def actualizarR(self, valor):
        if not isinstance(valor, (int)) or valor <= 0:
            raise ValueError("R debe ser un número positivo")
        self._guardar_estado()
        self.R = float(valor)
    def actualizarL(self, valor):
        if not isinstance(valor, (int)) or valor <= 0:
            raise ValueError("L debe ser un número positivo")
        self._guardar_estado()
        self.L = float(valor)
    def actualizarT(self, valor):
        if not isinstance(valor, (int)) or valor <= 0:
            raise ValueError("T debe ser un número positivo")
        self._guardar_estado()
        self.T = float(valor)

    def crearEvento(self, idEvento, magnitud, profundidad, zonax, zonay, fecha, estacion):
        try:
            if not self._IdUnica(idEvento):
                raise ValueError("El identificador ingresado ya existe.")

            self._validarEstaciones(estacion)

            evento = Evento(idEvento, magnitud, profundidad, zonax, zonay, fecha, 1, estacion)
            self._guardar_estado()
            self._crearEvento(evento)
        except ValueError as e:
            print("error: ", e)
            raise
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
    
    def _validarEstaciones(self, estaciones):
        if not isinstance(estaciones, list):
            raise ValueError("Las estaciones deben ser una lista.")

        ids_estaciones = { estacion.id_estacion for estacion in self.estaciones }

        for id_estacion in estaciones:
            if type(id_estacion) is not str or not id_estacion.strip():
                raise ValueError(
                    "La referencia de estación debe ser un string no vacío."
                )

            if id_estacion not in ids_estaciones:
                raise ValueError(f"La estación {id_estacion} no existe en el escenario.")
            
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
            return candidatos, 0

        cola = deque([self.avl.raiz])
        nodos_examinados = 0

        while cola:
            nodo = cola.popleft()
            nodos_examinados += 1

            eventoA = nodo.evento

            if eventoA.esCandidato(eventoB, self.W, self.R):
                candidatos.append(eventoA)

            if nodo.izq is not None:
                cola.append(nodo.izq)

            if nodo.der is not None:
                cola.append(nodo.der)

        return candidatos, nodos_examinados
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

    def _obtenerAsociaciones(self, eventoB, nodos_examinados_previos=0):
        candidatos, nodos_examinados = self._buscarCandidatos(eventoB)

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
            "asociado": asociado,
            "nodos_avl_examinados": nodos_examinados_previos + nodos_examinados
        }
    def prepararReporte(
        self,
        id_evento,
        nRevision,
        magnitud,
        profundidad,
        zonax,
        zonay,
        fecha,
        estacion
    ):
        reporte = Reporte(
            id_evento,
            nRevision,
            magnitud,
            profundidad,
            zonax,
            zonay,
            fecha,
            estacion
        )

        if not self._datos_validos_reporte(reporte): raise ValueError("Los datos del reporte no son válidos.")

        self.encolarReporte(reporte)

        return reporte

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

            self._validarEstaciones([reporte.estacion])

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

        metricas_antes = self.avl.metricas.copy()

        resultado = self.procesarReporte(reporte)

        metricas_despues = self.avl.metricas

        rotaciones = {
            "izquierda": (
                metricas_despues["giros_izquierda"]
                - metricas_antes["giros_izquierda"]
            ),
            "derecha": (
                metricas_despues["giros_derecha"]
                - metricas_antes["giros_derecha"]
            ),
            "LL": (
                metricas_despues["casos_LL"]
                - metricas_antes["casos_LL"]
            ),
            "RR": (
                metricas_despues["casos_RR"]
                - metricas_antes["casos_RR"]
            ),
            "LR": (
                metricas_despues["casos_LR"]
                - metricas_antes["casos_LR"]
            ),
            "RL": (
                metricas_despues["casos_RL"]
                - metricas_antes["casos_RL"]
            )
        }
        return {
            "estacion": reporte.estacion,
            "evento": reporte.id_evento,
            "revision": reporte.nRevision,
            "estado": resultado["estado"],
            "decision": resultado["accion"],
            "rotaciones": rotaciones
        }

# dhdhdhdhdh

    def verificarEstructura(self):
        reporte = self.avl.verificarEstructura(self.modo_estres)

        inconsistentes = list(reporte.get("eventos_inconsistentes", []))
        ids_activos = {nodo.evento.id for nodo in self.avl.nodosConConteo()[0]}

        for evento in self.historico:
            if evento.id in ids_activos:
                inconsistentes.append({
                    "id": evento.id,
                    "errores": [f"Identificador duplicado entre activos e histórico: {evento.id}"],
                    "advertencias": []
                })

        for nodo in self.avl.nodosConConteo()[0]:
            evento = nodo.evento
            prioridad_esperada = evento.calcularPrioridad(
                self._esPoblada(evento.zonax, evento.zonay)
            )
            if nodo.key.prioridad != prioridad_esperada:
                inconsistentes.append({
                    "id": evento.id,
                    "errores": [
                        "prioridad de la clave no coincide: "
                        f"clave={nodo.key.prioridad}, esperado={prioridad_esperada}"
                    ],
                    "advertencias": []
                })

        reporte["eventos_inconsistentes"] = inconsistentes
        reporte["valido"] = not any(
            registro.get("errores") for registro in inconsistentes
        )
        return reporte

    def consultarEvento(self, idEvento:int):
        for evento in self.historico:
            if evento.id == idEvento:
                return {"status": "archivado"}
        if idEvento in self.eliminados:
            return {"status": "eliminado"}

        nodo, nodos_examinados = self.avl.encontrarNodoConConteo(idEvento)
        if nodo is None:
            raise ValueError("el id ingresado no existe")
        return self._consultarEvento(nodo, nodos_examinados)

    def _consultarEvento(self, nodo:Nodo, nodos_examinados=0):
        evento = nodo.evento
        prioridad = nodo.key.prioridad
        profundidad, nodos_profundidad = self.avl.nivel_de_un_nodoConConteo(nodo.key)
        datos = self.avl.obtenerDatosNodo(nodo)

        poblada = self._esPoblada(evento.zonax, evento.zonay)
        asociaciones = self._obtenerAsociaciones(
            evento,
            nodos_examinados + nodos_profundidad
        )
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
            "nodos_avl_examinados": asociaciones["nodos_avl_examinados"],
            "asociaciones": {
                "candidatos": [candidato.id for candidato in asociaciones["candidatos"]],
                "asociado": asociaciones["asociado"].id if asociaciones["asociado"] is not None else None
            }
        }

    def _datosConsultaEvento(self, nodo:Nodo, estado_registro="activo"):
        evento = nodo.evento
        return {
            "id": evento.id,
            "magnitud": evento.magnitud,
            "profundidad": evento.profundidad,
            "fecha": evento.fechaHora,
            "prioridad": nodo.key.prioridad,
            "clave": nodo.key.mostrarValores(),
            "estado": estado_registro,
            "estado_revision": evento.estado
        }

    def consultarPrimerosPendientes(self, k: int):
        if type(k) is not int or k <= 0:
            raise ValueError("k debe ser un entero positivo")

        nodos, examinados = self.avl.primerosPendientesDescendente(k)
        return {
            "eventos": [self._datosConsultaEvento(nodo) for nodo in nodos],
            "nodos_avl_examinados": examinados
        }

    def consultarPorMagnitud(self, minimo, maximo):
        minimo = Decimal(str(minimo))
        maximo = Decimal(str(maximo))

        if minimo > maximo:
            raise ValueError("El mínimo no puede ser mayor que el máximo")

        eventos = []
        nodos_examinados = 0

        for prioridad in (1, 2, 3):
            limite_inferior = Key(prioridad, minimo, 0)
            limite_superior = Key(prioridad, maximo, 999999)

            nodos, examinados = self.avl.buscarRangoConConteo(
                limite_inferior,
                limite_superior
            )

            nodos_examinados += examinados

            for nodo in nodos:
                eventos.append(self._datosConsultaEvento(nodo))

        return {
            "intervalo": (minimo, maximo),
            "eventos": eventos,
            "nodos_avl_examinados": nodos_examinados
        }

    def consultarPorProfundidadYFechas(
        self,
        profundidad_maxima,
        fecha_inicio: datetime,
        fecha_fin: datetime
    ):
        try:
            profundidad_maxima = Decimal(str(profundidad_maxima))
        except (InvalidOperation, TypeError, ValueError):
            raise ValueError("El límite de profundidad debe ser numérico")
        if not profundidad_maxima.is_finite() or profundidad_maxima < 0:
            raise ValueError("El límite de profundidad no es válido")
        if (
            not isinstance(fecha_inicio, datetime)
            or not isinstance(fecha_fin, datetime)
            or fecha_inicio.tzinfo is not timezone.utc
            or fecha_fin.tzinfo is not timezone.utc
            or fecha_inicio > fecha_fin
        ):
            raise ValueError("El intervalo de fechas UTC no es válido")

        nodos, examinados = self.avl.nodosConConteo()
        eventos = [
            self._datosConsultaEvento(nodo)
            for nodo in nodos
            if (
                nodo.evento.profundidad <= profundidad_maxima
                and fecha_inicio <= nodo.evento.fechaHora <= fecha_fin
            )
        ]
        return {
            "profundidad_maxima": profundidad_maxima,
            "intervalo_fechas": (fecha_inicio, fecha_fin),
            "eventos": eventos,
            "nodos_avl_examinados": examinados
        }

    def _estadoAsociacion(self, evento, ids_activos):
        return "activo" if evento.id in ids_activos else "archivado"

    def consultarAsociaciones(self, idEvento: int):
        nodos_activos, examinados = self.avl.nodosConConteo()
        eventos_activos = [nodo.evento for nodo in nodos_activos]

        ids_activos = {evento.id for evento in eventos_activos}

        evento = next(
            (evento_activo for evento_activo in eventos_activos
            if evento_activo.id == idEvento),
            None
        )

        if evento is None:
            evento = next(
                (historico for historico in self.historico
                if historico.id == idEvento),
                None
            )

        if evento is None:
            raise ValueError(
                "El id ingresado no existe en activos ni en el histórico"
            )

        eventos = eventos_activos + self.historico

        candidatos_por_id = {}
        referencia_por_id = {}

        for eventoB in eventos:
            candidatos = []

            for eventoA in eventos:
                if eventoA.id == eventoB.id:
                    continue

                if eventoA.esCandidato(eventoB, self.W, self.R):
                    candidatos.append(eventoA)

            candidatos_por_id[eventoB.id] = candidatos
            referencia_por_id[eventoB.id] = (
                self._seleccionarCandidato(candidatos, eventoB)
            )

        candidatos = candidatos_por_id[evento.id]
        referencia = referencia_por_id[evento.id]

        referenciado_por = []

        for evento_consultado in eventos:
            if evento_consultado.id == evento.id:
                continue

            if referencia_por_id[evento_consultado.id] is evento:
                referenciado_por.append({
                    "id": evento_consultado.id,
                    "estado": self._estadoAsociacion(
                        evento_consultado,
                        ids_activos
                    )
                })

        estado_evento = self._estadoAsociacion(
            evento,
            ids_activos
        )

        return {
            "evento": {
                "id": evento.id,
                "estado": estado_evento
            },
            "candidatos": [
                {
                    "id": candidato.id,
                    "estado": self._estadoAsociacion(
                        candidato,
                        ids_activos
                    )
                }
                for candidato in candidatos
            ],
            "referencia_elegida": (
                {
                    "id": referencia.id,
                    "estado": self._estadoAsociacion(
                        referencia,
                        ids_activos
                    )
                }
                if referencia is not None else None
            ),
            "referenciado_por": referenciado_por,
            "nodos_avl_examinados": examinados
        }

    def consultarEventosCostosos(self):
        return self._indicadorEventosCostosos()

    def compararOrdenesInsercion(self, ordenes=None):
        nodos, _ = self.avl.nodosConConteo()
        nodos_por_id = {nodo.evento.id: nodo for nodo in nodos}
        ids_ascendentes = [
            nodo.evento.id for nodo in sorted(nodos, key=lambda nodo: nodo.key)
        ]
        if ordenes is None:
            ordenes = {
                "ascendente": ids_ascendentes,
                "descendente": list(reversed(ids_ascendentes))
            }

        resultados = {}
        for nombre, ids_orden in ordenes.items():
            if len(ids_orden) != len(ids_ascendentes) or set(ids_orden) != set(ids_ascendentes):
                raise ValueError("Cada orden debe incluir una vez todos los eventos activos")

            avl = Avl()
            bst = Bst()
            for id_evento in ids_orden:
                nodo_original = nodos_por_id[id_evento]
                avl.insertar(nodo_original.key, nodo_original.evento, False)
                bst.insertar(nodo_original.key, nodo_original.evento)

            comparaciones_por_clave = []
            comparaciones_avl = 0
            comparaciones_bst = 0
            for nodo_original in nodos:
                _, visitas_avl = avl.buscarConConteo(nodo_original.key)
                _, visitas_bst = bst.buscarConConteo(nodo_original.key)
                comparaciones_avl += visitas_avl
                comparaciones_bst += visitas_bst
                comparaciones_por_clave.append({
                    "id": nodo_original.evento.id,
                    "avl": visitas_avl,
                    "bst": visitas_bst
                })

            resultados[nombre] = {
                "altura_avl": avl.altura(),
                "hojas_avl": avl.hojas(),
                "altura_bst": bst.altura(),
                "hojas_bst": bst.hojas(),
                "comparaciones_avl": comparaciones_avl,
                "comparaciones_bst": comparaciones_bst,
                "comparaciones_por_clave": comparaciones_por_clave
            }

        return resultados


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
            self._validarEstaciones(estaciones)
            nueva_estacion = evento.estaciones.copy()

            for estacion in estaciones:
                if estacion not in nueva_estacion:
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

        self.avl.recuperar()
        reporte = self.avl.verificarEstructura(False)
        if not reporte["valido"] or not reporte["equilibrado"]:
            self.deshacer()
            raise ValueError("La recuperación del AVL no logró restablecer una estructura válida y equilibrada.")

        self.modo_estres = False
        self._registrar_accion("recuperacion", {})

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

        nodos_con_profundidad, examinados = self.avl.nodosConProfundidadYConteo()
        for nodo, profundidad in nodos_con_profundidad:
            if nodo.key.prioridad == 3 and profundidad > self.L:
                encontrado, visitas = self.avl.buscarConConteo(nodo.key)
                if encontrado is not None:
                    eventos.append((nodo, profundidad, visitas))

        return {
            "cantidad": len(eventos),
            "limite": self.L,
            "nodos_avl_examinados": examinados,
            "eventos": [
                {
                    **self._datosIndicadorEvento(nodo, profundidad),
                    "limite": self.L,
                    "nodos_visitados_busqueda": visitas
                }
                for nodo, profundidad, visitas in eventos
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

        resultado = persistencia.cargarInserciones(datos, self.zonas, self.estaciones)

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

        resultado = persistencia.cargarTopologia(datos, self.zonas, self.estaciones)

        if not self.modo_estres and not resultado["balanceado"]:
            raise ValueError("la topologia del arbol esta desbalanceada: no puede cargarse en modo normal")
        
        self._guardar_estado()

        self.avl = resultado["avl"]
        return {
            "tipo": "topologia",
            "avl": persistencia._serializarArbol(self.avl)
        }

    def cargarEscenario(self, datos:dict):
        persistencia = Persistencia()
        estado = persistencia.cargarEscenario(datos)
        self._guardar_estado()
        self._restaurarEstado(estado)

    def guardarEscenario(self):
        persistencia = Persistencia()
        return persistencia.guardarEscenario(self)   

    def obtenerDatosMapa(self):
        datos = []
        def recorrer(nodo):
            if nodo is None:
                return
            recorrer(nodo.izq)
            evento = nodo.evento
            datos.append({
                "id": evento.id,
                "x": float(evento.zonax),
                "y": float(evento.zonay),
                "prioridad": nodo.key.prioridad
            })
            recorrer(nodo.der)
        recorrer(self.avl.raiz)
        return datos

    def obtener_nodos(self, avl, bst):
        return {
            "avl": {
                "raiz": avl.raiz.key.id_key if avl.raiz is not None else None,
                "nodos": self._obtener_nodos(avl, True)
            },
            "bst": {
                "raiz": bst.raiz.key.id_key if bst.raiz is not None else None,
                "nodos": self._obtener_nodos(bst, False)
            }
    }

    def _obtener_nodos(self, arbol, es_avl):
        nodos = []

        def recorrer(nodo, profundidad=0):
            if nodo is None:
                return

            nodos.append({
                "id": nodo.key.id_key,
                "prioridad": nodo.key.prioridad,
                "magnitud": nodo.key.magnitud,
                "profundidad": profundidad,
                "altura": nodo.altura,
                "factor": self.avl._factor_balance(nodo) if es_avl else None,
                "izq": nodo.izq.key.id_key if nodo.izq is not None else None,
                "der": nodo.der.key.id_key if nodo.der is not None else None
            })

            recorrer(nodo.izq, profundidad + 1)
            recorrer(nodo.der, profundidad + 1)

        recorrer(arbol.raiz)
        return nodos