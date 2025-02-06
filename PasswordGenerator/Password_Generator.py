import random
import string
import tkinter as tk
from tkinter import ttk

def generate_password(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def update_password():
    length = length_var.get()
    password = generate_password(length)
    password_var.set(password)

def toggle_theme():
    if theme_var.get() == "Dark":
        root.configure(bg="#2E2E2E")
        style.configure("TLabel", background="#2E2E2E", foreground="white")
        style.configure("TButton", background="#555555", foreground="white")
    else:
        root.configure(bg="white")
        style.configure("TLabel", background="white", foreground="black")
        style.configure("TButton", background="#DDDDDD", foreground="black")

def main():
    global root, length_var, password_var, theme_var, style
    
    root = tk.Tk()
    root.title("Password Generator")
    root.geometry("300x250")
    
    style = ttk.Style()
    
    
    
    ttk.Label(root, text="Select Password Length:").pack(pady=5)
    length_var = tk.IntVar(value=8)
    length_slider = ttk.Scale(root, from_=4, to=32, orient='horizontal', variable=length_var, command=lambda e: length_label.config(text=f"Length: {int(length_var.get())}"))
    length_slider.pack()
    
    length_label = ttk.Label(root, text=f"Length: {length_var.get()}")
    length_label.pack(pady=5)
    
    generate_button = ttk.Button(root, text="Generate Password", command=update_password)
    generate_button.pack(pady=10)
    
    password_var = tk.StringVar()
    password_entry = ttk.Entry(root, textvariable=password_var, state='readonly', width=30)
    password_entry.pack(pady=5)
    
    theme_var = tk.StringVar(value="Light")
    ttk.Label(root, text="Select Theme:").pack(pady=5)
    theme_menu = ttk.Combobox(root, textvariable=theme_var, values=["Light", "Dark"], state="readonly")
    theme_menu.pack()
    theme_menu.bind("<<ComboboxSelected>>", lambda e: toggle_theme())
    toggle_theme()
    
    root.mainloop()
    
if __name__ == "__main__":
    main()
