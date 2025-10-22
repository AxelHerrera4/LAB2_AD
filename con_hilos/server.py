import socket
import csv
import json
import os
import threading

ARCHIVO_CSV = '../calificaciones.csv'

def inicializar_csv():
    """
    Verifica si el archivo CSV existe y, si no, lo crea con los headers iniciales.
    """
    if not os.path.exists(ARCHIVO_CSV):
        with open(ARCHIVO_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID_Estudiante', 'Nombre', 'Materia', 'Calificacion'])

def consultar_nrc(nrc):
    """
    Consulta el servidor de NRCs para validar si una materia/NRC es válida.
    Retorna el resultado de la validación.
    """
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12346))
        client_socket.send(f"BUSCAR_NRC|{nrc}".encode('utf-8'))
        respuesta = client_socket.recv(1024).decode('utf-8')
        client_socket.close()
        return json.loads(respuesta)
    except ConnectionRefusedError:
        return {"status": "error", "mensaje": "Servidor de NRCs no disponible"}
    except Exception as e:
        return {"status": "error", "mensaje": f"Error consultando NRC: {str(e)}"}

def agregar_calificacion(id_est, nombre, materia, calif):
    """
    Agrega una nueva fila al CSV con validación de NRC.
    """
    # Validar NRC primero
    res_nrc = consultar_nrc(materia)
    if res_nrc["status"] != "ok":
        return {"status": "error", "mensaje": f"Materia/NRC no válida: {res_nrc.get('mensaje', 'NRC no existe')}"}
    
    try:
        with open(ARCHIVO_CSV, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([id_est, nombre, materia, calif])
        return {"status": "ok", "mensaje": f"Calificación agregada para {nombre}"}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}

def buscar_por_id(id_est):
    """
    Busca una fila por ID Estudiante y retorna los detalles si existe.
    """
    try:
        with open(ARCHIVO_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['ID_Estudiante'] == id_est:
                    return {"status": "ok", "data": row}
        return {"status": "not_found", "mensaje": "ID no encontrado"}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}

def actualizar_calificacion(id_est, nueva_calif):
    """
    Lee todo el CSV, actualiza la calificación si encuentra el ID, y reescribe el archivo.
    """
    try:
        filas = []
        encontrado = False
        with open(ARCHIVO_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['ID_Estudiante'] == id_est:
                    row['Calificacion'] = nueva_calif
                    encontrado = True
                filas.append(row)
        
        if encontrado:
            with open(ARCHIVO_CSV, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['ID_Estudiante', 'Nombre', 'Materia', 'Calificacion'])
                writer.writeheader()
                writer.writerows(filas)
            return {"status": "ok", "mensaje": "Calificación actualizada"}
        else:
            return {"status": "not_found", "mensaje": "ID no encontrado"}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}

def listar_todas():
    """
    Lee y retorna todas las filas como lista de dicts.
    """
    try:
        with open(ARCHIVO_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        return {"status": "ok", "data": data}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}

def eliminar_por_id(id_est):
    """
    Lee el CSV, filtra filas sin el ID, y reescribe.
    """
    try:
        filas = []
        encontrado = False
        with open(ARCHIVO_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['ID_Estudiante'] != id_est:
                    filas.append(row)
                else:
                    encontrado = True
        
        if encontrado:
            with open(ARCHIVO_CSV, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['ID_Estudiante', 'Nombre', 'Materia', 'Calificacion'])
                writer.writeheader()
                writer.writerows(filas)
            return {"status": "ok", "mensaje": "Registro eliminado"}
        else:
            return {"status": "not_found", "mensaje": "ID no encontrado"}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}

def procesar_comando(comando):
    """
    Parsea el comando del cliente y delega a la función modular correspondiente.
    """
    partes = comando.strip().split('|')
    op = partes[0]
    
    if op == "AGREGAR" and len(partes) == 5:
        return agregar_calificacion(partes[1], partes[2], partes[3], partes[4])
    elif op == "BUSCAR" and len(partes) == 2:
        return buscar_por_id(partes[1])
    elif op == "ACTUALIZAR" and len(partes) == 3:
        return actualizar_calificacion(partes[1], partes[2])
    elif op == "LISTAR":
        return listar_todas()
    elif op == "ELIMINAR" and len(partes) == 2:
        return eliminar_por_id(partes[1])
    else:
        return {"status": "error", "mensaje": "Comando inválido"}

def manejar_cliente(client_socket, addr):
    """
    Maneja la conexión de un cliente en un hilo separado.
    """
    print(f"Cliente conectado desde {addr} en hilo {threading.current_thread().name}")
    try:
        data = client_socket.recv(1024).decode('utf-8')
        if data:
            respuesta = procesar_comando(data)
            client_socket.send(json.dumps(respuesta).encode('utf-8'))
    except Exception as e:
        print(f"Error en hilo: {e}")
    finally:
        client_socket.close()
        print(f"Cliente {addr} desconectado.")

# Configuración del servidor concurrente
inicializar_csv()
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)  # Cola para múltiples
print("Servidor concurrente escuchando en puerto 12345...")

try:
    while True:
        client_socket, addr = server_socket.accept()
        hilo = threading.Thread(target=manejar_cliente, args=(client_socket, addr))
        hilo.start()
except KeyboardInterrupt:
    print("\nServidor detenido.")
finally:
    server_socket.close()