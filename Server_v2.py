# ===== SERVIDOR (password + whitelist) =====

import socket
import subprocess

PASSWORD = "clave159"
WHITELIST = ["sleep", "gedit", "python", "ls", "calc", "notepad"]

def handle_client(conn):
    try:
        # 1. Recibir y validar Password
        pwd = conn.recv(1024).decode().strip()
        
        if pwd != PASSWORD:
            print("Password incorrecta.")
            conn.sendall(b"ERROR\n")
            return
        
        # Enviamos OK para que el cliente sepa que puede enviar la operación
        conn.sendall(b"OK\n") 

        # 2. Recibir Operación
        op = conn.recv(1024).decode().strip()
        print(f"Operación solicitada: {op}")
        
        if op == "1": # LISTAR
            # Capturamos la salida para que el cliente la reciba
            resultado = subprocess.check_output("ps -eo pid,comm | tail -n 15", shell=True)
            conn.sendall(resultado)

        elif op == "2": # INICIAR
            # El cliente envía el comando tras elegir opción 2
            cmd = conn.recv(1024).decode().strip()
            
            # Verificamos si el comando base está en la whitelist
            if any(w in cmd for w in WHITELIST):
                # stdout=subprocess.DEVNULL evita que el servidor se trabe
                subprocess.Popen(cmd.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                conn.sendall(f"SUCCESS: Iniciado {cmd}\n".encode())
            else:
                conn.sendall(b"ERROR: Comando no permitido en Whitelist\n")

        elif op == "3": # DETENER
            # El cliente envía el PID tras elegir opción 3
            pid = conn.recv(1024).decode().strip()
            if pid.isdigit():
                subprocess.run(["kill", pid])
                conn.sendall(f"SUCCESS: PID {pid} detenido\n".encode())
            else:
                conn.sendall(b"ERROR: PID invalido\n")

    except Exception as e:
        print(f"Error procesando cliente: {e}")
    finally:
        conn.close()

# --- Configuración del Servidor ---
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("172.25.250.9", 5000))
server.listen(1)

print("Servidor listo y escuchando en 172.25.250.9:5000...")

while True:
    conn, addr = server.accept()
    print(f"Conexión establecida desde: {addr}")
    handle_client(conn)
