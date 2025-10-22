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
        respuesta = client_socket.recv(4096).decode('utf-8')
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
        # Mostrar respuesta en JSON
        print(json.dumps(res, indent=4, ensure_ascii=False))
        
    elif opcion == "2":
        print("\n--- Buscar por ID ---")
        id_est = input("ID: ")
        res = enviar_comando(f"BUSCAR|{id_est}")
        print(json.dumps(res, indent=4, ensure_ascii=False))
            
    elif opcion == "3":
        print("\n--- Actualizar Calificación ---")
        id_est = input("ID: ")
        nueva_calif = input("Nueva calificación (0-20): ")
        res = enviar_comando(f"ACTUALIZAR|{id_est}|{nueva_calif}")
        print(json.dumps(res, indent=4, ensure_ascii=False))
        
    elif opcion == "4":
        print("\n--- Lista de Calificaciones ---")
        res = enviar_comando("LISTAR")
        print(json.dumps(res, indent=4, ensure_ascii=False))
            
    elif opcion == "5":
        print("\n--- Eliminar Registro ---")
        id_est = input("ID: ")
        confirmacion = input(f"¿Está seguro de eliminar el registro {id_est}? (s/n): ")
        if confirmacion.lower() == 's':
            res = enviar_comando(f"ELIMINAR|{id_est}")
            print(json.dumps(res, indent=4, ensure_ascii=False))
        else:
            print("\nOperación cancelada.")
        
    elif opcion == "6":
        print("\nCerrando cliente... ¡Hasta luego!")
        break
        
    else:
        print("\n✗ Opción inválida. Por favor, elija una opción del 1 al 6.")
