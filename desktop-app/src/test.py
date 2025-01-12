from tkinter import *
import ttkbootstrap as ttk

root = ttk.Window(themename='superhero')

root.title("Test Sayfası")
root.geometry("800x600")

label_date_entry = ttk.Label(root, text="Tarih Seçiniz:")
label_date_entry.pack()
date_entry = ttk.DateEntry(root, bootstyle="danger")
date_entry.pack()

root.mainloop()