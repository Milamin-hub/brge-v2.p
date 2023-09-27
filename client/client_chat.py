import socket
import pyaudio
import threading


class AudioThread:
    def __init__(self, func, *args) -> None:
        self.thread = threading.Thread(target=func, args=(*args,))
        self.thread.start()

    def join(self):
        self.thread.join()


class Audio:
    def __init__(self) -> None:
        # Initialize PyAudio
        self.audio = pyaudio.PyAudio()

        # For audio recording and sending
        self.audio_stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=44100,
            input=True
        )
        self.audio_thread_send = None

        # For audio receiving and playback
        self.audio_stream_play = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=44100,
            output=True
        )
        self.audio_thread_play = None


class AudioClient:
    def __init__(self) -> None:
        # Create a TCP socket for connecting to the server
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set the server's IP address and port for connection
        self.server_host = "0.0.0.0"  # Specify the server's IP address
        self.server_port = 12345  # Use the same port as the server

        # Connect to the server
        self.client_socket.connect((self.server_host, self.server_port))

        self.handle_audio = Audio()
        self.handle_audio.audio_thread_send = AudioThread(
            self.send_audio,
            self.handle_audio.audio_stream,
            self.client_socket
        )
        self.handle_audio.audio_thread_play = AudioThread(
            self.play_audio,
            self.handle_audio.audio_stream_play,
        )

    # Function for playing audio received from the server
    def play_audio(self, stream):
        while True:
            try:
                # Receive audio data from the server
                audio_data = self.client_socket.recv(1024)

                # Playback audio data
                stream.write(audio_data)
            except Exception as e:
                print(e)
                break

    # Function for recording audio and sending it to the server
    def send_audio(self, stream, connection):
        while True:
            try:
                # Read audio data from the microphone
                audio_data = stream.read(1024)

                # Send audio data to the server
                connection.send(audio_data)
            except Exception as e:
                print(e)
                break


class AudioChat:
    def __init__(self) -> None:
        self.client = AudioClient()

    def main(self):
        while True:
            try:
                pass  # Client interface, chat client
            except KeyboardInterrupt:
                break

        # Terminate audio threads and close the socket
        self.client.handle_audio.audio_thread_send.join()
        self.client.handle_audio.audio_thread_play.join()
        self.client.handle_audio.audio_stream.stop_stream()
        self.client.handle_audio.audio_stream.close()
        self.client.handle_audio.audio.terminate()
        self.client.client_socket.close()


if __name__ == '__main__':
    chat = AudioChat()
    chat.main()
