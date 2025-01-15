import os
import numpy as np
from scipy.io import wavfile
import sounddevice as sd
import math

class Signal:
    def __init__(self, entry_signal_path, label_result, sliders):
        self.entry_signal_path = entry_signal_path
        self.signal_path = ""
        self.sampling_rate = 0
        self.signal = []
        self.processed_signal = None
        self.label_result = label_result
        self.sliders = sliders
        self.volume_slider = None

    def set_volume_control(self, volume_slider):
        #seteaza volumul
        self.volume_slider = volume_slider

    def load_signal(self):
        #incarca semnalul
        self.signal_path = self.entry_signal_path.get().strip()

        if not self.signal_path:
            self.label_result.config(text="Introdu calea")
            return

        if not os.path.exists(self.signal_path):
            self.label_result.config(text="Calea nu exista")
            return

        try:
            self.sampling_rate, self.signal = wavfile.read(self.signal_path)
            if self.signal.ndim > 1:
                self.signal = self.signal[:, 0]  # Convert to mono if stereo
            self.label_result.config(text="Semnalul a fost incarcat cu succes")
        except Exception as e:
            self.label_result.config(text=f"Eroare la incarcarea semnalului: {str(e)}")

    def apply_equalizer(self):
        #Aplicarea egalizatorului
        if len(self.signal) == 0:
            self.label_result.config(text="Nu este incarcat niciun semnal")
            return

        center_frequencies = [62.5, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]  # in Hz

        # Spectrul
        freqs = np.fft.rfftfreq(len(self.signal), d=1 / self.sampling_rate)

        #Transformata fourier a semnalului
        signal_fft = np.fft.rfft(self.signal)

        # aplicarea egalizatorului
        gains = [slider.get() for slider in self.sliders]
        for center, gain in zip(center_frequencies, gains):
            # calculam pe care se aplica egalizatorul

            low = center / (math.sqrt(2))
            high = center * (math.sqrt(2))
            band = (freqs >= low) & (freqs < high)

            #aplicam gain-ul doar pentru banda corespunzatoare (unde band este True)
            signal_fft[band] *= gain

        # convertim inapoi in domeniu timp
        self.processed_signal = np.fft.irfft(signal_fft).astype(np.float32)

        # ajustare volum
        if self.volume_slider:
            volume = self.volume_slider.get()
            self.processed_signal *= volume

        # reconversie la int16
        self.processed_signal = np.clip(self.processed_signal, -32768, 32767).astype(np.int16)
        self.label_result.config(text="Egalizatorul a fost aplicat")

    def play_signal(self):
        #redare audio
        if self.processed_signal is None:
            self.label_result.config(text="Aplica egalizatorul inainte de redare")
            return

        try:
            sd.play(self.processed_signal, samplerate=self.sampling_rate)
            self.label_result.config(text="Redarea a inceput")
            sd.wait() 
        except Exception as e:
            self.label_result.config(text=f"Eroare la redarea semnalului: {str(e)}")
