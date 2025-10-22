import socket
import csv
import json
import os
ARCHIVO_CSV = 'calificaciones.csv'

def inicializar_csv():
    if not os.path.exists(ARCHIVO_CSV):
        with open(ARCHIVO_CSV, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['ID_Estudiante', 'Nombre', 'Materia', 'Calificacion'])

def agregar_calificacion(id_est, nombre, materia, calif):
    try:
        with open(ARCHIVO_CSV, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([id_est, nombre, materia, calif])
        return {"status": "ok", "mensaje": f"Calificación agregada para {nombre}"}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}
    
def buscar_por_id(id_est):
    try:
        with open(ARCHIVO_CSV, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['ID_Estudiante'] == id_est:
                    return {"status": "ok", "data": row}
        return {"status": "not_found", "mensaje": "ID no encontrado"}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}
    
def actualizar_calificacion(id_est, nueva_calif):
    try:
        filas = []
        encontrado = False
        with open(ARCHIVO_CSV, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['ID_Estudiante'] == id_est:
                    row['Calificacion'] = nueva_calif
                    encontrado = True
                filas.append(row)
        
        if not encontrado:
            return {"status": "not_found", "mensaje": "ID no encontrado"}
        
        with open(ARCHIVO_CSV, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['ID_Estudiante', 'Nombre', 'Materia', 'Calificacion'])
            writer.writeheader()
            writer.writerows(filas)
        
        return {"status": "ok", "mensaje": f"Calificación actualizada para ID {id_est}"}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}
    
def listar_todas():
    try:
        with open(ARCHIVO_CSV, 'r') as f:
            reader = csv.DictReader(f)
            datos = list(reader)
        return {"status": "ok", "data": datos}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}
    
def eliminar_por_id(id_est):
    try:
        filas = []
        encontrado = False
        with open(ARCHIVO_CSV, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['ID_Estudiante'] == id_est:
                    encontrado = True
                    continue
                filas.append(row)
        
        if not encontrado:
            return {"status": "not_found", "mensaje": "ID no encontrado"}
        
        with open(ARCHIVO_CSV, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['ID_Estudiante', 'Nombre', 'Materia', 'Calificacion'])
            writer.writeheader()
            writer.writerows(filas)
        
        return {"status": "ok", "mensaje": f"Calificación eliminada para ID {id_est}"}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}
    
def procesar_comando(comando):
    partes = comando.strip().split(',')
    accion = partes[0].upper()
    
    if accion == 'AGREGAR' and len(partes) == 5:
        return agregar_calificacion(partes[1], partes[2], partes[3], partes[4])
    elif accion == 'BUSCAR' and len(partes) == 2:
        return buscar_por_id(partes[1])
    elif accion == 'ACTUALIZAR' and len(partes) == 3:
        return actualizar_calificacion(partes[1], partes[2])
    elif accion == 'LISTAR':
        return listar_todas()
    elif accion == 'ELIMINAR' and len(partes) == 2:
        return eliminar_por_id(partes[1])
    else:
        return {"status": "error", "mensaje": "Comando inválido o parámetros incorrectos"}
    
inicializar_csv()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(1)
print("Servidor escuchando en el puerto 12345...")

try:
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Cliente conectado desde {addr}")
        data = client_socket.recv(1024).decode('utf-8')
        if data:
            respuesta = procesar_comando(data)
            client_socket.send(json.dumps(respuesta).encode('utf-8'))
        client_socket.close()
        print("Cliente desconectado.")
except KeyboardInterrupt:
    print("Servidor detenido.")
finally:
    server_socket.close()