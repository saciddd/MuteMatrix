import ttkbootstrap as ttk
import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime

class DatePicker(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.selected_date = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        self.date_entry = ttk.Entry(self, textvariable=self.selected_date)
        self.date_entry.grid(row=0, column=0, padx=(0, 2))

        self.calendar_button = ttk.Button(self, text="📅", width=3, command=self.show_calendar)
        self.calendar_button.grid(row=0, column=1)

    def show_calendar(self):
        top = tk.Toplevel(self)
        top.geometry("300x250")
        top.resizable(False, False)
        
        cal = Calendar(top, selectmode='day', date_pattern='yyyy-mm-dd')
        cal.pack(expand=True, fill='both')
        
        def set_date():
            self.selected_date.set(cal.get_date())
            top.destroy()
        
        ttk.Button(top, text="Seç", command=set_date).pack()

    def get(self):
        return self.selected_date.get()

    def set(self, date):
        self.selected_date.set(date)
