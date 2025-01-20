import ttkbootstrap as ttk
from tkinter import messagebox

class IslemTanimlariWindow(ttk.Toplevel):
    def __init__(self, parent, table_controller):
        super().__init__(parent)
        self.table_controller = table_controller
        self.title("İşlem Tanımları")
        self.geometry("500x600")
        #self.iconbitmap("desktop-app/src/ui/MuteMatrix.ico")
        
        self.colors = [
            ("Varsayılan", "default"),
            ("Mavi", "primary"),
            ("Yeşil", "success"),
            ("Kırmızı", "danger"),
            ("Sarı", "warning"),
            ("Turuncu", "warning"),
            ("Mor", "secondary"),
            ("Gri", "info")
        ]
        
        self.create_widgets()
        self.load_islem_tipleri()

    def create_widgets(self):
        # Entry frame with color selection
        entry_frame = ttk.Frame(self)
        entry_frame.pack(pady=10, padx=10, fill="x")

        self.islem_tipi_entry = ttk.Entry(entry_frame)
        self.islem_tipi_entry.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.color_var = ttk.StringVar(value="default")
        self.color_combobox = ttk.Combobox(entry_frame, textvariable=self.color_var, 
                                          values=[color[0] for color in self.colors])
        self.color_combobox.pack(side="left", padx=5)
        
        ttk.Button(entry_frame, text="Ekle", command=self.add_islem_tipi).pack(side="right")

        # Listbox frame with color preview
        list_frame = ttk.Frame(self)
        list_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.islem_tipleri_listbox = ttk.Treeview(list_frame, 
            columns=("islem_tipi", "color"), show="headings")
        self.islem_tipleri_listbox.heading("islem_tipi", text="İşlem Tipi")
        self.islem_tipleri_listbox.heading("color", text="Renk")
        self.islem_tipleri_listbox.pack(fill="both", expand=True)

        # Buttons frame
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10, padx=10, fill="x")

        ttk.Button(button_frame, text="Sil", command=self.delete_islem_tipi).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Kapat", command=self.destroy).pack(side="right", padx=5)

    def load_islem_tipleri(self):
        # Clear existing items
        for item in self.islem_tipleri_listbox.get_children():
            self.islem_tipleri_listbox.delete(item)
            
        # Load from database and insert into listbox
        islem_tipleri = self.table_controller.get_islem_tipleri()
        for islem_tipi, color in islem_tipleri:
            color_name = next((name for name, val in self.colors if val == color), "Varsayılan")
            self.islem_tipleri_listbox.insert("", "end", values=(islem_tipi, color_name))

    def add_islem_tipi(self):
        islem_tipi = self.islem_tipi_entry.get().strip()
        color = dict(self.colors)[self.color_var.get()]
        if islem_tipi:
            self.table_controller.add_islem_tipi(islem_tipi, color)
            self.islem_tipi_entry.delete(0, "end")
            self.color_var.set("default")
            self.load_islem_tipleri()
        else:
            messagebox.showwarning("Uyarı", "İşlem tipi boş olamaz!")

    def delete_islem_tipi(self):
        selected = self.islem_tipleri_listbox.selection()
        if selected:
            islem_tipi = self.islem_tipleri_listbox.item(selected[0])["values"][0]
            if messagebox.askyesno("Onay", f"{islem_tipi} silinecek. Emin misiniz?"):
                self.table_controller.delete_islem_tipi(islem_tipi)
                self.load_islem_tipleri()
