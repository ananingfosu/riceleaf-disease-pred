from PIL import ImageTk
import PIL.Image
from tkinter import *
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import font as tkFont
from skimage.io import imread
from skimage.transform import resize
import skimage, pickle
import os
import sys

# Modern font fallback
MODERN_FONT = ("Poppins", 13)
HEADER_FONT = ("Poppins", 22, "bold")
PRED_FONT = ("Poppins", 23, "bold")

# Color palettes
LIGHT = {
    "bg": "#f7f7f5",  # soft white
    "primary": "#228B22",  # forest green
    "secondary": "#bfa76f",  # soft brown
    "accent": "#FFD700",  # golden yellow
    "text": "#222",
    "button_bg": "#228B22",
    "button_fg": "#fff",
    "button_hover": "#145214",
    "pred_bg": "#fff",
    "pred_border": "#228B22"
}
DARK = {
    "bg": "#23272e",
    "primary": "#4caf50",
    "secondary": "#a1887f",
    "accent": "#FFD700",
    "text": "#f7f7f5",
    "button_bg": "#4caf50",
    "button_fg": "#fff",
    "button_hover": "#357a38",
    "pred_bg": "#2e323a",
    "pred_border": "#4caf50"
}

current_theme = LIGHT

def set_theme(theme):
    global current_theme
    current_theme = theme
    windo.configure(bg=theme["bg"])
    left_frame.configure(bg=theme["bg"])
    right_frame.configure(bg=theme["bg"])
    instructions.configure(bg=theme["bg"], fg=theme["text"])
    toggle_btn.configure(bg=theme["secondary"], fg=theme["text"])
    upload_btn.configure(bg=theme["button_bg"], fg=theme["button_fg"], activebackground=theme["button_hover"])
    # Predict and Reset button colors will be handled by their state update functions
    if hasattr(windo, "pred_box") and windo.pred_box:
        windo.pred_box.configure(bg=theme["pred_bg"], fg=theme["primary"], highlightbackground=theme["pred_border"], highlightcolor=theme["pred_border"])
    # Ensure disabled buttons stay grey after theme toggle
    if predict_btn['state'] == 'disabled':
        predict_btn.config(bg=INACTIVE_GREY, fg="#fff", activebackground=INACTIVE_GREY)
    if reset_btn['state'] == 'disabled':
        reset_btn.config(bg=INACTIVE_GREY, fg="#fff", activebackground=INACTIVE_GREY)

windo = Tk()
windo.title("Rice Disease Prediction GUI")
windo.geometry('1120x820')
windo.iconbitmap('./images/rice.ico')
windo.resizable(True, True)
windo.configure(bg=LIGHT["bg"])

# Configure grid for responsiveness
windo.grid_rowconfigure(1, weight=1)
windo.grid_columnconfigure(0, weight=1)
windo.grid_columnconfigure(1, weight=2)

# Header (spans both columns)
header = tk.Label(windo, text="Rice Disease Prediction", font=("Poppins", 26, "bold"), bg=LIGHT["primary"], fg=LIGHT["button_fg"], pady=15)
header.grid(row=0, column=0, columnspan=2, sticky="ew")

# Left and right frames
left_frame = Frame(windo, bg=LIGHT["bg"])
right_frame = Frame(windo, bg=LIGHT["bg"])
left_frame.grid(row=1, column=0, sticky="nsew")
right_frame.grid(row=1, column=1, sticky="nsew")
windo.grid_rowconfigure(1, weight=1)
windo.grid_columnconfigure(0, weight=1)
windo.grid_columnconfigure(1, weight=2)
left_frame.grid_propagate(False)
right_frame.grid_propagate(False)

# Dark mode toggle
is_dark = False
def toggle_mode():
    global is_dark
    is_dark = not is_dark
    set_theme(DARK if is_dark else LIGHT)
    toggle_btn.configure(text="Light Mode" if is_dark else "Dark Mode")

toggle_btn = tk.Button(windo, text="Dark Mode", command=toggle_mode, font=MODERN_FONT, bg=LIGHT["secondary"], fg=LIGHT["text"], bd=0, relief="flat", padx=10, pady=3)
toggle_btn.grid(row=0, column=1, sticky="ne", padx=20, pady=10)

# Instructions
instructions = tk.Label(
    left_frame,
    text="1. Upload a rice leaf image (png or jpg)\n2. Click Predict to see the result\n3. Click Restart to restart the application or \n4. Just click upload to predict a new rice leaf image",
    font=MODERN_FONT,
    bg=LIGHT["bg"],
    fg=LIGHT["text"],
    justify="left",
    wraplength=320  # Initial value; will be updated dynamically
)
instructions.grid(row=0, column=0, sticky="ew", padx=30, pady=(30,10))

def update_instruction_wrap(event):
    # Subtract padding to avoid overflow
    instructions.config(wraplength=max(100, event.width - 60))

left_frame.bind('<Configure>', update_instruction_wrap)

#Size for displaying Image
w = 400; h = 300
size = (w, h) 

def on_enter(e, btn, color):
    btn['bg'] = color

def on_leave(e, btn, color):
    btn['bg'] = color

def upload_im():
    try:
        global im, resized, path, display, img_frame
        path = filedialog.askopenfilename()
        if not path:
            return
        im = PIL.Image.open(path)
        resized = im.resize(size, PIL.Image.Resampling.LANCZOS)
        tkimage = ImageTk.PhotoImage(resized)
        # Remove previous image preview frame if exists
        for widget in right_frame.winfo_children():
            if isinstance(widget, tk.Frame) and getattr(widget, 'is_img_frame', False):
                widget.destroy()
        img_box_width = 600
        img_box_height = 300
        img_frame = tk.Frame(right_frame, width=img_box_width, height=img_box_height, bg=current_theme["bg"])
        img_frame.place(x=60, y=80)
        img_frame.is_img_frame = True
        display = tk.Label(img_frame, image=tkimage, bg=current_theme["bg"])
        display.imgtk = tkimage
        display.place(relx=0.5, rely=0.5, anchor="center")
        # Remove previous prediction box if exists
        if hasattr(windo, "pred_box") and windo.pred_box:
            windo.pred_box.destroy()
        # Enable predict button
        update_predict_btn_state(True)
    except Exception as e:
        print(e)
        messagebox.showerror("Image Upload Error", "Please upload a valid Image file (PNG or JPG).\nError: {}".format(e))

def destroy_widget(widget):
    widget.destroy()

def prediction():
    def load_image(im_file):
        dimension = (104, 104)
        flat_data = []
        img = skimage.io.imread(im_file)
        img_resized = resize(img, dimension, anti_aliasing=True, mode='reflect')
        flat_data.append(img_resized.flatten())
        return flat_data
    try:
        # Get the absolute path of the script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(script_dir, 'model', 'rice_pred.pkl')
        with open(model_path, 'rb') as f:
            clf = pickle.load(f)
        img = load_image(path)
        pred = clf.predict(img)
        labels = ['Bacterial leaf blight', 'Brown spot', 'Leaf smut']
        s = [str(i) for i in pred]
        a = int("".join(s))
        lab = str("Predicted Disease is " + labels[a])
        # Remove previous prediction box if exists
        if hasattr(windo, "pred_box") and windo.pred_box:
            windo.pred_box.destroy()
        pred_box_width = 600
        windo.pred_box = tk.Label(
            right_frame,
            text=lab,
            font=("Poppins", 27, "bold"),
            bg=current_theme["pred_bg"],
            fg=current_theme["primary"],
            bd=0,
            padx=30,
            pady=30,
            relief="flat",
            highlightthickness=4,
            highlightbackground=current_theme["pred_border"],
            highlightcolor=current_theme["pred_border"],
            wraplength=pred_box_width-40,  # wrap text at width minus padding
            justify="center"
        )
        # Calculate the required height after wrapping
        windo.pred_box.update_idletasks()
        text_height = windo.pred_box.winfo_reqheight()
        windo.pred_box.place(x=60, y=420, width=pred_box_width, height=text_height)
        update_reset_btn_state(True)
    except FileNotFoundError:
        messagebox.showerror("Model Not Found", "Model not found. Please ensure the model directory contains rice_pred.pkl")
    except Exception as e:
        print(f"Error during prediction: {e}")
        messagebox.showerror("Prediction Error", "Error during prediction. Please check the image format and try again.\nError: {}".format(e))

# Upload Button
upload_btn = tk.Button(left_frame, text='Upload Image', font=MODERN_FONT, bg=LIGHT["button_bg"], fg=LIGHT["button_fg"], activebackground=LIGHT["button_hover"], bd=0, relief="flat", padx=18, pady=12, command=upload_im, cursor="hand2")
upload_btn.grid(row=1, column=0, sticky="ew", padx=30, pady=(10, 8))
upload_btn.bind("<Enter>", lambda e: on_enter(e, upload_btn, current_theme["button_hover"]))
upload_btn.bind("<Leave>", lambda e: on_leave(e, upload_btn, current_theme["button_bg"]))

# Predict Button
INACTIVE_GREY = "#b0b0b0"

predict_btn = tk.Button(left_frame, text='Predict Disease', font=MODERN_FONT, bg=INACTIVE_GREY, fg="#fff", activebackground=INACTIVE_GREY, bd=0, relief="flat", padx=18, pady=12, command=prediction, state='disabled', cursor="hand2")
predict_btn.grid(row=2, column=0, sticky="ew", padx=30, pady=8)

def update_predict_btn_state(active):
    if active:
        predict_btn.config(state='normal', bg=current_theme["button_bg"], fg=current_theme["button_fg"], activebackground=current_theme["button_hover"])
    else:
        predict_btn.config(state='disabled', bg=INACTIVE_GREY, fg="#fff", activebackground=INACTIVE_GREY)

# Only apply hover if active
predict_btn.bind("<Enter>", lambda e: predict_btn.config(bg=current_theme["button_hover"]) if predict_btn['state']=='normal' else None)
predict_btn.bind("<Leave>", lambda e: predict_btn.config(bg=current_theme["button_bg"]) if predict_btn['state']=='normal' else None)

# Reset Button
def reset_app():
    windo.destroy()
    os.execl(sys.executable, sys.executable, *sys.argv)

reset_btn = tk.Button(left_frame, text='Restart', font=MODERN_FONT, bg=INACTIVE_GREY, fg="#fff", activebackground=INACTIVE_GREY, bd=0, relief="flat", padx=18, pady=12, command=reset_app, state='disabled', cursor="hand2")
reset_btn.grid(row=3, column=0, sticky="ew", padx=30, pady=(8, 10))

# Only apply hover if active
reset_btn.bind("<Enter>", lambda e: reset_btn.config(bg=current_theme["button_hover"]) if reset_btn['state']=='normal' else None)
reset_btn.bind("<Leave>", lambda e: reset_btn.config(bg=current_theme["button_bg"]) if reset_btn['state']=='normal' else None)

def update_reset_btn_state(active):
    if active:
        reset_btn.config(state='normal', bg=current_theme["button_bg"], fg=current_theme["button_fg"], activebackground=current_theme["button_hover"])
    else:
        reset_btn.config(state='disabled', bg=INACTIVE_GREY, fg="#fff", activebackground=INACTIVE_GREY)

# Initial preview image
try:
    ri = PIL.Image.open('./images/rice.png')
    ri = ri.resize(size, PIL.Image.Resampling.LANCZOS)
    sad_img = ImageTk.PhotoImage(ri)
    img_box_width = 600
    img_box_height = 300
    preview_frame = tk.Frame(right_frame, width=img_box_width, height=img_box_height, bg=LIGHT["bg"])
    preview_frame.place(x=60, y=80)
    preview_frame.is_img_frame = True
    preview = tk.Label(preview_frame, image=sad_img, bg=LIGHT["bg"])
    preview.imgtk = sad_img
    preview.place(relx=0.5, rely=0.5, anchor="center")
except:
    pass

windo.mainloop()