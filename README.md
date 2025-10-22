# SistemaDistribuido-Calificaciones

![Portada](ruta/de/tu/imagen.png)

SistemaDistribuido-Calificaciones es una aplicación distribuida en Python para el registro de calificaciones finales de estudiantes. Utiliza **sockets TCP**, archivos **CSV** para persistencia de datos y soporta concurrencia mediante **hilos**. Incluye un servidor adicional de NRC para validar materias antes de registrar calificaciones.

## Características principales

* Servidor de calificaciones con funciones **CRUD**: agregar, buscar, actualizar, listar y eliminar calificaciones.
* Cliente de consola interactivo que envía comandos y recibe respuestas en **JSON**.
* Servidor concurrente capaz de atender múltiples clientes simultáneamente.
* Servidor de NRC independiente para validar materias/NRC antes de registrar o actualizar calificaciones.
* Persistencia de datos en archivos `calificaciones.csv` y `nrcs.csv`.
* Manejo de errores y validación de entradas, incluyendo fallos de conexión al servidor de NRC.

## Estructura del proyecto

```
laboratorio_2/
│
├── README.md
├── calificaciones.csv
├── nrcs.csv
├── sin_hilos/
│   ├── server.py
│   └── client.py
├── con_hilos/
│   ├── server.py
│   └── client.py
└── nrcs_server.py
```

## Requisitos

* Python 3.8 o superior
* Sistema operativo compatible con sockets TCP
* Editor de texto o IDE (VS Code, PyCharm, etc.)

## Despliegue

### 1. Clonar el repositorio

```bash
git clone https://github.com/AxelHerrera4/LAB2_AD
cd SistemaDistribuido-Calificaciones
```

## Pasos de ejecución

### 1. Iniciar el servidor

Ejecuta el servidor (secuencial o concurrente) según tu necesidad.
![Iniciar Servidor](ruta/de/imagen_servidor.png)

```bash
# Servidor secuencial
cd sin_hilos
python server.py

# Servidor concurrente
cd ../con_hilos
python server.py
```

### 2. Conexión de los clientes

Cada cliente se ejecuta en una terminal independiente y se conecta al servidor.
![Conexión de Clientes](ruta/de/imagen_clientes.png)

```bash
python client.py
```

### 3. Ejecutar el servidor de NRC

El servidor de NRC valida los NRC antes de registrar o actualizar calificaciones.
![Servidor NRC](ruta/de/imagen_nrc.png)

```bash
python nrcs_server.py
```

## Ejemplo de uso

![Ejemplo](ruta/de/otra/imagen.png)
