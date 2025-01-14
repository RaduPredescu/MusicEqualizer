import tkinter as tk
from tkinter import ttk, filedialog
from signal_utils import Signal

def open_file_dialog(entry):
    file_path = filedialog.askopenfilename(
        title="Selectează un fișier audio",
        filetypes=(("Fișiere WAV", "*.wav"), ("Toate fișierele", "*.*"))
    )
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def disable_buttons(buttons):
    """Disable a list of buttons."""
    for button in buttons:
        button.config(state=tk.DISABLED)

def enable_buttons(buttons):
    """Enable a list of buttons."""
    for button in buttons:
        button.config(state=tk.NORMAL)

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
    for freq in frequencies:
        col_frame = ttk.Frame(frame)
        col_frame.pack(side=tk.LEFT, padx=5)

        slider = ttk.Scale(
            col_frame,
            from_=10,
            to=-10,
            length=200,
            orient=tk.VERTICAL
        )
        slider.set(0)
        slider.pack()
        sliders.append(slider)

        label = ttk.Label(col_frame, text=freq, font=("Arial", 10))
        label.pack(pady=5)

frame_path = ttk.Frame(root)
frame_path.pack(pady=20)

label_signal_path = ttk.Label(
    frame_path, text="Introdu path-ul către semnal:", font=("Arial", 12)
)
label_signal_path.pack(side=tk.LEFT, padx=5)

entry_signal_path = ttk.Entry(frame_path, width=40)
entry_signal_path.pack(side=tk.LEFT, padx=5)

button_browse = ttk.Button(
    frame_path, text="Browse", command=lambda: open_file_dialog(entry_signal_path)
)
button_browse.pack(side=tk.LEFT, padx=5)

label_result = ttk.Label(
    root, text="", font=("Arial", 12), anchor="center", justify="center", wraplength=800
)
label_result.pack(pady=20)

signal = Signal(entry_signal_path, label_result, sliders)

frame_volume = ttk.Frame(root)
frame_volume.pack(pady=10)

volume_label = ttk.Label(frame_volume, text="Volum general:", font=("Arial", 12))
volume_label.pack(side=tk.LEFT, padx=5)

volume_slider = ttk.Scale(
    frame_volume, from_=0, to=2, length=200, orient=tk.HORIZONTAL
)
volume_slider.set(1)  # Default volume (1x)
volume_slider.pack(side=tk.LEFT, padx=5)

signal.set_volume_control(volume_slider)
create_sliders(signal)

frame_buttons = ttk.Frame(root)
frame_buttons.pack(pady=20)

button_load = ttk.Button(
    frame_buttons, text="Încarcă semnalul", command=lambda: execute_action(signal.load_signal)
)
button_apply = ttk.Button(
    frame_buttons, text="Aplică egalizatorul", command=lambda: execute_action(signal.apply_equalizer)
)
button_play = ttk.Button(
    frame_buttons, text="Redă semnalul", command=lambda: execute_action(signal.play_signal)
)

# List of buttons to manage enable/disable
all_buttons = [button_load, button_apply, button_play]

button_load.pack(side=tk.LEFT, padx=10)
button_apply.pack(side=tk.LEFT, padx=10)
button_play.pack(side=tk.LEFT, padx=10)

def execute_action(action):
    """Execute an action with buttons temporarily disabled."""
    disable_buttons(all_buttons)
    root.after(100, lambda: [action(), enable_buttons(all_buttons)])

root.mainloop()
