import os
import numpy as np
from scipy.io import wavfile
import pyaudio

class Signal:
    def __init__(self, entry_signal_path, label_result, sliders):
        self.entry_signal_path = entry_signal_path
        self.signal_path = ""
        self.sampling_rate = 0
        self.signal = np.array([])
        self.label_result = label_result
        self.sliders = sliders

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
            self.signal = self.signal.astype(np.float32) / np.max(np.abs(self.signal))  # Normalize
            self.label_result.config(text="Semnalul a fost incarcat cu succes")
        except Exception as e:
            self.label_result.config(text=f"Eroare la incarcarea semnalului: {str(e)}")

    def apply_equalizer(self, signal):
        """
        Applies equalizer adjustments to the signal based on slider values.
        """
        for slider in self.sliders:
            gain = slider.get()  # Get the gain value (0 to 2)
            signal = signal * gain  # Apply the gain
        return np.clip(signal, -1, 1)  # Ensure the signal remains within [-1, 1]

    def play_filtered_signal(self):
        if len(self.signal) == 0:
            self.label_result.config(text="Incarcati mai intai un semnal")
            return

        # Create a PyAudio stream for playback
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paFloat32,
            channels=1 if len(self.signal.shape) == 1 else self.signal.shape[1],
            rate=self.sampling_rate,
            output=True,
        )

        # Apply equalizer and play signal in chunks
        chunk_size = 1024
        for i in range(0, len(self.signal), chunk_size):
            chunk = self.signal[i:i + chunk_size]
            filtered_chunk = self.apply_equalizer(chunk)
            stream.write(filtered_chunk.astype(np.float32).tobytes())

        # Close the stream
        stream.stop_stream()
        stream.close()
        p.terminate()
