import socket
import threading
import pyaudio
from config import *


class ServerAudioChat:
    # List of connected clients
    clients = []

    def __init__(self) -> None:
        # initial PyAudio
        self.audio = pyaudio.PyAudio()

        # Create a TCP socket to establish connections with clients
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set the host and port to listen to
        self.host = HOST # Listen on all available interfaces
        self.port = PORT # Use port 12345 (you can choose another)

        self.socket_bind()

    def socket_bind(self):
        # Bind the socket to the host and port
        self.server_socket.bind((self.host, self.port))

    # Function to process audio data and send it to all clients
    def audio_broadcast(self, stream, connection):
        while True:
            try:
                self.audio_data = connection.recv(1024)
                if not self.audio_data:
                    break
                for client in self.clients:
                    if client != connection:
                        try:
                            client.send(self.audio_data)
                        except:
                            self.clients.remove(client)
            except Exception as e:
                print(e)
                break

    def server_loop(self):
        # Main server loop
        self.server_socket.listen(5)
        print(f"The server is listening on {self.host}:{self.port}")

    def main(self):

        self.server_loop()

        while True:
            try:
                client_socket, client_address = self.server_socket.accept()
                print(f"Client connected {client_address}")
                self.clients.append(client_socket)
                audio_stream = self.audio.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True)
                audio_thread = threading.Thread(target=self.audio_broadcast, args=(audio_stream, client_socket))
                audio_thread.start()
            except KeyboardInterrupt:
                break

        self.close()

    def close(self):
        # Terminate all threads and close sockets
        for client in self.clients:
            client.close()
        self.server_socket.close()
        self.audio.terminate()


if __name__ == '__main__':
    server = ServerAudioChat()
    server.main()