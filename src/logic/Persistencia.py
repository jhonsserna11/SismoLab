from datetime import datetime, timezone

from src.domain.Evento import Evento
from src.structures.Avl import Avl
from src.structures.Bst import Bst
from src.structures.Nodo import Key


class Persistencia:

    def cargarInserciones(self, datos, zonas):
        if not isinstance(datos, dict):
            raise ValueError("El archivo debe contener un objeto JSON.")

        if datos.get("tipo_carga") != "inserciones":
            raise ValueError(
                "El archivo no corresponde a una carga por inserciones."
            )

        eventos = datos.get("eventos")

        if not isinstance(eventos, list):
            raise ValueError(
                "El campo 'eventos' debe ser una lista."
            )

        avl = Avl()
        bst = Bst()
        ids = set()

        for datos_evento in eventos:

            if not isinstance(datos_evento, dict):
                raise ValueError(
                    "Cada elemento de 'eventos' debe ser un objeto."
                )
            campos_obligatorios = {
                "id",
                "magnitud",
                "profundidad",
                "zonax",
                "zonay",
                "fechaHora",
                "revision",
                "estaciones"
            }

            faltantes = campos_obligatorios - datos_evento.keys()

            if faltantes:
                raise ValueError(
                    f"Faltan campos obligatorios: {sorted(faltantes)}"
                )

            id_evento = datos_evento.get("id")

            if id_evento in ids:
                raise ValueError(
                    f"El identificador {id_evento} está repetido."
                )

            ids.add(id_evento)

            fecha = self._fechaDesdeJson(
                datos_evento.get("fechaHora")
            )

            evento = Evento(
                id_evento,
                datos_evento.get("magnitud"),
                datos_evento.get("profundidad"),
                datos_evento.get("zonax"),
                datos_evento.get("zonay"),
                fecha,
                datos_evento.get("revision"),
                datos_evento.get("estaciones")
            )

            poblada = self._esPoblada(
                zonas,
                evento.zonax,
                evento.zonay
            )

            prioridad = evento.calcularPrioridad(poblada)

            key = Key(
                prioridad,
                evento.magnitud,
                evento.id
            )

            # La carga por inserciones exige AVL balanceado.
            avl.insertar(key, evento, False)

            # BST sin balanceo.
            bst.insertar(key, evento)

        return {
            "tipo": "inserciones",
            "avl": self._serializarArbol(avl),
            "bst": self._serializarArbol(bst)
        }

    def _esPoblada(self, zonas, zonax, zonay):
        for zona in zonas:
            if zona.contiene(zonax, zonay) and zona.es_poblada():
                return True

        return False

    def _serializarArbol(self, arbol):
        arbol.altura()
        nodos = []

        def recorrer(nodo, profundidad):
            if nodo is None:
                return

            datos = {
                "id": nodo.key.id_key,
                "evento": {
                    "id": nodo.evento.id,
                    "magnitud": float(nodo.evento.magnitud),
                    "profundidad": float(nodo.evento.profundidad),
                    "zonax": float(nodo.evento.zonax),
                    "zonay": float(nodo.evento.zonay),
                    "fechaHora": nodo.evento.fechaHora.isoformat(),
                    "revision": nodo.evento.revision,
                    "estaciones": nodo.evento.estaciones,
                    "estado": nodo.evento.estado
                },
                "prioridad": nodo.key.prioridad,
                "profundidad": profundidad,
                "altura": nodo.altura,
                "izquierda": (
                    nodo.izq.key.id_key
                    if nodo.izq is not None
                    else None
                ),
                "derecha": (
                    nodo.der.key.id_key
                    if nodo.der is not None
                    else None
                )
            }

            if type(arbol) is Avl:
                datos["factor"] = (
                    (nodo.izq.altura if nodo.izq is not None else -1)
                    - (nodo.der.altura if nodo.der is not None else -1)
                )

            nodos.append(datos)

            recorrer(nodo.izq, profundidad + 1)
            recorrer(nodo.der, profundidad + 1)

        recorrer(arbol.raiz, 0)

        return {
            "raiz": (
                arbol.raiz.key.id_key
                if arbol.raiz is not None
                else None
            ),
            "altura": arbol.altura(),
            "profundidad_maxima": (
                max(nodo["profundidad"] for nodo in nodos)
                if nodos
                else -1
            ),
            "hojas": arbol.hojas(),
            "nodos": nodos
        }
    
    def _fechaDesdeJson(self, valor):
        if not isinstance(valor, str):
            raise ValueError(
                "La fecha debe ser una cadena."
            )

        try:
            if valor.endswith("Z"):
                valor = valor[:-1] + "+00:00"

            fecha = datetime.fromisoformat(valor)

        except ValueError:
            raise ValueError(
                "La fecha no tiene un formato ISO 8601 válido."
            )

        if fecha.tzinfo is None:
            raise ValueError(
                "La fecha debe incluir zona horaria."
            )

        return fecha.astimezone(timezone.utc)