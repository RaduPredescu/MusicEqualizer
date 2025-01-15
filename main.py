import tkinter as tk
from tkinter import ttk, filedialog
from signal_utils import Signal

def open_file_dialog(entry):
    #functie pentru cautarea fisierului audio
    file_path = filedialog.askopenfilename(
        title="Selecteaza un fisier audio",
        filetypes=(("Fisiere WAV", "*.wav"), ("Toate fisierele", "*.*")))
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

root = tk.Tk()
root.title("Egalizator Audio")
root.geometry("1920x1080")

label_title = ttk.Label(root, text="Egalizator Audio", font=("Arial", 24))
label_title.pack(pady=20)

frequencies = ["60Hz", "120Hz", "250Hz", "500Hz", "1kHz", "2kHz", "4kHz", "8kHz", "16kHz"]
sliders = []

frame = ttk.Frame(root)
frame.pack(pady=10)

signal = None

def create_sliders(signal_obj):
    #functie ce creaza sliderele
    for freq in frequencies:
        col_frame = ttk.Frame(frame)
        col_frame.pack(side=tk.LEFT, padx=5)
        #sliderele determina amplificarea pe fiecare spectru de frecvente
        slider = ttk.Scale(
            col_frame,
            from_=2,
            to=0,
            length=200,
            orient=tk.VERTICAL)

        slider.set(1)
        slider.pack()
        sliders.append(slider)

        label = ttk.Label(col_frame, text=freq)
        label.pack(pady=5)

frame_path = ttk.Frame(root)
frame_path.pack(pady=20)

label_signal_path = ttk.Label(frame_path, text="Introdu calea catre semnal:")
label_signal_path.pack(side=tk.LEFT, padx=5)

entry_signal_path = ttk.Entry(frame_path, width=40)
entry_signal_path.pack(side=tk.LEFT, padx=5)

button_browse = ttk.Button(frame_path, text="Browse", command=lambda: open_file_dialog(entry_signal_path))
button_browse.pack(side=tk.LEFT, padx=5)

label_result = ttk.Label(root, text="", anchor="center", justify="center", wraplength=800)
label_result.pack(pady=20)

signal = Signal(entry_signal_path, label_result, sliders)

frame_volume = ttk.Frame(root)
frame_volume.pack(pady=10)

volume_label = ttk.Label(frame_volume, text="Volum general:", font=("Arial", 12))
volume_label.pack(side=tk.LEFT, padx=5)

volume_slider = ttk.Scale(
    frame_volume, from_=0, to=2, length=200, orient=tk.HORIZONTAL
)
volume_slider.set(1)
volume_slider.pack(side=tk.LEFT, padx=5)

signal.set_volume_control(volume_slider)
create_sliders(signal)

frame_buttons = ttk.Frame(root)
frame_buttons.pack(pady=20)

button_load = ttk.Button(frame_buttons, text="Incarca semnalul", command=lambda: signal.load_signal())

button_apply = ttk.Button(frame_buttons, text="Aplica egalizatorul", command=lambda: signal.apply_equalizer())

button_play = ttk.Button(frame_buttons, text="Reda semnalul", command=lambda: signal.play_signal())

# lista butoanelor de incarcat, aplicat egalizator si play pentru semnal
all_buttons = [button_load, button_apply, button_play]

button_load.pack(side=tk.LEFT, padx=10)
button_apply.pack(side=tk.LEFT, padx=10)
button_play.pack(side=tk.LEFT, padx=10)

root.mainloop()
