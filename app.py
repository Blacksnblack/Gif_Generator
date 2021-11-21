import time
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from gif_generator import Generator
from os import path
from PIL import ImageTk


def error_message(message):
    showinfo(title='Error', message=message)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # configure the root window
        self.title('Gif Generator')
        # self.geometry('400x600')

        self.filepath, self.generator, self.images, self.initial_time = None, None, None, None
        # self.change_file()
        print(self.filepath)
        self.image_index = 0

        self.Width = tk.StringVar()
        self.Width.set("300")
        self.Height = tk.StringVar()
        self.Height.set("300")

        # Change File Button
        self.change_file_frame = tk.Frame(self)
        self.change_file_frame.pack()
        self.change_file_button = tk.Button(self.change_file_frame, text="Change File")
        self.change_file_button['command'] = self.change_file
        self.change_file_button.pack()

        # Image
        self.image_frame = tk.Frame(self, highlightbackground="black", highlightthickness=1)
        self.image_frame.pack()
        self.canvas = tk.Canvas(self.image_frame, width=300, height=300)
        self.canvas.pack(padx=10, pady=10)
        if self.images and len(self.images) > 0:
            self.current_image = ImageTk.PhotoImage(self.images[0])
            self.canvas.create_image(0, 0, image=self.current_image)

        # Width Input
        self.width_frame = ttk.Frame(self)
        self.width_frame.pack()
        self.width_frame_label = ttk.Label(self.width_frame, text="Max Width: ")
        self.width_frame_label.pack(side="left")
        self.width_frame_entry = tk.Entry(self.width_frame, text="#", textvariable=self.Width)
        self.width_frame_entry.pack(side="left")
        self.width_frame_entry.focus_force()

        # Height Input
        self.height_frame = ttk.Frame(self)
        self.height_frame.pack()
        self.height_frame_label = ttk.Label(self.height_frame, text="Max Height: ")
        self.height_frame_label.pack(side="left")
        self.height_frame_entry = tk.Entry(self.height_frame, text="#", textvariable=self.Height)
        self.height_frame_entry.pack(side="left")

        # Slider
        self.slider_frame = ttk.Frame(self)
        self.slider_frame.pack()
        self.slider_label = ttk.Label(self.slider_frame, text="Time (Ms): ")
        self.slider_label.pack(side="left")
        self.slider = tk.Scale(self.slider_frame, from_=0, to=200, orient=tk.HORIZONTAL)
        self.slider.set(100)
        self.slider.pack(side="left")

        # Apply Buttons
        self.apply_frame = ttk.Frame(self)
        self.apply_frame.pack()
        self.apply_button = ttk.Button(self.apply_frame, text='Apply')
        self.apply_button['command'] = self.apply_button_clicked
        self.apply_button["state"] = "disabled"
        self.apply_button.pack(side="left")

        self.save_button = ttk.Button(self.apply_frame, text='Save')
        self.save_button['command'] = self.save_button_clicked
        self.save_button["state"] = "disabled"
        self.save_button.pack(side="right")

    def update_image(self):
        if not self.images or len(self.images) <= 0:
            return
        self.image_index += 1
        if self.image_index >= len(self.images):
            self.image_index = 0
        self.current_image = ImageTk.PhotoImage(self.images[self.image_index])

        self.canvas.create_image(int(int(self.canvas['width']) / 2), int(int(self.canvas['height']) / 2),
                                 image=self.current_image, anchor=tk.CENTER)
        self.canvas.update()

    def change_file(self):
        valid = False
        while not valid:
            self.filepath = fd.askdirectory(title="Select a File")
            if path.exists(self.filepath):
                valid = True
            else:
                error_message("Invalid Path.")
        if self.generator:
            self.generator.file_path = self.filepath
        else:
            self.generator = Generator(self.filepath)
        self.images = self.generator.get_images()
        self.apply_button["state"] = "normal"

    def enable_apply_button(self):
        self.apply_button["state"] = "normal"

    def enable_save_button(self):
        self.save_button["state"] = "normal"

    def save_button_clicked(self):
        filepath = self.generator.generate_gif()
        showinfo(title='Gif Saved!', message=f"The Gif was saved in the location of: {filepath}")

    def apply_button_clicked(self):
        height_text = self.Height.get()
        width_text = self.Width.get()
        if len(height_text) > 0 and len(width_text) > 0:
            if height_text.isnumeric() and width_text.isnumeric():
                max_size = max(int(self.width_frame_entry.get()), int(self.height_frame_entry.get()))
                if not self.generator:
                    self.generator = Generator(self.filepath, int(self.slider.get()), max_size)
                else:
                    self.generator.MAX_SIZE = max_size
                    self.generator.duration = int(self.slider.get())
                    self.generator.original_size = False
                self.images = self.generator.get_images()
                self.canvas['width'] = int(width_text)
                self.canvas['height'] = int(height_text)
                self.save_button['state'] = 'normal'
            else:
                error_message('Width/Height Values must be integers.')
                self.width_frame_entry.delete(0, "end")
                self.height_frame_entry.delete(0, "end")
        else:
            self.generator.original_size = True
            self.images = self.generator.get_images()
            self.canvas['width'] = int(self.images[0].width)
            self.canvas['height'] = int(self.images[0].height)
            # error_message("Width/Height Fields must contain numeric values.")
        can_wid = int(self.canvas['width'])
        can_hei = int(self.canvas['height'])
        if can_wid > 1500:
            self.canvas['width'] = 1500
            self.generator.MAX_SIZE = max(can_hei, can_wid)

        if can_hei > 700:
            self.canvas['height'] = 700
            self.generator.MAX_SIZE = max(can_hei, can_wid)
        self.canvas.update()

    def mainloop(self, n=0):
        initial_time = time.time_ns()
        while True:
            self.update()
            self.update_idletasks()
            new_time = time.time_ns()
            delta_time = (new_time - initial_time) / 1_000_000  # in milliseconds
            if self.slider.get() <= delta_time:
                initial_time = new_time
                self.update_image()


if __name__ == "__main__":
    app = App()
    app.mainloop()
