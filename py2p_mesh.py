import py2p
import threading
import time
import uuid

def handle_message(msg, sender):
    #clean_msg = extract_message(msg)
    print(f"Received message from {sender}: {msg}")

def extract_message(input_string):
    start_index = input_string.index("(b'") + 3
    end_index = input_string.index("',)")
    message = input_string[start_index:end_index]
    return message

def show_connected_devices(node):
    print("Connected devices:")
    for peer in node.routing_table:
        print(f"ID: {peer.recv.sender}, Address: {peer.addr}")
        
def message_to_string(message_obj):
    return str(message_obj.packets)

def main():
    # Create a new mesh node with a specified port
    node = py2p.MeshSocket('0.0.0.0', 5678)

    node.timeout = 10
    node.max_connections = 2

    # unique ID
    node.sender = str(uuid.uuid4())[:8]

    print(f"This node's address: {node.out_addr}")
    print(f"This node's ID: {node.sender}")

    # Connect to the bootstrap node if you know its address
    bootstrap_address = input("Enter the bootstrap node's address (IP:Port) or leave empty: ")
    if bootstrap_address:
        ip, port = bootstrap_address.split(':')
        node.connect(ip, int(port))

    # Start a thread to handle incoming messages
    def message_handler():
        while True:
            received = node.recv()

            if received:
                msg = received
                string_msg = message_to_string(msg)  # Convert the Message object to a string
                sender = received.sender
                handle_message(string_msg, sender)
            time.sleep(0.1)

    message_thread = threading.Thread(target=message_handler)
    message_thread.daemon = True
    message_thread.start()

    # Send messages to the other nodes
    while True:
        message = input("Enter message to send, 'exit' or 'show': ")

        if message == 'exit':
            break
        elif message == 'disconnect':
            node.disconnect()
            break
        elif message == 'show':
            show_connected_devices(node)
        else:
            node.send(bytes(message, 'utf-8'))

if __name__ == "__main__":
    main()
