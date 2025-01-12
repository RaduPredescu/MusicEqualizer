import sounddevice as sd
from scipy.signal import butter, lfilter
import numpy as np

class Signal:
    def __init__(self, input_device_var, output_device_var, label_result, sliders):
        self.input_device_var = input_device_var
        self.output_device_var = output_device_var
        self.label_result = label_result
        self.sliders = sliders  # Store sliders for dynamic access
        self.sampling_rate = 44100
        self.stream = None

    def start_processing(self, eq_values):
        input_device = self.input_device_var.get()
        output_device = self.output_device_var.get()

        if not input_device or not output_device:
            self.label_result.config(text="Please select both input and output devices.")
            return

        try:
            input_index = [device['name'] for device in sd.query_devices()].index(input_device)
            output_index = [device['name'] for device in sd.query_devices()].index(output_device)

            # Define frequency ranges for the equalizer bands
            frequency_bands = {
                '<31': (0, 31),
                '63': (31, 63),
                '125': (63, 125),
                '250': (125, 250),
                '500': (250, 500),
                '1K': (500, 1000),
                '2K': (1000, 2000),
                '4K': (2000, 4000),
                '8K': (4000, 8000),
                '>16K': (16000, self.sampling_rate / 2),
            }

            # Callback function for the audio stream
            def callback(indata, outdata, frames, time, status):
                if status:
                    print(status)

                # Initialize processed_data as zeros
                processed_data = np.zeros_like(indata)

                nyquist = 0.5 * self.sampling_rate

                # Dynamically fetch the slider values for each band
                current_eq_values = {freq: self.sliders[freq].get() for freq in frequency_bands.keys()}

                # Apply equalizer filters
                for freq_label, gain in current_eq_values.items():
                    low, high = frequency_bands.get(freq_label, (0, 0))

                    # Normalize frequency range
                    low_norm = low / nyquist
                    high_norm = high / nyquist

                    if low_norm <= 0 or high_norm >= 1 or low_norm >= high_norm:
                        continue  # Skip invalid frequency ranges

                    # Design the Butterworth bandpass filter
                    b, a = butter(2, [low_norm, high_norm], btype='band')

                    # Apply the filter to the input data
                    band = lfilter(b, a, indata[:, 0])

                    # Scale the band by the slider gain
                    processed_data[:, 0] += band * (gain / 10.0)

                # Write the processed data to the output buffer
                outdata[:] = processed_data

            # Start the audio stream
            self.stream = sd.Stream(
                device=(input_index, output_index),
                samplerate=self.sampling_rate,
                channels=1,
                callback=callback,
            )
            self.stream.start()
            self.label_result.config(text="Audio processing started.")

        except Exception as e:
            self.label_result.config(text=f"Error: {e}")

    def stop_processing(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
            self.label_result.config(text="Audio processing stopped.")
