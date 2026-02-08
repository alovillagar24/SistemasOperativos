# ===== CLIENTE (usa middleware y envía password) =====

import socket
import middleware  # Asegúrate de que el archivo middleware.py esté en la misma carpeta

# Obtenemos los datos del servidor elegido
HOST, PORT, PASSWORD = middleware.seleccionar()

def enviar_y_recibir(op, extra=""):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((HOST, PORT))
            
            # 1. Enviamos contraseña con salto de línea
            s.sendall(f"{PASSWORD}\n".encode())
            
            # --- MANEJO DE AUTENTICACIÓN ---
            # Esperamos la respuesta del servidor antes de mandar la operación
            confirmacion = s.recv(1024).decode().strip()
            
            # Verificamos si la respuesta contiene "OK" (así aceptamos "OK" u "OK: Autenticado")
            if "OK" not in confirmacion.upper():
                print(f"\n[SERVIDOR]: Acceso Denegado -> {confirmacion}")
                return

            # 2. Si el password fue aceptado, enviamos la operación
            s.sendall(f"{op}\n".encode())
            
            # 3. Enviamos datos extra (el nombre del comando o el PID)
            if extra:
                # Pequeña pausa para asegurar que el servidor esté listo para el segundo dato
                s.sendall(f"{extra}\n".encode())
            
            # 4. Leer la respuesta del servidor (Lista de procesos o estados)
            print("\n" + "="*40)
            print(f"Respuesta desde {HOST}:")
            print("-" * 40)
            
            # Leemos en bucle para recibir datos largos (como la lista de procesos)
            while True:
                respuesta = s.recv(4096).decode(errors='ignore')
                if not respuesta:
                    break
                print(respuesta, end="") 
            print("\n" + "="*40)

    except ConnectionRefusedError:
        print(f"\n[!] Error: No se pudo conectar al servidor en {HOST}:{PORT}")
    except socket.timeout:
        print("\n[!] Error: El servidor no respondió a tiempo.")
    except Exception as e:
        print(f"\n[!] Error inesperado: {e}")

# --- MENÚ INTERACTIVO ---
while True:
    print("\n--- PANEL DE CONTROL REMOTO ---")
    print(f"Conectado a: {HOST}")
    print("1) Listar Procesos")
    print("2) Iniciar Aplicación")
    print("3) Detener (Kill) PID")
    print("0) Salir")
    
    op = input("Opción: ").strip()

    if op == "1":
        enviar_y_recibir("1")

    elif op == "2":
        cmd = input("Comando a iniciar (ej. gedit, sleep 100): ").strip()
        if cmd:
            enviar_y_recibir("2", cmd)

    elif op == "3":
        pid = input("PID a detener: ").strip()
        if pid.isdigit():
            enviar_y_recibir("3", pid)
        else:
            print("Entrada inválida. El PID debe ser un número.")

    elif op == "0":
        print("Cerrando cliente...")
        break
