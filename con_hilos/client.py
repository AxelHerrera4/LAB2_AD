import socket
import json

def mostrar_menu():
    """
    Muestra el menú interactivo en consola.
    """
    print("\n--- Menú de Calificaciones ---")
    print("1. Agregar calificación")
    print("2. Buscar por ID")
    print("3. Actualizar calificación")
    print("4. Listar todas")
    print("5. Eliminar por ID")
    print("6. Salir")
    return input("Elija opción: ")

def enviar_comando(comando):
    """
    Envía comandos al servidor y retorna respuestas parseadas de JSON.
    """
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12345))
        client_socket.send(comando.encode('utf-8'))
        respuesta = client_socket.recv(1024).decode('utf-8')
        client_socket.close()
        return json.loads(respuesta)
    except ConnectionRefusedError:
        return {"status": "error", "mensaje": "No se pudo conectar al servidor. Verifique que esté ejecutándose."}
    except Exception as e:
        return {"status": "error", "mensaje": f"Error de conexión: {str(e)}"}

# Bucle principal del cliente
print("=== Cliente de Sistema de Calificaciones ===")
print("Conectando al servidor concurrente en localhost:12345")

while True:
    opcion = mostrar_menu()
    
    if opcion == "1":
        print("\n--- Agregar Calificación ---")
        id_est = input("ID: ")
        nombre = input("Nombre: ")
        materia = input("Materia (NRC): ")
        calif = input("Calificación (0-20): ")
        res = enviar_comando(f"AGREGAR|{id_est}|{nombre}|{materia}|{calif}")
        print(f"\n✓ {res['mensaje']}" if res['status'] == 'ok' else f"\n✗ {res['mensaje']}")
        
    elif opcion == "2":
        print("\n--- Buscar por ID ---")
        id_est = input("ID: ")
        res = enviar_comando(f"BUSCAR|{id_est}")
        if res["status"] == "ok":
            print(f"\n📋 Información del Estudiante:")
            print(f"   ID: {res['data']['ID_Estudiante']}")
            print(f"   Nombre: {res['data']['Nombre']}")
            print(f"   Materia: {res['data']['Materia']}")
            print(f"   Calificación: {res['data']['Calificacion']}")
        else:
            print(f"\n✗ {res['mensaje']}")
            
    elif opcion == "3":
        print("\n--- Actualizar Calificación ---")
        id_est = input("ID: ")
        nueva_calif = input("Nueva calificación (0-20): ")
        res = enviar_comando(f"ACTUALIZAR|{id_est}|{nueva_calif}")
        print(f"\n✓ {res['mensaje']}" if res['status'] == 'ok' else f"\n✗ {res['mensaje']}")
        
    elif opcion == "4":
        print("\n--- Lista de Calificaciones ---")
        res = enviar_comando("LISTAR")
        if res["status"] == "ok":
            if len(res["data"]) == 0:
                print("No hay registros en el sistema.")
            else:
                print(f"\nTotal de registros: {len(res['data'])}\n")
                print(f"{'ID':<10} {'Nombre':<20} {'Materia':<10} {'Calificación':<12}")
                print("-" * 55)
                for row in res["data"]:
                    print(f"{row['ID_Estudiante']:<10} {row['Nombre']:<20} {row['Materia']:<10} {row['Calificacion']:<12}")
        else:
            print(f"\n✗ {res['mensaje']}")
            
    elif opcion == "5":
        print("\n--- Eliminar Registro ---")
        id_est = input("ID: ")
        confirmacion = input(f"¿Está seguro de eliminar el registro {id_est}? (s/n): ")
        if confirmacion.lower() == 's':
            res = enviar_comando(f"ELIMINAR|{id_est}")
            print(f"\n✓ {res['mensaje']}" if res['status'] == 'ok' else f"\n✗ {res['mensaje']}")
        else:
            print("\nOperación cancelada.")
        
    elif opcion == "6":
        print("\nCerrando cliente... ¡Hasta luego!")
        break
        
    else:
        print("\n✗ Opción inválida. Por favor, elija una opción del 1 al 6.")