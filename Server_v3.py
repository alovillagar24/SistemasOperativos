# ===== SERVIDOR AWS (Password + Whitelist + Corrección de Red) =====
import socket
import subprocess

# Configuración de Seguridad
PASSWORD = "clave159"
# Nota: gedit o calc no funcionarán en AWS (no hay interfaz gráfica), 
# pero los dejamos por compatibilidad con tu ejercicio.
WHITELIST = ["sleep", "python", "ls", "top", "ps", "df"]

def handle_client(conn):
    try:
        # 1. Validar Password
        data = conn.recv(1024).decode().strip()
        if not data or data != PASSWORD:
            print(f"Intento de acceso fallido: {data}")
            conn.sendall(b"ERROR: Password incorrecta\n")
            return
        
        conn.sendall(b"OK\n") 

        # 2. Recibir Operación (1=Listar, 2=Iniciar, 3=Detener)
        op = conn.recv(1024).decode().strip()
        print(f"Operación solicitada: {op}")
        
        if op == "1": # LISTAR PROCESOS
            # Usamos ps para listar los últimos 15 procesos
            resultado = subprocess.check_output("ps -eo pid,comm --sort=-pid | head -n 15", shell=True)
            conn.sendall(resultado)

        elif op == "2": # INICIAR PROCESO
            conn.sendall(b"READY_FOR_CMD\n") # Avisar que esperamos el comando
            cmd = conn.recv(1024).decode().strip()
            
            # Verificamos si el comando base está permitido
            base_cmd = cmd.split()[0]
            if base_cmd in WHITELIST:
                # Ejecutar en segundo plano sin bloquear el servidor
                subprocess.Popen(cmd.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                conn.sendall(f"SUCCESS: Iniciado {cmd}\n".encode())
                print(f"Ejecutado: {cmd}")
            else:
                conn.sendall(b"ERROR: Comando no permitido en Whitelist\n")

        elif op == "3": # DETENER PROCESO
            conn.sendall(b"READY_FOR_PID\n")
            pid = conn.recv(1024).decode().strip()
            if pid.isdigit():
                # Intentar matar el proceso
                subprocess.run(["kill", "-9", pid])
                conn.sendall(f"SUCCESS: PID {pid} detenido\n".encode())
                print(f"Proceso {pid} terminado.")
            else:
                conn.sendall(b"ERROR: PID invalido\n")

    except Exception as e:
        print(f"Error procesando cliente: {e}")
        try:
            conn.sendall(f"ERROR: {str(e)}\n".encode())
        except:
            pass
    finally:
        conn.close()

# --- Configuración del Servidor en AWS ---
HOST = "0.0.0.0" # IMPORTANTE: Escucha en todas las interfaces de AWS
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"--- SERVIDOR DE PROCESOS ACTIVO ---")
    print(f"Escuchando en puerto: {PORT}")
    print(f"Esperando conexiones desde el Middleware...")
except Exception as e:
    print(f"No se pudo iniciar el servidor: {e}")

while True:
    conn, addr = server.accept()
    print(f"\n[+] Nueva conexión desde: {addr}")
    handle_client(conn)
