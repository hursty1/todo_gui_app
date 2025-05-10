import tkinter as tk



class MenuBar:
    def __init__(self, root, on_save=None, on_exit=None, on_new=None):
        self.menubar = tk.Menu(root)

        # File menu
        file_menu = tk.Menu(self.menubar, tearoff=0)
        file_menu.add_command(label="New",accelerator="Ctrl+N", command=on_new)
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=on_save)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=on_exit or root.quit)
        self.menubar.add_cascade(label="File", menu=file_menu)

        # Help menu
        help_menu = tk.Menu(self.menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        self.menubar.add_cascade(label="Help", menu=help_menu)

        # Attach to root
        root.config(menu=self.menubar)

    def show_about(self):
        tk.messagebox.showinfo("About", "NotesApp v0.1") 