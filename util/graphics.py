import tkinter as tk
import tkinter.messagebox as mbox
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class NotesApp:
    def __init__(self, default_path="files", extension='.md'):
        self.root = tk.Tk()
        self.root.title("Notes")
        self.root.geometry("800x600")  # Set initial size
        self.default_path = default_path
        self.extension = extension

        # Create and use a directory for note files
        self.notes_dir = Path("data")
        self.notes_dir.mkdir(parents=True, exist_ok=True)  # creates 'data/' if missing
        self.filename = self.notes_dir / "notes.md"         # saves to data/notes.md


        self.setup_ui()

    def setup_ui(self):
        paned_window = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, showhandle=True)
        paned_window.pack(fill=tk.BOTH, expand=1)

        # Left Panel
        self.left_frame = tk.Frame(paned_window, bg="lightblue", width=150)
        self.left_frame.pack_propagate(False)

        button_left = tk.Button(self.left_frame, text="Left Button", command=self.on_left_button)
        button_left.pack(pady=20)

        # Right Panel
        self.right_frame = tk.Frame(paned_window, bg="lightgreen")
        self.right_frame.pack_propagate(False)

        self.text_input = tk.Text(self.right_frame)
        self.text_input.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.button_right = tk.Button(self.right_frame, text="Right Button", command=self.on_right_button)
        self.button_right.pack()

        paned_window.add(self.left_frame)
        paned_window.add(self.right_frame)

    def on_left_button(self):
        mbox.showinfo("Message", "Left Button Clicked")

    def on_right_button(self):
        logger.debug("DEBUG save")
        logger.info(self.text_input.get("1.0","end-1c"))
        if self.filename:
            self.save_to_file()
        else:
            pass #append

    def save_to_file(self):
        with self.filename.open('w') as file:
            file.write(self.text_input.get("1.0","end-1c"))

    def run(self):
        self.root.mainloop()

    