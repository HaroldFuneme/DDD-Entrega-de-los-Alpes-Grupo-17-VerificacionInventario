# DDD-Entrega-de-los-Alpes-Grupo-17-VerificacionInventario
Microservicio de verificación de inventario: Este microservicio se encargaría de verificar el inventario de cada producto en la orden de compra, buscando en las bodegas y centros de distribución.

## Estructura del proyecto

El repositorio en su raíz está estructurado de la siguiente forma::

- **src:** En este directorio encuentra el código fuente del microservicio. En la siguiente sección se explica un poco mejor la estructura del mismo ([link](https://blog.ionelmc.ro/2014/05/25/python-packaging/#the-structure%3E) para más información)
- **gitpod.yml:** Archivo que define las tareas/pasos a ejecutar para configurar su workspace en Gitpod
- **README.md:** El archivo que está leyendo :)
- **requirements.txt:** Archivo con los requerimientos para el correcto funcionamiento del proyecto (librerias Python)

## EDA
### Ejecutar Base de datos
Desde el directorio principal ejecute el siguiente comando.

```bash
docker-compose --profile db up
```

Este comando descarga las imágenes e instala las dependencias de la base datos.

### Ejecutar Aplicación

Desde el directorio principal ejecute el siguiente comando.

```bash
flask --app src/verifica_inventario/api run
```

Siempre puede ejecutarlo en modo DEBUG:

```bash
flask --app src/verifica_inventario/api --debug run
```

### Ejecutar pruebas

```bash
coverage run -m pytest
```

### Ver reporte de covertura
```bash
coverage report
```

### Crear imagen Docker

Desde el directorio principal ejecute el siguiente comando.

```bash
docker build . -f verifica-inventario.Dockerfile -t eda/verifica-inventario
```

### Ejecutar contenedora (sin compose)

Desde el directorio principal ejecute el siguiente comando.

```bash
docker run -p 5000:5000 eda/verifica-inventario
```

### Consultar tópicos
Abrir en una terminal:

```bash
docker exec -it broker bash
```

Ya dentro de la contenedora ejecute:

```bash
./bin/pulsar-admin topics list public/default
```

### Cambiar retención de tópicos
Abrir en una terminal:

```bash
docker exec -it broker bash
```
Ya dentro de la contenedora ejecute:

```bash
./bin/pulsar-admin namespaces set-retention public/default --size -1 --time -1
```

Para poder ver que los cambios fueron efectivos ejecute el siguiente comando:

```bash
./bin/pulsar-admin namespaces get-retention public/default
```

**Nota**: Esto nos dejará con una retención infinita. Sin embargo, usted puede cambiar la propiedad de `size` para poder usar [Tiered Storage](https://pulsar.apache.org/docs/2.11.x/concepts-tiered-storage/)

## Docker-compose

Para desplegar toda la arquitectura en un solo comando, usamos `docker-compose`. Para ello, desde el directorio principal, ejecute el siguiente comando:

```bash
docker-compose up
```

Si desea detener el ambiente ejecute:

```bash
docker-compose stop
```

En caso de querer desplegar dicha topología en el background puede usar el parametro `-d`.

```bash
docker-compose up -d
```

### Correr docker-compose usando profiles
```bash
docker-compose --profile <pulsar|db> up
```