import socket
import csv
import json
import os

ARCHIVO_NRC = 'nrcs.csv'

def inicializar_nrc_csv():
    """
    Verifica si el archivo nrcs.csv existe y, si no, lo crea con headers y datos de ejemplo.
    """
    if not os.path.exists(ARCHIVO_NRC):
        with open(ARCHIVO_NRC, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['NRC', 'Materia'])
            # Agregar algunos NRCs de ejemplo
            writer.writerow(['MAT101', 'Matemáticas I'])
            writer.writerow(['FIS101', 'Física I'])
            writer.writerow(['PRO101', 'Programación I'])
            writer.writerow(['CAL101', 'Cálculo I'])
            writer.writerow(['ALG101', 'Álgebra Lineal'])
        print("Archivo nrcs.csv creado con datos de ejemplo")

def listar_nrcs():
    """
    Lee y retorna todos los NRCs disponibles.
    """
    try:
        with open(ARCHIVO_NRC, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        return {"status": "ok", "data": data}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}

def buscar_nrc(nrc):
    """
    Busca un NRC específico en el archivo.
    Retorna status ok si existe, not_found si no.
    """
    try:
        with open(ARCHIVO_NRC, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['NRC'] == nrc:
                    return {"status": "ok", "data": row}
        return {"status": "not_found", "mensaje": f"NRC {nrc} no existe"}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}

def procesar_comando_nrc(comando):
    """
    Parsea el comando del cliente y delega a la función correspondiente.
    """
    partes = comando.strip().split('|')
    op = partes[0]
    
    if op == "LISTAR_NRC":
        return listar_nrcs()
    elif op == "BUSCAR_NRC" and len(partes) == 2:
        return buscar_nrc(partes[1])
    else:
        return {"status": "error", "mensaje": "Comando inválido"}

# Configuración del servidor de NRCs
inicializar_nrc_csv()
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12346))
server_socket.listen(5)
print("Servidor de NRCs escuchando en puerto 12346...")
print("NRCs disponibles:")
nrcs = listar_nrcs()
if nrcs["status"] == "ok":
    for nrc in nrcs["data"]:
        print(f"  - {nrc['NRC']}: {nrc['Materia']}")

try:
    while True:
        client_socket, addr = server_socket.accept()
        data = client_socket.recv(1024).decode('utf-8')
        if data:
            respuesta = procesar_comando_nrc(data)
            client_socket.send(json.dumps(respuesta).encode('utf-8'))
        client_socket.close()
except KeyboardInterrupt:
    print("\nServidor de NRCs detenido.")
finally:
    server_socket.close()