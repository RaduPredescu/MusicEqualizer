import tkinter as tk
from tkinter import ttk
from signal_utils import Signal
import sounddevice as sd

# Create the main application window
root = tk.Tk()
root.title("Egalizator Audio")
root.geometry("1920x1080")

label_title = ttk.Label(root, text="Egalizator Audio", font=("Arial", 24))
label_title.pack(pady=20)

# Frequencies for the equalizer
frequencies = ['<31', '63', '125', '250', '500', '1K', '2K', '4K', '8K', '>16K']
sliders = {}

frame = ttk.Frame(root)
frame.pack(pady=10)

for freq in frequencies:
    col_frame = ttk.Frame(frame)
    col_frame.pack(side=tk.LEFT, padx=5)

    slider = ttk.Scale(col_frame, from_=10, to=-10, length=200, orient=tk.VERTICAL)
    slider.set(0)  # Default position
    slider.pack()
    sliders[freq] = slider

    label = ttk.Label(col_frame, text=freq, font=("Arial", 10))
    label.pack(pady=5)

# Get audio devices
def get_audio_devices():
    devices = sd.query_devices()
    return [device['name'] for device in devices]

audio_devices = get_audio_devices()

# Input device selection
frame_input_output = ttk.Frame(root)
frame_input_output.pack(pady=20)

label_input = ttk.Label(frame_input_output, text="Select Input Device:", font=("Arial", 12))
label_input.pack(side=tk.LEFT, padx=5)

input_device_var = tk.StringVar()
input_dropdown = ttk.Combobox(frame_input_output, textvariable=input_device_var, width=40)
input_dropdown['values'] = audio_devices
input_dropdown.pack(side=tk.LEFT, padx=5)

# Output device selection
label_output = ttk.Label(frame_input_output, text="Select Output Device:", font=("Arial", 12))
label_output.pack(side=tk.LEFT, padx=5)

output_device_var = tk.StringVar()
output_dropdown = ttk.Combobox(frame_input_output, textvariable=output_device_var, width=40)
output_dropdown['values'] = audio_devices
output_dropdown.pack(side=tk.LEFT, padx=5)

label_result = ttk.Label(
    root, text="", font=("Arial", 12), anchor="center", justify="center", wraplength=800
)
label_result.pack(pady=20)

# Initialize the Signal class
signal = Signal(input_device_var, output_device_var, label_result)

# Frame for buttons
frame_buttons = ttk.Frame(root)
frame_buttons.pack(pady=20)

def apply_equalizer():
    # Retrieve slider values and process the audio stream
    eq_values = {freq: sliders[freq].get() for freq in frequencies}
    signal.start_processing(eq_values)

def stop_equalizer():
    signal.stop_processing()

button_start = ttk.Button(
    frame_buttons, text="Start", command=apply_equalizer
)
button_start.pack(side=tk.LEFT, padx=10)

button_stop = ttk.Button(
    frame_buttons, text="Stop", command=stop_equalizer
)
button_stop.pack(side=tk.LEFT, padx=10)

root.mainloop()
