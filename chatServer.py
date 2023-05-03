import socket
import threading
from RedMesh import RedMesh
from RedMesh import Nodo


class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.red_mesh = RedMesh()
        self.red_mesh.configurar_red_inalambrica("Piso2", "")
        self.red_mesh.agregar_nodo(self.host)

    def aceptar_conexiones(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Conexión aceptada desde {client_address}")
            cliente = Nodo(client_address[0])
            self.red_mesh.agregar_nodo(cliente.direccion_ip)
            cliente_socket_thread = threading.Thread(target=self.escuchar_cliente, args=(client_socket, cliente))
            cliente_socket_thread.start()

    def escuchar_cliente(self, client_socket, cliente):
        while True:
            try:
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                print(f"Mensaje recibido desde {cliente.direccion_ip}: {data}")
                self.red_mesh.enrutamiento_congestion(cliente.direccion_ip, self.host, data.encode())
            except Exception as e:
                print(e)
                break
        client_socket.close()
        self.red_mesh.eliminar_nodo(cliente.direccion_ip)

    def iniciar(self):
        print(f"Servidor de chat iniciado en {self.host}:{self.port}")
        aceptar_conexiones_thread = threading.Thread(target=self.aceptar_conexiones)
        aceptar_conexiones_thread.start()

#Para ejecutar en 3 maquinas virtuales
#En mi caso uso tengo la IP 192.168.0.101 del servidor
server = ChatServer('192.168.56.1', 8000)
server.iniciar()


