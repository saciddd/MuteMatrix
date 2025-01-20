from tkinter import *
import ttkbootstrap as ttk
from ui.table import DataTable
from ui.filter import FilterFrame
from ui.form import DataEntryForm
from controllers.table_controller import TableController
from models.database import Database
from controllers.sendika_controller import SendikaController
from ui.sendika_form import SendikaForm
from ui.sendika_table import SendikaTable

def main():
    root = ttk.Window(themename='sandstone')
    root.title("MuteMatrix")
    root.geometry("1024x768")
    
    # Theme selector at the very top
    theme_frame = ttk.Frame(root)
    theme_frame.pack(fill="x", padx=10, pady=5)
    
    theme_var = StringVar(value='sandstone')
    theme_combo = ttk.Combobox(theme_frame, textvariable=theme_var, values=[
        'cosmo', 'flatly', 'litera', 'minty', 'lumen', 'sandstone', 
        'yeti', 'pulse', 'united', 'morph', 'journal', 'darkly', 'cyborg', 'superhero'
    ])
    theme_combo.pack(side="right", padx=5)
    ttk.Label(theme_frame, text="Tema Seçiniz:").pack(side="right", padx=5)
    
    # Create notebook for tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=5)
    
    # Initialize controllers and database
    database = Database()
    
    # Tab 1: Personel İşlemleri
    personel_tab = ttk.Frame(notebook)
    notebook.add(personel_tab, text="Personel İşlemleri")
    
    # Create table and controller first
    table_frame = ttk.Frame(personel_tab)
    data_table = DataTable(table_frame)
    table_controller = TableController(data_table)  # Create controller before using it
    data_table.table_controller = table_controller
    data_table.setup_table()
    
    # Now create form
    data_entry_form = DataEntryForm(personel_tab, table_controller)
    data_entry_form.pack(fill="x", padx=5, pady=5)
    
    # First separator
    ttk.Separator(personel_tab, orient="horizontal").pack(fill="x", padx=5, pady=5)
    
    # Filter frame with search and export
    filter_frame = FilterFrame(personel_tab, table_controller)
    filter_frame.pack(fill="x", padx=5)
    
    # Second separator
    ttk.Separator(personel_tab, orient="horizontal").pack(fill="x", padx=5, pady=5)
    
    # Finally pack the table
    table_frame.pack(fill="both", expand=True, padx=5, pady=5)
    data_table.pack(fill="both", expand=True)
    
    # Load initial data for personnel records
    table_controller.load_data()
    
    # Tab 2: Sendika İşlemleri
    sendika_tab = ttk.Frame(notebook)
    notebook.add(sendika_tab, text="Sendika İşlemleri")
    
    # Initialize sendika components
    sendika_controller = SendikaController(database)
    
    # Initialize sendika tab components
    sendika_form = SendikaForm(sendika_tab, sendika_controller)
    sendika_form.pack(fill="x", padx=5, pady=5)
    
    ttk.Separator(sendika_tab, orient="horizontal").pack(fill="x", padx=5, pady=5)
    
    sendika_table = SendikaTable(sendika_tab, sendika_controller)
    sendika_table.pack(fill="both", expand=True, padx=5, pady=5)
    
    # Load initial data for sendika records
    sendika_table.show_all_records()
    
    # Footer
    ttk.Separator(root, orient="horizontal").pack(fill="x", padx=10, pady=5)
    ttk.Label(root, text="MuteMatrix v1 © Sacit Polat 2025").pack(pady=5)
    
    def change_theme(event):
        root.style.theme_use(theme_var.get())
    
    theme_combo.bind('<<ComboboxSelected>>', change_theme)
    root.mainloop()

if __name__ == "__main__":
    main()
