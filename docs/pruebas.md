# Pruebas del proyecto

Las pruebas del proyecto validan tanto la estructura de datos como la lógica de negocio y las consultas de desempeño.

## 1. Organización de pruebas

El proyecto tiene pruebas en la carpeta `tests/`, con varios grupos:

- pruebas del AVL
- pruebas del BST
- pruebas del dominio `Evento`
- pruebas de reportes y zonas
- pruebas del escenario y sus métricas

## 2. Tipo de validaciones

### 2.1 Validación funcional

Comprueba que:

- los eventos se crean correctamente,
- no se aceptan ids duplicados,
- las prioridades se calculan bien,
- los reportes alteran el estado correcto del evento,
- las asociaciones son coherentes,
- el histórico y el activo se mantienen sincronizados.

### 2.2 Validación estructural

Las pruebas revisan:

- altura del árbol,
- hojas,
- rotaciones,
- balance del AVL,
- sincronización con el BST,
- orden de inserción y búsquedas.

### 2.3 Validación de desempeño

Se verifican casos como:

- primeros `k` pendientes,
- rangos por magnitud,
- rangos por profundidad y fechas,
- eventos de prioridad alta y costosos,
- nodos examinados por consulta,
- comparación AVL vs BST bajo distintos órdenes de inserción.

## 3. Ejemplo de flujo de prueba

Un caso típico consiste en:

1. crear un escenario,
2. insertar eventos,
3. consultar propiedades del árbol,
4. comprobar que una operación devuelve el resultado esperado,
5. verificar métricas como altura, nodos accesados o rotaciones.

## 4. Importancia de las pruebas

Las pruebas no solo validan que el código funciona, sino que garantizan que las decisiones de diseño no se rompan en cambios posteriores. Esto es especialmente importante en una solución donde la estructura de datos y la lógica de negocio están fuertemente acopladas.
