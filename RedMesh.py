import socket
import threading

class Nodo:
    def __init__(self, direccion_ip):
        self.direccion_ip = direccion_ip
        self.vecinos = []
        self.socket_servidor = None

    def iniciar_hilo(self):
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_servidor.bind((self.direccion_ip, 8000))
        self.socket_servidor.listen()
        thread = threading.Thread(target=self.escuchar_conexiones_entrantes)
        thread.start()

    def escuchar_conexiones_entrantes(self):
        while True:
            conn, addr = self.socket_servidor.accept()
            print(f"Conexión entrante de {addr}")
            thread = threading.Thread(target=self.escuchar_mensajes, args=(conn,))
            thread.start()

    def escuchar_mensajes(self, conn):
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"Mensaje recibido en {self.direccion_ip}: {data.decode()}")
            for vecino in self.vecinos:
                self.enviar_mensaje(vecino, data)
        conn.close()

    def enviar_mensaje(self, direccion_ip_destino, mensaje):
        socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_cliente.connect((direccion_ip_destino, 8000))
        socket_cliente.send(mensaje.encode())
        socket_cliente.close()

nodo1 = Nodo("192.168.0.1")
nodo2 = Nodo("192.168.0.2")

nodo1.vecinos.append(nodo2.direccion_ip)
nodo2.vecinos.append(nodo1.direccion_ip)

nodo1.iniciar_hilo()
nodo2.iniciar_hilo()

