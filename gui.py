from flask import Flask, render_template_string, request, jsonify
import socket

app = Flask(__name__)

# Configuración del Túnel hacia AWS
AWS_HOST = "127.0.0.1"
AWS_PORT = 5000
PASSWORD = "clave159"

# HTML/CSS con el diseño de tu imagen
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Gestor de Procesos (Cliente Web)</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #2b2b2b; color: white; margin: 0; padding: 20px; }
        .header { background-color: #333; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
        h1 { margin: 0; font-size: 28px; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .card { background-color: #eee; color: #333; padding: 20px; border-radius: 10px; }
        .card h3 { margin-top: 0; color: #000; }
        .path { color: #0066cc; font-weight: bold; margin: 10px 0; }
        input { padding: 8px; width: 60%; border-radius: 5px; border: 1px solid #ccc; }
        button { padding: 10px 20px; background-color: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button.kill { background-color: #dc3545; }
        #console { background-color: #1e1e1e; color: #33ff33; padding: 15px; border-radius: 5px; margin-top: 20px; height: 300px; overflow-y: scroll; font-family: monospace; white-space: pre; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Gestor de Procesos (Cliente Web)</h1>
        <p>HOST: {{host}} | PORT: {{port}} | Servidor: AWS_EC2</p>
    </div>

    <div class="grid">
        <div class="card">
            <h3>1) Listar procesos</h3>
            <p>Obtén la lista de procesos (salida de ps del servidor).</p>
            <div class="path">/procesos</div>
            <button onclick="enviar('1')">Ver Procesos</button>
        </div>
        
        <div class="card">
            <h3>2) Iniciar comando</h3>
            <p>Ejemplo: sleep 60. (whitelist: sleep, python3, ping).</p>
            <div class="path">/run</div>
            <input type="text" id="cmd" placeholder="Comando...">
            <button onclick="enviar('2', document.getElementById('cmd').value)">Ejecutar</button>
        </div>

        <div class="card">
            <h3>3) Terminar por PID</h3>
            <p>Envía una señal para finalizar un proceso por su ID.</p>
            <div class="path">/kill</div>
            <input type="text" id="pid" placeholder="PID...">
            <button class="kill" onclick="enviar('3', document.getElementById('pid').value)">Terminar</button>
        </div>
    </div>

    <div id="console">Esperando respuesta del servidor...</div>

    <script>
        async function enviar(op, extra='') {
            const consoleDiv = document.getElementById('console');
            consoleDiv.innerText = "Conectando con AWS...";
            
            const res = await fetch('/ejecutar', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({op, extra})
            });
            const data = await res.json();
            consoleDiv.innerText = data.output;
        }
    </script>
</body>
</html>
"""

def socket_comunicacion(op, extra=""):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((AWS_HOST, AWS_PORT))
            s.sendall(f"{PASSWORD}\n".encode())
            auth = s.recv(1024).decode().strip()
            
            if "OK" not in auth.upper(): return "Error de Autenticación"

            s.sendall(f"{op}\n".encode())
            if extra: s.sendall(f"{extra}\n".encode())

            respuesta = ""
            while True:
                data = s.recv(4096).decode(errors='ignore')
                if not data: break
                respuesta += data
            return respuesta
    except Exception as e:
        return f"Error de conexión: {str(e)}"

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, host=AWS_HOST, port=AWS_PORT)

@app.route('/ejecutar', methods=['POST'])
def ejecutar():
    data = request.json
    salida = socket_comunicacion(data['op'], data['extra'])
    return jsonify({"output": salida})

if __name__ == '__main__':
    # Corremos en el 8080 para que lo abras en tu navegador
    print("Iniciando Web Dashboard en http://127.0.0.1:8080")
    app.run(host='0.0.0.0', port=8080)
