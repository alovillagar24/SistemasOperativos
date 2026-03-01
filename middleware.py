# ===== MIDDLEWARE (Selección y Verificación de Red) =====
import socket

# Lista de servidores disponibles
# Agregamos tu instancia de AWS con el puerto 5000 y la clave definida
SERVERS = [
    ("3.129.67.137", 5000, "clave159"), # Instancia AWS EC2
    ("172.25.250.9", 5000, "clave159"), # Laboratorio Local (RedHat)
    ("127.0.0.1", 5000, "clave159"),
]

def verificar_conexion(ip, puerto):
    """Intenta una conexión rápida para ver si el puerto está abierto en AWS"""
    try:
        # Timeout de 3 segundos para no quedarse colgado
        with socket.create_connection((ip, puerto), timeout=3):
            return True
    except:
        return False

def seleccionar():
    while True:
        print("\n" + "="*40)
        print("   SISTEMA DISTRIBUIDO - SELECCIÓN   ")
        print("="*40)
        
        for i, (ip, port, _) in enumerate(SERVERS):
            # No mostramos la clave por seguridad
            status = "[ONLINE]" if verificar_conexion(ip, port) else "[OFFLINE/BLOCKED]"
            print(f"[{i}] IP: {ip} | Puerto: {port} | Status: {status}")
        
        try:
            sel = input("\nElige servidor (número) o 'q' para salir: ").strip()
            
            if sel.lower() == 'q':
                print("[!] Saliendo del sistema...")
                exit()

            idx = int(sel)
            if 0 <= idx < len(SERVERS):
                host, port, pwd = SERVERS[idx]
                
                # Verificación final antes de entregar los datos
                if verificar_conexion(host, port):
                    print(f"[*] Conexión exitosa a {host}. Iniciando túnel...")
                    return host, port, pwd
                else:
                    print(f"[!] ADVERTENCIA: {host} parece no responder. Verifica el Security Group de AWS.")
                    confirmar = input("¿Intentar conectar de todos modos? (s/n): ").lower()
                    if confirmar == 's':
                        return host, port, pwd
            else:
                print(f"[!] Error: El número debe estar entre 0 y {len(SERVERS)-1}")
        
        except ValueError:
            print("[!] Error: Por favor, ingresa un número válido o 'q'.")

# Punto de entrada para pruebas del Middleware
if __name__ == "__main__":
    h, p, pw = seleccionar()
    print(f"\n[OK] Datos para el Cliente Principal:")
    print(f" > Host: {h}\n > Port: {p}\n > Pwd:  {pw}")
