import tkinter as tk
from tkinter import messagebox
import sys
import json
import os

def submit():
    name = entry_name.get()
    email = entry_email.get()
    if not name or not email:
        messagebox.showerror("Missing info", "Please fill in all fields.")
    else:
        data = {"name": name, "email": email}
        with open("user_input.json", "w") as f:
            json.dump(data, f)
        messagebox.showinfo("Submitted", f"Thanks {name}!")
        root.quit()

root = tk.Tk()
root.title("User Info")

tk.Label(root, text="Name").grid(row=0, column=0)
tk.Label(root, text="Email").grid(row=1, column=0)

entry_name = tk.Entry(root)
entry_email = tk.Entry(root)

entry_name.grid(row=0, column=1)
entry_email.grid(row=1, column=1)

tk.Button(root, text="Submit", command=submit).grid(row=2, columnspan=2)

root.mainloop()
