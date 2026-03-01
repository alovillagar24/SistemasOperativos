############################################################
#                                                          #
#   GESTOR DE PROCESOS DISTRIBUIDO (AWS-HYBRID SYSTEM)     #
#                                                          #
############################################################

/ DESCRIPCION /
------------------------------------------------------------
Arquitectura distribuida para la administracion remota de 
instancias AWS EC2. El sistema utiliza tuneles SSH para 
operar sobre redes restringidas mediante encapsulamiento 
de sockets TCP.

/ ARQUITECTURA DEL SISTEMA /
------------------------------------------------------------
[ WEB BROWSER ] <---> [ FLASK GUI ] <---> [ SSH TUNNEL ] <---> [ AWS EC2 ]
      (8080)             (5000)             (443)             (5000)



/ COMPONENTES /
------------------------------------------------------------
# SERVIDOR (servidor.py):
  Ejecutado en el nodo remoto. Gestiona señales de sistema
  (ps, Popen, kill) bajo una politica de WHITELIST.

# MIDDLEWARE (middleware.py):
  Capa de diagnostico. Realiza sondeos de red (polling) 
  para verificar disponibilidad de nodos.

# CLIENTE WEB (gui.py):
  Interfaz Flask que traduce peticiones HTTP en flujos 
  binarios de Sockets.

/ CONFIGURACION DE RED /
------------------------------------------------------------
Para conectar en entornos bloqueados, se utiliza Local 
Port Forwarding:

[ COMANDO DE TUNELIZACION ]
# ssh -i llave.pem -p 443 -L 5000:localhost:5000 ec2-user@ip



/ DESPLIEGUE /
------------------------------------------------------------
1 // Iniciar servidor en AWS:
     # python3 servidor.py

2 // Iniciar cliente en Local:
     # python3 gui.py

3 // Acceso via Navegador:
     # URL: http://127.0.0.1:8080

/ MATRIZ DE FUNCIONES /
------------------------------------------------------------
| ACCION     | COMANDO REMOTO | DESCRIPCION                |
|------------|----------------|----------------------------|
| LISTAR     | ps -eo         | Recupera tabla de procesos |
| EJECUTAR   | Popen          | Inicia procesos en background|
| FINALIZAR  | kill -9        | Detencion forzada por PID  |



############################################################
# ESTATUS: OPERACIONAL // PROTOCOLO: TCP/IP // PUERTO: 443 #
############################################################
