import os
from scipy.io import wavfile


class Signal:
    def __init__(self, entry_signal_path, label_result):
        self.entry_signal_path = entry_signal_path
        self.signal_path = ""
        self.sampling_rate = 0.0
        self.signal = []
        self.label_result = label_result

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
            self.label_result.config(text="Semnalul a fost incarcat cu succes")
            
        except Exception as e:
            self.label_result.config(text="Eroare la incarcarea semnalului")
            error_message = f"Eroare la incarcarea semnalului: {str(e)}"
            self.label_result.config(text=error_message)

    # TODO implement equalizer functions
    def apply_equalizer(self):
        pass
