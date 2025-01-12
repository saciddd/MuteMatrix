from tkinter import StringVar, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import MessageDialog
import sqlite3
import platform
from datetime import datetime

class DataTable(ttk.Frame):
    def __init__(self, parent, table_controller=None):
        super().__init__(parent)
        self.table_controller = table_controller
        self.sort_column = None
        self.sort_reverse = False
        self.create_widgets()
        self.create_context_menu()

    def create_context_menu(self):
        self.context_menu = ttk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Düzenle", command=self.edit_record)
        self.context_menu.add_command(label="Sil", command=self.delete_record)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Yenile", command=self.refresh_table)
        
        self.table.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        item = self.table.identify_row(event.y)
        if item:
            self.table.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def create_widgets(self):
        # Create scrollbars
        y_scrollbar = ttk.Scrollbar(self)
        y_scrollbar.grid(row=0, column=1, sticky="ns")
        x_scrollbar = ttk.Scrollbar(self, orient="horizontal")
        x_scrollbar.grid(row=1, column=0, sticky="ew")

        # Create table with correct columns
        self.table = ttk.Treeview(self, 
            columns=("id", "tc_no", "name", "date", "operation_type", "description", "timestamp", "computer_name"),
            show='headings',
            yscrollcommand=y_scrollbar.set,
            xscrollcommand=x_scrollbar.set)
        
        # Configure scrollbars
        y_scrollbar.configure(command=self.table.yview)
        x_scrollbar.configure(command=self.table.xview)
        
        # Setup column headings with sorting
        columns = [
            ("id", "ID", 50),
            ("tc_no", "T.C. Kimlik Numarası", 120),
            ("name", "İsim Soyisim", 150),
            ("date", "İşlem Tarihi", 100),
            ("operation_type", "İşlem Tipi", 120),
            ("description", "Açıklama", 200),
            ("timestamp", "Kayıt Zamanı", 120),
            ("computer_name", "Bilgisayar Adı", 120)
        ]
        
        for col, heading, width in columns:
            self.table.heading(col, text=heading,
                             command=lambda c=col: self.sort_by_column(c))
            self.table.column(col, width=width)

        self.table.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.setup_table()

    def load_data(self, data):
        for row in data:
            self.table.insert("", "end", values=row)

    def on_info_icon_click(self, event):
        item = self.table.identify_row(event.y)
        if item:
            record_time = self.get_record_time(item)
            computer_name = platform.node()
            MessageDialog.show_info("Record Info", f"Record Time: {record_time}\nSaved By: {computer_name}")

    def get_record_time(self, item):
        # Assuming the record time is stored in the database and can be fetched
        # This is a placeholder for actual database retrieval logic
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Replace with actual record time retrieval logic

    def color_rows(self, transaction_type):
        color_map = {
            "Ücretsiz İzin Ayrılış": "primary",
            "Askerlik": "danger",
            # Add more mappings as needed
        }
        return color_map.get(transaction_type, "default")  # Default color if not found

    def display_data(self, data):
        self.table.delete(*self.table.get_children())
        for record in data:
            self.table.insert("", "end", values=record, tags=(record[4],))

    def sort_by_column(self, col):
        if self.sort_column == col:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = col
            self.sort_reverse = False
        
        items = [(self.table.item(item)["values"], item) for item in self.table.get_children("")]
        col_index = list(self.table["columns"]).index(col)
        
        items.sort(key=lambda x: str(x[0][col_index]).lower(), reverse=self.sort_reverse)
        
        for idx, (_, item) in enumerate(items):
            self.table.move(item, "", idx)

    def setup_table(self):
        # Only configure colors if table_controller is available
        if self.table_controller:
            try:
                islem_tipleri = self.table_controller.get_islem_tipleri()
                for islem_tipi, color in islem_tipleri:
                    background_color = self.get_color_code(color)
                    self.table.tag_configure(islem_tipi, background=f'#{background_color}')
            except:
                pass  # Skip color configuration if there's an error
    
    def get_color_code(self, bootstyle):
        color_map = {
            "default": "ffffff",
            "primary": "cfe2ff",
            "secondary": "e2e3e5",
            "success": "d4edda",
            "danger": "efb0b6",
            "warning": "fff3cd",
            "info": "cff4fc"
        }
        return color_map.get(bootstyle, "ffffff")

    def edit_record(self):
        selected = self.table.selection()
        if selected:
            item = selected[0]
            values = self.table.item(item)['values']
            if values and self.table_controller:
                # Create edit dialog
                edit_window = ttk.Toplevel(self)
                edit_window.title("Kaydı Düzenle")
                edit_window.geometry("500x400")
                
                # Create form fields
                fields = [
                    ("T.C. Kimlik No:", values[1]),
                    ("İsim Soyisim:", values[2]),
                    ("İşlem Tarihi:", values[3]),
                    ("İşlem Tipi:", values[4]),
                    ("Açıklama:", values[5])
                ]
                
                entries = {}
                for i, (label, value) in enumerate(fields):
                    ttk.Label(edit_window, text=label).grid(row=i, column=0, padx=5, pady=5)
                    if label == "İşlem Tipi:":
                        var = StringVar(value=value)
                        entry = ttk.Combobox(edit_window, textvariable=var, 
                                           values=self.table_controller.get_islem_tipleri_values())
                        entries[label] = var
                    else:
                        entry = ttk.Entry(edit_window)
                        entry.insert(0, value)
                        entries[label] = entry
                    entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")

                def save_changes():
                    updated_values = [
                        entries["T.C. Kimlik No:"].get(),
                        entries["İsim Soyisim:"].get(),
                        entries["İşlem Tarihi:"].get(),
                        entries["İşlem Tipi:"].get(),
                        entries["Açıklama:"].get()
                    ]
                    
                    success = self.table_controller.update_record(values[0], *updated_values)
                    if success:
                        messagebox.showinfo("Başarılı", "Kayıt güncellendi.")
                        edit_window.destroy()
                        self.refresh_table()
                    else:
                        messagebox.showerror("Hata", "Kayıt güncellenirken bir hata oluştu.")

                ttk.Button(edit_window, text="Kaydet", command=save_changes).grid(
                    row=len(fields), column=0, columnspan=2, pady=20)

    def delete_record(self):
        selected = self.table.selection()
        if selected:
            item = selected[0]
            values = self.table.item(item)['values']
            if values and self.table_controller:
                if messagebox.askyesno("Onay", "Bu kaydı silmek istediğinizden emin misiniz?"):
                    if self.table_controller.delete_record(values[0]):
                        messagebox.showinfo("Başarılı", "Kayıt silindi.")
                        self.refresh_table()
                    else:
                        messagebox.showerror("Hata", "Kayıt silinirken bir hata oluştu.")

    def refresh_table(self):
        if self.table_controller:
            self.table_controller.load_data()