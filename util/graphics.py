import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mbox
import os
from pathlib import Path
import logging
from datetime import datetime
logger = logging.getLogger(__name__)


class NotesApp:
    def __init__(self, default_path="files", extension='.md'):
        self.root = tk.Tk()
        self.root.title("Notes")
        self.root.geometry("800x600")  # Set initial size
        self.default_path = default_path
        self.extension = extension
        self.editting = False

        self.notes_dir = Path("data")
        self.notes_dir.mkdir(parents=True, exist_ok=True)  # creates 'data/' if missing
        # self.filename = self.notes_dir / "notes.md"         # saves to data/notes.md
        self.filename = None # only used if editting

        self.setup_ui()

    def setup_ui(self):
        paned_window = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, showhandle=True)
        paned_window.pack(fill=tk.BOTH, expand=1)

        # left panel
        self.treeview = ttk.Treeview()
        self.treeview.bind('<<TreeviewSelect>>', self.on_file_selected)

        self.note_tree_view()
        self.left_frame = self.treeview
        self.left_frame.pack()


        # Right Panel
        self.right_frame = tk.Frame(paned_window, bg="lightgreen")
        self.right_frame.pack_propagate(False)
        
        self.new_button = tk.Button(self.right_frame, text="New", command=self.on_new_file)
        self.new_button.pack()
        self.text_input = tk.Text(self.right_frame)
        self.text_input.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.button_right = tk.Button(self.right_frame, text="Save", command=self.on_right_button)
        self.button_right.pack()

        #add to root
        paned_window.add(self.left_frame)
        paned_window.add(self.right_frame)
    def run(self):
        self.root.mainloop()
    def on_new_file(self):
        logger.info(f"Save and new_file")
        self.on_right_button() #save path
        self.clear_input_field() #reset input, editting, filename
        
    def clear_input_field(self):
        self.text_input.delete("1.0", tk.END) #delete contents
        self.editting = False
        self.filename = None

    def refresh_tree_view(self):
        selected_items = self.treeview.selection()
        if selected_items:
            self.treeview.selection_remove(selected_items)
        for item in self.treeview.get_children():
            self.treeview.delete(item)  
        self.note_tree_view()

    def note_tree_view(self):
        data_root = "data"
        
        all_items = os.listdir(data_root)

        folders = [f for f in all_items if os.path.isdir(os.path.join("data", f))]
        
        for folder in folders:
            folder_path = os.path.join(data_root, folder)
            item_f = self.treeview.insert("", tk.END, text=folder)
            
            files = [
                file for file in os.listdir(folder_path)
                if os.path.isfile(os.path.join(folder_path, file)) and file.endswith(".md")
            ]
            logger.info(files)
            
            files = sorted(files, key=lambda f: int(f.split(".")[0]), reverse=True) #save as every file has to have .md already
            
            for note in files:
                self.treeview.insert(item_f, tk.END, text=note) #files (with .md)
        
        
    def on_file_selected(self, event):
        
        selection = self.treeview.selection()
        if not selection:
            return

        selected_item_id = selection[0]
        # selected_item_id = self.treeview.selection()[0]
        item_data = self.treeview.item(selected_item_id)

        label = item_data["text"]
        parent_id = self.treeview.parent(selected_item_id)
        parent_data = self.treeview.item(parent_id)
        folder = parent_data["text"] if parent_id else None

        logger.info(f"Selected item: {label}")
        logger.info(f"From folder: {folder}")

        #load file 
        if folder and label.endswith('.md'):
            self.load_note_from_file(os.path.join("data", folder, label))
        
    def load_note_from_file(self, filename):
        try:
            logger.info(f"Loading {filename}...")
            with open(filename, 'r') as file:
                contents = file.read()
            self.text_input.delete("1.0", tk.END)
            self.text_input.insert("1.0", contents)
            self.editting = True
            self.filename = filename
            self.right_frame.config(bg="lightyellow")
        except Exception as e:
            logger.error(f"Failed to load file due to: {e}")

    def on_left_button(self):
        mbox.showinfo("Message", "Left Button Clicked")

    def on_right_button(self):
        logger.debug("DEBUG save")
        logger.info(self.text_input.get("1.0","end-1c"))
        if not self.editting:
            #todays folder
            self.notes_dir #data
            today = datetime.now().strftime('%Y.%m.%d')
            today_path = Path(f'data/{today}')
            today_path.mkdir(parents=True, exist_ok=True) #creates folder
            current_items = os.listdir(today_path)
            files = [f for f in current_items if os.path.isfile(os.path.join(today_path, f)) and f.endswith(".md")]
            new_file_name = str(len(files) + 1) + '.md' #3
            self.save_to_file(today_path / new_file_name)
            
            #we have created a file we will now set editting true and set filename
            self.editting = True
            self.filename = today_path / new_file_name
        else:
            self.save_to_file() #this is now a edit

        self.refresh_tree_view()

    def save_to_file(self, file_name_path = None):
        if not self.filename: #only on new file
            with file_name_path.open('w') as file:
                file.write(self.text_input.get("1.0","end-1c"))
            
            self.load_note_from_file(file_name_path)
        else:
            logger.info
            with open(self.filename, 'w') as file:
                file.write(self.text_input.get("1.0","end-1c"))


    