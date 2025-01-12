from tkinter import *
import ttkbootstrap as ttk
from ui.table import DataTable
from ui.filter import FilterFrame
from ui.form import DataEntryForm
from controllers.table_controller import TableController

def main():
    root = ttk.Window(themename='sandstone')
    root.title("MuteMatrix")
    root.geometry("1024x768")
    root.iconbitmap("desktop-app/src/ui/MuteMatrix.ico")

    # Theme selector at the very top
    theme_frame = ttk.Frame(root)
    theme_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
    
    theme_var = StringVar(value='sandstone')
    theme_combo = ttk.Combobox(theme_frame, textvariable=theme_var, values=[
        'cosmo', 'flatly', 'litera', 'minty', 'lumen', 'sandstone', 
        'yeti', 'pulse', 'united', 'morph', 'journal', 'darkly', 'cyborg', 'superhero'
    ])
    theme_combo.pack(side="right", padx=5)
    ttk.Label(theme_frame, text="Tema Seçiniz:").pack(side="right", padx=5)
    
    # First separator below theme selector
    ttk.Separator(root, orient="horizontal").grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

    # Data entry form
    data_entry_frame = ttk.Frame(root)
    data_entry_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    # Separator below data entry form
    ttk.Separator(root, orient="horizontal").grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
    
    # Filter and table frames
    filter_frame = ttk.Frame(root)
    filter_frame.grid(row=4, column=0, padx=10, pady=5, sticky="ew")
    
    table_frame = ttk.Frame(root)
    table_frame.grid(row=5, column=0, padx=10, pady=5, sticky="nsew")

    # Footer separator and copyright
    ttk.Separator(root, orient="horizontal").grid(row=6, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
    
    footer_label = ttk.Label(root, text="MuteMatrix v1 © Sacit Polat 2025")
    footer_label.grid(row=7, column=0, columnspan=2, pady=5)

    # Initialize components
    data_table = DataTable(table_frame)
    table_controller = TableController(data_table)
    data_table.table_controller = table_controller
    data_table.setup_table()
    data_table.pack(fill="both", expand=True)
    
    data_entry_form = DataEntryForm(data_entry_frame, table_controller)
    data_entry_form.pack(fill="x")
    
    data_filter = FilterFrame(filter_frame, table_controller)
    data_filter.pack(fill="x")
    
    # Configure grid weights
    root.grid_rowconfigure(5, weight=1)  # Make table row expandable
    root.grid_columnconfigure(0, weight=1)

    def change_theme(event):
        root.style.theme_use(theme_var.get())
    
    theme_combo.bind('<<ComboboxSelected>>', change_theme)

    root.mainloop()

if __name__ == "__main__":
    main()