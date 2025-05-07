import tkinter as tk
import tkinter.messagebox as mbox

def display_message(text):
    mbox.showinfo("Message", text)

root = tk.Tk()
root.title("Notes")
root.update()
paned_window = tk.PanedWindow(orient=tk.HORIZONTAL, showhandle=True, height=800, width=600)
paned_window.pack(fill=tk.BOTH, expand=1)

left_frame = tk.Frame(paned_window, bg="lightblue", width=150)
left_frame.pack_propagate(False)
right_frame = tk.Frame(paned_window, bg="lightgreen")
right_frame.pack_propagate(False)

button_left = tk.Button(left_frame, text="Left Button", command=lambda: display_message("Left Button Clicked"))
button_left.pack(pady=20)

text_input_right = tk.Text(right_frame, height=root.winfo_height())
text_input_right.pack(pady=20)

paned_window.add(left_frame)
paned_window.add(right_frame)

root.mainloop()