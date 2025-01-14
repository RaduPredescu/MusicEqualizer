import os
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter
import pyaudio

class Signal:
    def __init__(self, entry_signal_path, label_result, sliders, frequencies):
        self.entry_signal_path = entry_signal_path
        self.signal_path = ""
        self.sampling_rate = 0
        self.signal = np.array([])
        self.label_result = label_result
        self.sliders = sliders
        self.frequencies = frequencies

    def load_signal(self):
        self.signal_path = self.entry_signal_path.get().strip()

        if not self.signal_path:
            self.label_result.config(text="Introdu path-ul")
            return

        if not os.path.exists(self.signal_path):
            self.label_result.config(text="Path-ul nu exista")
            return

        try:
            self.sampling_rate, self.signal = wavfile.read(self.signal_path)
            self.signal = self.signal.astype(np.float32) / np.max(np.abs(self.signal))  # Normalizare
            self.label_result.config(text="Semnalul a fost incarcat cu succes")
        except Exception as e:
            self.label_result.config(text=f"Eroare la incarcarea semnalului: {str(e)}")

    def butter_bandpass(self, lowcut, highcut, fs, order=4):
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def bandpass_filter(self, data, lowcut, highcut):
        b, a = self.butter_bandpass(lowcut, highcut, self.sampling_rate)
        return lfilter(b, a, data)

    def apply_equalizer(self, chunk):
        """
        Aplică reglajele egalizatorului în timp real pentru un chunk de semnal.
        """
        # Definirea intervalelor de frecvență pentru fiecare slider
        frequency_ranges = [
            (20, 80),     # 60Hz
            (80, 300),    # 250Hz
            (300, 700),   # 500Hz
            (700, 1500),  # 1kHz
            (1500, 3000), # 2kHz
            (3000, 6000), # 4kHz
            (6000, 12000),# 8kHz
            (12000, 20000) # 16kHz
        ]

        filtered_chunk = np.zeros_like(chunk)
        for i, (low, high) in enumerate(frequency_ranges):
            gain = self.sliders[i].get()  # Obține valoarea amplificării de la slider
            band = self.bandpass_filter(chunk, low, high)
            filtered_chunk += band * gain

        return np.clip(filtered_chunk, -1, 1)  # Se asigură că semnalul rămâne în intervalul [-1, 1]

    def play_signal_realtime(self):
        if len(self.signal) == 0:
            self.label_result.config(text="Incarcati mai intai un semnal")
            return

        # Configurarea stream-ului PyAudio
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paFloat32,
            channels=1 if len(self.signal.shape) == 1 else self.signal.shape[1],
            rate=self.sampling_rate,
            output=True,
        )

        # Procesare și redare pe bucăți
        chunk_size = 1024
        for i in range(0, len(self.signal), chunk_size):
            chunk = self.signal[i:i + chunk_size]
            filtered_chunk = self.apply_equalizer(chunk)  # Aplică reglajele în timp real
            stream.write(filtered_chunk.astype(np.float32).tobytes())

        # Închidere stream
        stream.stop_stream()
        stream.close()
        p.terminate()
