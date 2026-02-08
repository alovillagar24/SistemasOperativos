# ===== MIDDLEWARE (selección de servidor) =====
# Agrega aquí los servidores disponibles en tu laboratorio

SERVERS = [
    ("172.25.250.9", 5000, "clave159"),
]

def seleccionar():
    while True:
        print("\n=== SELECCIÓN DE SERVIDOR REMOTO ===")
        for i, (ip, port, _) in enumerate(SERVERS):
            # No mostramos la clave aquí por seguridad
            print(f"[{i}] IP: {ip} | Puerto: {port}")
        
        try:
            sel = input("\nElige servidor (número) o 'q' para salir: ").strip()
            
            if sel.lower() == 'q':
                exit()

            idx = int(sel)
            if 0 <= idx < len(SERVERS):
                host, port, pwd = SERVERS[idx]
                print(f"[*] Conectando a {host}...")
                return host, port, pwd
            else:
                print(f"[!] Error: El número debe estar entre 0 y {len(SERVERS)-1}")
        
        except ValueError:
            print("[!] Error: Por favor, ingresa un número válido.")

# Ejemplo de uso interno para pruebas
if __name__ == "__main__":
    h, p, pw = seleccionar()
    print(f"Datos obtenidos: {h}:{p} con clave {pw}")