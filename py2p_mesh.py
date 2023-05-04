import py2p
import threading
import time

def handle_message(msg):
    clean_msg = extract_message(msg)
    print(f"Received message: {clean_msg}")

def extract_message(input_string):
    start_index = input_string.index("(b'") + 3
    end_index = input_string.index("',)")
    message = input_string[start_index:end_index]
    return message

def main():
    # Create a new mesh node with a specified port
    node = py2p.MeshSocket('0.0.0.0', 5678)

    # Connect to the bootstrap node if you know its address
    bootstrap_address = input("Enter the bootstrap node's address (IP:Port) or leave empty: ")
    if bootstrap_address:
        ip, port = bootstrap_address.split(':')
        node.connect(ip, int(port))

    print(f"This node's address: {node.out_addr}")

    # Start a thread to handle incoming messages
    def message_handler():
        while True:
            msg, sender = node.recv()
            if msg:
                handle_message(msg)
            time.sleep(0.1)

    message_thread = threading.Thread(target=message_handler)
    message_thread.daemon = True
    message_thread.start()

    # Send messages to the other nodes
    while True:
        message = input("Enter message to send, 'exit' to quit, or 'disconnect' to disconnect: ")

        if message == 'exit':
            break
        elif message == 'disconnect':
            node.disconnect()
            break
        else:
            node.send(bytes(message, 'utf-8'))

if __name__ == "__main__":
    main()
