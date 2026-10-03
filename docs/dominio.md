# Módulo de dominio

Este módulo representa los objetos del problema real del sistema de sismos. En este proyecto, el dominio no es un conjunto de entidades abstractas, sino clases con reglas concretas que validan y modelan cómo se comportan los terremotos, las estaciones y los reportes que los actualizan.

## 1. `Evento`

Archivo: `src/domain/Evento.py`

### Responsabilidad

`Evento` es la clase más importante del dominio. Representa un sismo que puede estar activo, revisado o archivado. Además de almacenar sus datos, decide si tiene prioridad alta, si puede relacionarse con otro evento y cómo se comporta durante una corrección.

### Atributos principales

- `id`: identificador único del evento.
- `magnitud`: intensidad del sismo. Se valida con un solo decimal y un rango permitido.
- `profundidad`: distancia desde la superficie hasta el foco del sismo.
- `zonax`, `zonay`: coordenadas del epicentro.
- `fechaHora`: fecha UTC con microsegundos en 0.
- `revision`: número de revisión del evento.
- `estaciones`: lista de estaciones relacionadas con el evento.
- `estado`: estado del evento, por ejemplo `Pendiente` o `Revisado`.

### Lógica de cada método importante

#### `__init__()`

Este constructor valida todos los datos de entrada antes de aceptar el evento. Si un valor está fuera de rango, si la fecha no usa UTC o si la lista de estaciones no es válida, lanza `ValueError`.

Esto sirve para garantizar que el árbol no almacene información corrupta ni contradictoria.

#### `_validar_undecimal(decimal)`

Este método asegura que los valores decimales estén normalizados con un solo decimal. Por ejemplo, si se intenta registrar `5.00`, la función lo deja como una representación correcta del dominio del proyecto.

La validación existe porque el sistema trabaja con números definidos y no quiere aceptar decimales arbitrarios.

#### `calcularPrioridad(poblada)`

La prioridad se calcula en base a tres factores:

- magnitud alta,
- profundidad pequeña,
- pertenencia a una zona poblada.

La lógica del código es:

```python
if self.magnitud >= 6.0 or (self.magnitud >= 4.5 and self.profundidad <= 30.0 and poblada):
	return 3
elif self.magnitud >= 4.5:
	return 2
else:
	return 1
```

Esto significa que un sismo muy fuerte o uno moderado pero localizado en una zona con población y poca profundidad puede escalar a prioridad máxima.

#### `esCandidato(eventoB, w, r)`

Este método decide si un evento puede ser un candidato para asociarse con otro evento `eventoB`.

La regla es:

- el evento actual debe tener mayor magnitud que `eventoB`,
- la diferencia horaria entre ambos debe estar en el rango permitido `w`,
- la distancia geográfica entre los epicentros debe ser menor o igual a `r`.

La lógica se basa en la intuición de que un sismo más fuerte y más cercano en tiempo y espacio puede ser la causa o el referente más probable para el evento de interés.

#### `marcarRevisado()`

Cambia el estado del evento a `Revisado`. Aunque es un método pequeño, representa una decisión funcional importante: después de la revisión, el evento ya no está simplemente pendiente, sino que pasó por una validación.

## 2. `Zona`

Archivo: `src/domain/Zona.py`

### Responsabilidad

`Zona` modela un rectángulo geográfico dentro del escenario. Su objetivo es saber si un punto cae dentro de una región y si esa región es poblada o no.

### Funcionalidad principal

- `contiene(x, y)`: revisa si una coordenada está dentro de los límites de la zona.
- `es_poblada()`: devuelve si la zona está marcada como habitada.
- `obtener_datos()`: entrega un resumen del registro de la zona.

### Por qué es importante

La zona afecta la prioridad del evento. Si el epicentro cae en una zona poblada y la magnitud es moderada, la prioridad puede subir. Eso hace que la geografía real influya en la organización del árbol.

## 3. `Estacion`

Archivo: `src/domain/Estacion.py`

### Responsabilidad

Representa una estación de observación o un punto de registro. No tiene lógica compleja, pero es crucial en la validación y trazabilidad del sistema.

### Atributos

- `id_estacion`: identificador único de la estación.
- `nombre`: nombre descriptivo de la estación.

Se usa para asegurar que los reportes provienen de estaciones conocidas y para mantener una trazabilidad del origen de la información.

## 4. `Reporte`

Archivo: `src/domain/Reporte.py`

### Responsabilidad

`Reporte` encapsula la información que llega desde una estación para actualizar o corregir un evento existente.

### Atributos principales

- `id_evento`: evento al que se refiere el reporte.
- `nRevision`: número de revisión del reporte.
- `magnitud`, `profundidad`, `zonax`, `zonay`: datos actualizados del sismo.
- `fecha`: fecha en que se reportó la información.
- `estacion`: estación emisora del reporte.

### Uso en el sistema

Un reporte puede:

- actualizar un evento activo,
- confirmar un dato existente,
- rechazar información antigua o inconsistente,
- reactivar un evento archivado,
- producir conflicto si llega una revisión contradictoria.

La clase en sí es un contenedor, pero su valor real aparece cuando `Escenario` la procesa y decide cuál es la acción correcta.

## 5. Interacción entre entidades

El flujo natural del dominio es:

1. se define una zona y una estación,
2. se crea un `Evento` con validación,
3. el evento se ordena dentro del árbol según su clave,
4. llega un `Reporte` desde una estación,
5. el escenario compara el reporte con el evento actual,
6. el evento puede cambiar de estado, de ubicación, de prioridad o incluso reactivarse.

Esto hace que el dominio no sea estático: cada evento es un objeto vivo que muta según los reportes y las reglas del negocio.
