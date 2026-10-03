# Estructuras de datos

Este módulo explica cómo el proyecto guarda los eventos y cómo los organiza para poder buscar, comparar y recuperar información de forma eficiente.

## 1. `Key`

Archivo: `src/structures/Nodo.py`

### Responsabilidad

`Key` es la clave de orden del árbol. No guarda solo un valor, sino una tupla de comparación compuesta por:

- prioridad,
- magnitud,
- identificador del evento.

### Por qué es importante

La clave determina la posición de un nodo dentro del árbol. En otras palabras, la lógica de ordenamiento de los eventos depende de esta estructura.

### Lógica de comparación

La comparación está definida por:

```python
(self.prioridad, self.magnitud, self.id_key)
```

Eso hace que primero se ordenen por prioridad, luego por magnitud y finalmente por id. Cuando dos eventos tienen la misma prioridad y magnitud, el id decide el orden. Esto permite que el árbol sea determinista y consistente.

## 2. `Nodo`

Archivo: `src/structures/Nodo.py`

### Responsabilidad

Cada nodo del árbol representa un evento dentro de la estructura. Tiene la clave que define su posición y el `evento` asociado.

### Atributos principales

- `key`: clave de comparación del evento.
- `evento`: objeto `Evento` almacenado.
- `izq`: hijo izquierdo.
- `der`: hijo derecho.
- `altura`: altura del nodo, útil para equilibrar el AVL.

### Método clave

#### `esHoja()`

Retorna `True` si el nodo no tiene hijos. Este método es útil para detectar hojas, validar estructuras vacías o decidir cómo eliminar nodos.

## 3. `AVL`

Archivo: `src/structures/Avl.py`

### Responsabilidad

`Avl` es la estructura principal del sistema. Su objetivo es mantener el árbol balanceado para evitar que la profundidad crezca demasiado y haga más costosa la búsqueda y la inserción.

### Cómo funciona

Cuando se inserta un nuevo nodo, el árbol recalcula la altura de cada nodo y el factor de balance. Si el balance está fuera del rango permitido, se aplican rotaciones:

- `LL`: rotación derecha,
- `RR`: rotación izquierda,
- `LR`: rotación izquierda + rotación derecha,
- `RL`: rotación derecha + rotación izquierda.

Estas rotaciones son la base del balance del AVL. Evitan que el árbol se convierta en una lista enlazada, lo que sería un problema para la eficiencia.

### Métodos importantes

#### `insertar(key, evento, modo_estres)`

Inserta un evento en el árbol y reequilibra la estructura si es necesario.

#### `_insertar(...)`

Recorrido recursivo para ubicar el punto correcto de inserción. Cuando se encuentra un hueco, se crea el nodo.

#### `_actualizarAltura(nodo)`

Recalcula la altura del nodo a partir de la altura de sus hijos.

#### `_factor_balance(nodo)`

Calcula la diferencia entre altura del subárbol izquierdo y derecho. Si el valor es muy alto o muy bajo, indica desbalance.

#### `_rotacion_derecha(nodo)` y `_rotacion_izquierda(nodo)`

Reorganizan la estructura para restaurar el equilibrio sin perder los nodos.

#### `verificarEstructura(modo_estres=False)`

Recorre el árbol y valida:

- si la clave es válida,
- si el evento asociado existe,
- si no hay nodos repetidos ni ciclos,
- si la altura calculada coincide con la altura almacenada,
- si el factor de balance está dentro de los límites.

Este método entrega un diccionario con el estado del árbol y errores o advertencias encontradas.

#### `encontrarNodo(id)`

Busca un evento por su identificador usando recorrido por niveles. Es útil para consultar eventos activos y distinguirlos del historial.

#### `eliminar(key, modo_estres)`

Elimina un nodo y rebalancea el árbol. La lógica usa casos típicos de eliminación en BST con ajuste de alturas y rotaciones.

### Métricas del AVL

El árbol lleva contadores como:

- `casos_LL`, `casos_RR`, `casos_LR`, `casos_RL`
- `giros_izquierda`, `giros_derecha`

Estas métricas permiten estudiar el costo real de la estructura y comparar el comportamiento del árbol bajo distintos tipos de inserciones.

## 4. `BST`

Archivo: `src/structures/Bst.py`

### Responsabilidad

El BST es un árbol binario de búsqueda no balanceado. Se usa como segunda estructura para comparar resultados, estudiar cómo cambia el orden y detectar desincronizaciones con el AVL.

### Funciones principales

- `insertar()`: agrega un nuevo nodo según la clave.
- `buscar()`: encuentra un nodo comparando la clave.
- `eliminar()`: elimina un nodo y reacomoda los subárboles.
- `preorden()`, `inorden()`, `posorden()`: devoluciones del recorrido del árbol.
- `altura()`: calcula la profundidad máxima.
- `cantidad_nodos()`: cuenta la cantidad total de nodos.
- `profundidad()`: devuelve la profundidad de un dato buscado.

### Diferencia con el AVL

El BST no reequilibra automáticamente. Por eso, cuando el orden de inserción es desfavorable, puede crecer mucho y hacerse más profundo. El AVL corrige esa situación. La comparación entre ambos es útil para demostrar por qué el AVL es mejor para este caso de uso.

## 5. Relación entre `Key`, `Nodo`, `AVL` y `BST`

El flujo general es:

1. se crea una `Key` para cada evento,
2. el `Nodo` guarda el evento y la clave,
3. el `AVL` inserta el nodo y lo reequilibra,
4. el `BST` recibe la misma información para comparar comportamiento.

El árbol es la base de almacenamiento del escenario, pero lo más importante es que la clave ordena los eventos por relevancia y la estructura decide cómo se recorren y consulten esos datos.
