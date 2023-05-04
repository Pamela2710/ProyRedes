from mesh_network import MeshNetwork
import threading
import time

def handle_message(src, msg):
    print(f"Received message from {src}: {msg}")

def main():
    mesh = MeshNetwork("127.0.0.1", 5555)
    mesh.on_receive(handle_message)

    # Start the mesh network node
    mesh_thread = threading.Thread(target=mesh.run)
    mesh_thread.start()

    # Connect the node to another node in the mesh network
    other_node = ("127.0.0.1", 5556)
    mesh.connect_node(other_node)

    # Send messages to other nodes
    while True:
        message = input("Enter message to send: ")
        mesh.broadcast(message)

        time.sleep(1)

if __name__ == "__main__":
    main()
