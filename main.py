import tkinter as tk
from tkinter import ttk
from signal_utils import Signal

root = tk.Tk()
root.title("Egalizator Audio")
root.geometry("1920x1080")

label_title = ttk.Label(root, text="Egalizator Audio", font=("Arial", 24))
label_title.pack(pady=20)

# Frecvențe pentru sliderele egalizatorului
frequencies = ["60Hz", "250Hz", "500Hz", "1kHz", "2kHz", "4kHz", "8kHz", "16kHz"]
sliders = []

frame = ttk.Frame(root)
frame.pack(pady=10)

for freq in frequencies:
    col_frame = ttk.Frame(frame)
    col_frame.pack(side=tk.LEFT, padx=5)

    # Slider cu intervalul (0, 2)
    slider = ttk.Scale(col_frame, from_=2, to=0, length=200, orient=tk.VERTICAL)
    slider.set(1)  # Valoare implicită 1 (amplificare neutră)
    slider.pack()
    sliders.append(slider)

    label = ttk.Label(col_frame, text=freq, font=("Arial", 10))
    label.pack(pady=5)

frame_path = ttk.Frame(root)
frame_path.pack(pady=20)

label_signal_path = ttk.Label(
    frame_path, text="Introdu path-ul catre semnal:", font=("Arial", 12)
)
label_signal_path.pack(side=tk.LEFT, padx=5)

entry_signal_path = ttk.Entry(frame_path, width=40)
entry_signal_path.pack(side=tk.LEFT, padx=5)

label_result = ttk.Label(
    root, text="", font=("Arial", 12), anchor="center", justify="center", wraplength=800
)
label_result.pack(pady=20)

signal = Signal(entry_signal_path, label_result, sliders, frequencies)  # Transmit sliderele și frecvențele către clasă

frame_buttons = ttk.Frame(root)
frame_buttons.pack(pady=20)

button_load = ttk.Button(
    frame_buttons, text="Incarca semnalul", command=signal.load_signal
)
button_load.pack(side=tk.LEFT, padx=10)

button_play = ttk.Button(
    frame_buttons, text="Reda semnalul in timp real", command=signal.play_signal_realtime
)
button_play.pack(side=tk.LEFT, padx=10)

root.mainloop()
