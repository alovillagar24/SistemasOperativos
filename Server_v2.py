# ===== SERVIDOR (password + whitelist) =====

import socket
import subprocess
import threading
import shlex  # Para parsear comandos de forma segura

PASSWORD = "clave159"
WHITELIST = ["sleep", "gedit", "python", "ls"]

def handle_client(conn, addr):
    try:
        # 1. Recibir password (buffer de 1024 es más eficiente)
        pwd = conn.recv(1024).decode().strip()
        if pwd != PASSWORD:
            conn.sendall(b"ERROR: Password incorrecta\n")
            return

        conn.sendall(b"OK: Autenticado\n")
        
        # 2. Recibir operación
        op = conn.recv(1024).decode().strip()
        
        if op == "1": # LISTAR
            # Usamos check_output para capturar la lista y enviarla al cliente
            resultado = subprocess.check_output("ps -eo pid,comm | tail -n 20", shell=True)
            conn.sendall(resultado)

        elif op == "2": # INICIAR
            conn.sendall(b"Esperando comando...\n")
            cmd_line = conn.recv(1024).decode().strip()
            
            # Validar contra whitelist de forma segura
            base_cmd = cmd_line.split()[0]
            if base_cmd in WHITELIST:
                # Ejecución en segundo plano sin shell=True (evita inyecciones)
                args = shlex.split(cmd_line)
                subprocess.Popen(args) 
                conn.sendall(f"SUCCESS: {base_cmd} iniciado\n".encode())
            else:
                conn.sendall(b"ERROR: Comando no permitido\n")

        elif op == "3": # DETENER
            conn.sendall(b"PID a detener?\n")
            pid = conn.recv(1024).decode().strip()
            if pid.isdigit():
                subprocess.run(["kill", pid])
                conn.sendall(b"SUCCESS: Proceso terminado\n")
            else:
                conn.sendall(b"ERROR: PID invalido\n")

    except Exception as e:
        print(f"Error con {addr}: {e}")
    finally:
        conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Evita error de puerto ocupado
    server.bind(("172.25.250.9", 5000))
    server.listen(5)
    print("[*] Servidor mejorado escuchando")

    while True:
        conn, addr = server.accept()
        # Multihilo para no bloquear el servidor
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
