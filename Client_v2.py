# ===== CLIENTE (usa middleware y envía password) =====

import socket
import middleware  # Asegúrate de que middleware.seleccionar() devuelva HOST, PORT, PASSWORD

HOST, PORT, PASSWORD = middleware.seleccionar()

def enviar_y_recibir(op, extra=""):
    try:
        # Creamos el socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5) # No esperar eternamente si el servidor falla
            s.connect((HOST, PORT))
            
            # 1. Enviamos contraseña (con salto de línea para tu servidor actual)
            s.sendall(f"{PASSWORD}\n".encode())
            
            # 2. Enviamos la operación
            s.sendall(f"{op}\n".encode())
            
            # 3. Enviamos datos extra si existen
            if extra:
                s.sendall(f"{extra}\n".encode())
            
            # 4. LEER LA RESPUESTA (La mejora clave)
            print("\n" + "="*30)
            print("[SERVIDOR]:")
            # Leemos en un bucle por si la lista de procesos es larga
            while True:
                respuesta = s.recv(4096).decode(errors='ignore')
                if not respuesta:
                    break
                print(respuesta)
            print("="*30)

    except ConnectionRefusedError:
        print("\n[!] Error: El servidor no está encendido o la IP/Puerto son incorrectos.")
    except socket.timeout:
        print("\n[!] Error: El servidor tardó demasiado en responder.")
    except Exception as e:
        print(f"\n[!] Ocurrió un error inesperado: {e}")

while True:
    print("\n--- PANEL DE CONTROL REMOTO ---")
    print("1) Listar Procesos")
    print("2) Iniciar Aplicación")
    print("3) Detener (Kill) PID")
    print("0) Salir")
    
    op = input("Opción: ").strip()

    if op == "1":
        enviar_y_recibir("1")

    elif op == "2":
        cmd = input("Comando a iniciar (ej. gedit): ").strip()
        if cmd:
            enviar_y_recibir("2", cmd)

    elif op == "3":
        pid = input("PID a detener: ").strip()
        if pid.isdigit():
            enviar_y_recibir("3", pid)
        else:
            print("Por favor, introduce un número de PID válido.")

    elif op == "0":
        print("Saliendo...")
        break