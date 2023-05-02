import socket
import threading
import RedMesh
from RedMesh import Nodo


class ChatClient:
    def __init__(self, host, port, username):
        self.host = host
        self.port = port
        self.username = username
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        self.nodo = Nodo(socket.gethostbyname(socket.gethostname()))
        self.red_mesh = RedMesh()
        self.red_mesh.agregar_nodo(self.nodo.direccion_ip)
        self.red_mesh.configurar_red_inalambrica("MiRed", "contraseña")
        self.iniciar_escucha()

    def enviar_mensaje(self, mensaje):
        try:
            self.client_socket.sendall(mensaje.encode())
        except Exception as e:
            print(e)

    def recibir_mensaje(self):
        while True:
            try:
                data = self.client_socket.recv(1024).decode()
                if not data:
                    break
                print(data)
            except Exception as e:
                print(e)
                break
        self.client_socket.close()

    def iniciar_escucha(self):
        recibir_mensaje_thread = threading.Thread(target=self.recibir_mensaje)
        recibir_mensaje_thread.start()

#Para las otras 2 maquinas o n maquinas (clientes)
#En mi caso uso tengo la IP 192.168.0.101 del servidor
client = ChatClient('192.168.0.101', 8000, 'Cliente1')
client.enviar_mensaje('Hola, ¿cómo están?')