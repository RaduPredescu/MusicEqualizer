import os
import numpy as np
from scipy.io import wavfile
import sounddevice as sd

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
        """Set the volume slider."""
        self.volume_slider = volume_slider

    def load_signal(self):
        """Load the signal from the specified path."""
        self.signal_path = self.entry_signal_path.get().strip()

        if not self.signal_path:
            self.label_result.config(text="Introdu path-ul")
            return

        if not os.path.exists(self.signal_path):
            self.label_result.config(text="Path-ul nu exista")
            return

        try:
            self.sampling_rate, self.signal = wavfile.read(self.signal_path)
            if self.signal.ndim > 1:
                self.signal = self.signal[:, 0]  # Convert to mono if stereo
            self.label_result.config(text="Semnalul a fost incarcat cu succes")
        except Exception as e:
            self.label_result.config(text=f"Eroare la incarcarea semnalului: {str(e)}")

    def apply_equalizer(self):
        """Apply the equalizer to the entire signal."""
        if len(self.signal) == 0:
            self.label_result.config(text="Nu este incarcat niciun semnal")
            return

        # Frequency bands for the equalizer
        center_frequencies = [60, 120, 250, 500, 1000, 2000, 4000, 8000, 16000]  # in Hz
        bandwidth_factor = 1 / 3  # ±1/3 octave

        # Get FFT bins and frequencies
        freqs = np.fft.rfftfreq(len(self.signal), d=1 / self.sampling_rate)
        signal_fft = np.fft.rfft(self.signal)

        # Apply equalizer gains
        gains = [slider.get() for slider in self.sliders]
        for center, gain in zip(center_frequencies, gains):
            # Calculate band range
            low = center / (2 ** (bandwidth_factor / 2))
            high = center * (2 ** (bandwidth_factor / 2))

            # Identify bins in this range
            band = (freqs >= low) & (freqs < high)

            # Apply gain (convert dB to linear scale)
            signal_fft[band] *= 10 ** (gain)

        # Convert back to time domain
        self.processed_signal = np.fft.irfft(signal_fft).astype(np.float32)

        # Apply volume adjustment
        if self.volume_slider:
            volume = self.volume_slider.get()
            self.processed_signal *= volume

        # Clip to int16 range
        self.processed_signal = np.clip(self.processed_signal, -32768, 32767).astype(np.int16)
        self.label_result.config(text="Egalizatorul a fost aplicat")

    def play_signal(self):
        """Play the processed signal."""
        if self.processed_signal is None:
            self.label_result.config(text="Aplica egalizatorul înainte de redare")
            return

        try:
            sd.play(self.processed_signal, samplerate=self.sampling_rate)
            self.label_result.config(text="Redarea a început")
            sd.wait()  # Block until playback finishes
        except Exception as e:
            self.label_result.config(text=f"Eroare la redarea semnalului: {str(e)}")
