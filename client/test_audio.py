import pyaudio
import wave


class TestAudio:
    def __init__(self) -> None:
        self.audio = pyaudio.PyAudio()
        self.OUTPUT_FILENAME = "tests/audio/test.wav"
        self.CHANNELS = 2
        self.RATE = 44100
        self.RECORD_SECONDS = 5
        self.FORMAT = pyaudio.paALSA
        self.stream = None
        self.frames = None

    def start(self):
        self.stream = self.audio.open(
            format=self.FORMAT, channels=self.CHANNELS,
            rate=self.RATE, input=True,
            frames_per_buffer=1024
        )
        print("Record started...")

    def record(self):
        self.start()
        self.frames = []

        # Запись аудио
        for _ in range(0, int(self.RATE / 1024 * self.RECORD_SECONDS)):
            data = self.stream.read(1024)
            self.frames.append(data)

        self.close()

    def close(self):
        print("Record completed.")
        # Остановка и закрытие потока
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

        self.save()

    def save(self):
        # Сохранение записи в файл WAV
        with wave.open(self.OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(self.frames))
            
        print(f"Record save in {self.OUTPUT_FILENAME}")


if __name__ == "__main__":
    audio = TestAudio()
    audio.record()
