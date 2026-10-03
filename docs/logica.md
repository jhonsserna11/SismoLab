# Módulo de lógica

Este módulo concentra la lógica de negocio del proyecto. Aquí se define el comportamiento del sistema: cómo se crean los eventos, cómo se validan, cómo se relacionan entre sí y cómo se responden las consultas.

## 1. `Escenario`

Archivo: `src/logic/Escenario.py`

### Responsabilidad

`Escenario` es la clase central del sistema. Es el punto de coordinación entre el dominio, las estructuras y las consultas. En otras palabras, un objeto `Escenario` representa el “mundo operativo” del sistema.

### Atributos principales

- `avl`: árbol principal donde viven los eventos activos.
- `bst`: árbol paralelo usado para comparar y verificar comportamiento.
- `historico`: lista de eventos archivados.
- `eliminados`: conjunto de ids que ya no están activos.
- `zonas`: zonas geográficas disponibles en el escenario.
- `estaciones`: estaciones de medición registradas.
- `reloj`: referencia temporal del sistema.
- `W`, `R`, `L`, `T`: parámetros del escenario, utilizados para candidatos, tiempos y antigüedad.
- `metricas`: contadores acumulados de reportes, conflictos y archivados.

### Estructura lógica

`Escenario` reúne todo lo necesario para:

- crear nuevos eventos,
- validar su contenido,
- aceptar y evaluar reportes,
- relacionar eventos por distancia y tiempo,
- consultar eventos según distintos criterios,
- conservar un histórico para análisis y recuperación.

## 2. Funciones y métodos más importantes

### `__init__(w, r, l, t, reloj)`

Inicializa todas las estructuras del sistema. Crea tanto el AVL como el BST, deja listas las colecciones de zonas, estaciones y eventos históricos, y reserva el estado para poder hacer deshacer.

Su papel es preparar el escenario para que el resto de las operaciones puedan ejecutarse con coherencia.

### `actualizarW()`, `actualizarR()`, `actualizarL()`, `actualizarT()`

Estos métodos ajustan los parámetros del escenario. Cada uno valida que el valor recibido sea positivo y luego guarda el estado previo para poder deshacer el cambio si hace falta.

La idea es que el sistema pueda adaptar la sensibilidad de las reglas sin perder capacidad de recuperación.

### `crearEvento(idEvento, magnitud, profundidad, zonax, zonay, fecha, estacion)`

Este método es la entrada principal para registrar un nuevo sismo. Primero valida que el id sea único, que la estación exista y que el evento cumpla las reglas del dominio.

Luego llama a `_crearEvento()`, que calcula la prioridad y lo inserta en el AVL y en el BST.

### `_crearEvento(evento)`

Este es el paso real de inserción. El método:

1. calcula la prioridad del evento usando la zona poblada,
2. crea su `Key` compuesta por prioridad, magnitud e id,
3. inserta el evento en el AVL,
4. inserta el mismo evento en el BST.

Es aquí donde la lógica del negocio y la estructura de datos se juntan.

### `_IdUnica(id)`

Verifica que un id no esté repetido en los eventos activos, históricos ni en el conjunto de eliminados. Si el id ya existe, se descarta la operación.

Esto evita inconsistencias en la trazabilidad del sistema.

### `_validarEstaciones(estaciones)`

Se asegura de que la lista de estaciones sea válida y que cada una exista dentro del escenario. Si no, lanza un error. Es una validación clave porque el sistema no solo almacena eventos, sino que mantiene la procedencia de la información.

### `_esPoblada(zonax, zonay)`

Revisa cada zona del escenario y determina si la coordenada pertenece a una zona marcada como poblada. Si el evento está en una zona poblada, su prioridad puede aumentar.

Este método conecta la geografía del problema con la lógica de nivel de riesgo.

## 3. Lógica de asociación entre eventos

### `_buscarCandidatos(eventoB)`

Recorre el AVL en anchura usando una cola. Para cada nodo, compara el evento con `eventoB` usando `esCandidato()`. Si cumple la regla de distancia, tiempo y magnitud, se agrega a la lista de candidatos.

Esto hace que el sistema busque relaciones entre todos los eventos activos sin depender solo del último ingresado.

### `_agregarCandidatosArchivados(eventoB, candidatos)`

Además de revisar eventos activos, el sistema también puede considerar eventos históricos. Eso permite evaluar si el evento de referencia podría estar relacionado incluso si ya fue archivado.

### `_seleccionarCandidato(candidatos, eventoB)`

Entre todos los candidatos, selecciona el mejor. La lógica aplica estos criterios:

1. el evento con mayor magnitud gana,
2. si hay empate, el más cercano en tiempo gana,
3. si sigue empatado, el id menor decide.

Esto genera una selección determinista y útil para el análisis de asociación. 

### `_obtenerAsociaciones(eventoB)`

Este método reúne la lista de candidatos y la elección final en un diccionario con:

- `candidatos`,
- `asociado`.

Es la base para consultas de relación entre eventos.

## 4. Manejo de reportes

### `encolarReporte(reporte)`

Agrega un reporte a la cola para procesarlo después. La cola convierte el sistema en una estructura ordenada para reportes pendientes.

### `desencolarSiguienteReporte()`

Extrae el próximo reporte de la cola. Es el método que permite consumir la información de manera secuencial.

### `_normalizar_decimal(valor)`

Normaliza valores decimales para comparar datos con el tipo esperado del dominio. Esto ayuda a manejar magnitudes y coordenadas sin errores por representación.

### `_datos_iguales(evento, reporte)`

Compara si los datos actuales del evento son iguales a los que trae el reporte. Si coincide, el sistema asume que el reporte solo confirma la información existente.

### `_datos_validos_reporte(reporte)`

Valida si el reporte tiene una fecha válida, estaciones conocidas, y si el contenido puede convertirse en un `Evento` sin romper invariantes del dominio.

### `_confirmarEvento(evento, reporte)`

Si el reporte confirma los datos actuales, solo se agrega la estación que lo emitió si no estaba ya incluida. Es una operación ligera y útil para consolidar evidencia.

### `_actualizarEventoReporte(nodo, reporte)`

Este es uno de los métodos centrales del sistema. Cuando llega un reporte con una revisión mayor, se crea una versión nueva del evento con la información corregida y se actualiza la clave principal del árbol.

La lógica es:

1. recuperar el evento actual del nodo,
2. crear un nuevo `Evento` con los datos del reporte,
3. recalcular la `Key`,
4. si la clave cambia, eliminar el nodo viejo y volver a insertar el nuevo,
5. si no cambia, reemplazar solo los datos del evento,
6. registrar la corrección aceptada en métricas.

Si la estructura de datos se rompe por un valor inválido, el método revierte a un estado anterior y descarta el reporte.

### `_reactivarEventoArchivado(reporte)`

Si el evento ya está en el histórico, se reconstruye un nuevo evento con la información del nuevo reporte y se vuelve a insertar en el AVL. El sistema actúa como si el evento “volviera a estar activo”.

### `procesarReporte(reporte)`

Es el método de orquestación para el flujo completo de un reporte. Decide si:

- el reporte es válido,
- el evento existe y está activo,
- la revisión es antigua,
- el evento está archivado,
- el reporte es un conflicto,
- el evento debe ser registrado como nuevo.

Es decir, este método resuelve la decisión final sobre el reporte.

## 5. Consultas y análisis de eventos

### `consultarEvento(idEvento)`

Busca un evento por id y devuelve su estado. Si está archivado, devuelve `archivado`; si está eliminado, devuelve `eliminado`; si está activo, devuelve el detalle completo del objeto.

### `_consultarEvento(nodo)`

Extrae una vista detallada del evento, incluyendo:

- magnitud,
- profundidad,
- coordenadas,
- fecha,
- revisión,
- estaciones,
- prioridad,
- clave,
- estado,
- profundidad del nodo,
- altura,
- factor de balance,
- asociaciones.

Es una consulta de diagnóstico muy útil para comprender la situación exacta de un evento.

### `corregirEvento(...)`

Permite modificar los datos de un evento activo sin dejar su estructura inconsistente. El método:

1. valida que el id exista,
2. toma los valores actuales o los nuevos,
3. crea un evento corregido,
4. calcula la nueva clave,
5. si cambia la clave puede reinsertarse el evento,
6. actualiza las métricas de corrección.

### `marcarRevisado(idEvento)`

Actualiza el estado del evento a `Revisado` y guarda el estado anterior para poder deshacer.

### `eliminacionIndividual(key)`

Elimina un evento activo usando la `Key` asociada. También lo agrega al conjunto `eliminados`, con lo que se preserva el historial de exclusiones.

## 6. Gestión del estado y recuperación

### `_guardar_estado()`

Hace una copia profunda del estado del escenario y la guarda en la pila de deshacer. Esto incluye:

- AVL,
- BST,
- estaciones,
- zonas,
- histórico,
- eliminados,
- parámetros W, R, L, T,
- reloj,
- métricas,
- cola de reportes.

La copia profunda es importante porque los objetos se referencian entre sí; sin una copia profunda, el deshacer no sería fiable.

### `deshacer()`

Recupera el último estado guardado. Es una herramienta muy útil para revertir cambios incorrectos manteniendo un historial de operaciones.

### `_restaurarEstado(estado)`

Restaura todas las estructuras y campos del estado guardado.

## 7. indicadores y métricas del sistema

### `obtenerIndicadores()`

Devuelve un resumen del escenario con métricas acumuladas y datos estructurales. Entre otros valores incluye:

- `eventos_activos`,
- `eventos_historicos`,
- `altura_avl`,
- `hojas`,
- `inorden`, `preorden`, `postorden`,
- `anchura`,
- `eventos_por_prioridad`,
- `eventos_pendientes`,
- `eventos_costosos`.

Estos indicadores permiten evaluar el comportamiento del sistema y detectar si el árbol está creciendo de manera esperada.

### `_indicadorEventosPorPrioridad()`

Agrupa eventos por prioridad y devuelve la cantidad y los detalles de cada grupo.

### `_indicadorEventosPendientes()`

Devuelve todos los eventos todavía pendientes de revisión.

### `_indicadorEventosCostosos()`

Selecciona eventos de prioridad alta que estén a una profundidad mayor que `L`. Es una forma de identificar eventos costosos o críticos en el árbol.

## 8. Archivado y recuperación del árbol

### `obtenerRamaArchivable()` y `_obtenerRamaArchivable(subraiz)`

Analizan si un subárbol cumple condiciones para ser archivado. La lógica revisa si los nodos son de prioridad baja y si han pasado un tiempo suficiente.

### `archivarRama(subraiz)`

Mueve nodos elegibles al histórico, elimina los nodos del AVL y BST y acumula métricas de archivado.

### `recuperarArbol()`

Intenta reequilibrar y recuperar la forma del AVL. Si la estructura no queda válida, deshace el cambio y lanza error.

## 9. Relación entre lógica y estructura

La clave del proyecto es que la lógica del negocio no trabaja aislada: siempre actúa sobre una estructura real. Cada acción — crear, revisar, borrar, actualizar, consultar, archivar — se ejecuta contra el AVL y el BST, y por eso se pueden medir los costos, los errores y la evolución del árbol.

La diferencia entre “qué hace el sistema” y “cómo lo hace” queda muy clara en este módulo, porque aquí se toma la decisión final sobre el estado del evento y sobre la validez del árbol.
