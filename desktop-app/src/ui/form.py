import ttkbootstrap as ttk
import tkinter as tk
from tkinter import messagebox
import re
from tkinter import StringVar
from ui.islem_tanimlari import IslemTanimlariWindow

class DataEntryForm(ttk.Frame):
    def __init__(self, parent, table_controller):
        super().__init__(parent)
        self.table_controller = table_controller
        self.create_widgets()
        self.load_islem_tipleri()

    def create_widgets(self):
        self.tc_kimlik_no_label = ttk.Label(self, text="T.C. Kimlik Numarası:")
        self.tc_kimlik_no_label.grid(row=0, column=0, padx=5, pady=5)
        self.tc_kimlik_no_entry = ttk.Entry(self)
        self.tc_kimlik_no_entry.grid(row=0, column=1, padx=5, pady=5)

        self.isim_soyisim_label = ttk.Label(self, text="İsim Soyisim:")
        self.isim_soyisim_label.grid(row=1, column=0, padx=5, pady=5)
        self.isim_soyisim_entry = ttk.Entry(self)
        self.isim_soyisim_entry.grid(row=1, column=1, padx=5, pady=5)

        self.islem_tarihi_label = ttk.Label(self, text="İşlem Tarihi:")
        self.islem_tarihi_label.grid(row=0, column=2, padx=5, pady=5)
        self.islem_tarihi_entry = ttk.DateEntry(self)
        self.islem_tarihi_entry.grid(row=0, column=3, padx=5, pady=5)

        self.islem_tipi_label = ttk.Label(self, text="İşlem Tipi:")
        self.islem_tipi_label.grid(row=1, column=2, padx=5, pady=5)
        self.islem_tipi_var = StringVar()
        self.islem_tipi_combobox = ttk.Combobox(self, textvariable=self.islem_tipi_var)
        self.islem_tipi_combobox.grid(row=1, column=3, padx=5, pady=5)

        self.islem_tipi_button = ttk.Button(self, text="⚙", command=self.open_islem_tipi_editor)
        self.islem_tipi_button.grid(row=1, column=4, padx=5, pady=5)

        self.aciklama_label = ttk.Label(self, text="Açıklama:")
        self.aciklama_label.grid(row=2, column=0, padx=5, pady=5)
        self.aciklama_entry = ttk.Entry(self)
        self.aciklama_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        self.kaydet_button = ttk.Button(self, text="Kaydet", command=self.submit_form)
        self.kaydet_button.grid(row=2, column=4, padx=5, pady=5)

    def submit_form(self):
        tc_kimlik = self.tc_kimlik_no_entry.get()
        isim_soyisim = self.isim_soyisim_entry.get()
        islem_tarihi = self.islem_tarihi_entry.entry.get()  # Use entry.get() for DateEntry
        islem_tipi = self.islem_tipi_var.get()
        aciklama = self.aciklama_entry.get()
        
        if self.validate_form(tc_kimlik, isim_soyisim, islem_tarihi, islem_tipi):
            message = self.table_controller.submit_form(tc_kimlik, isim_soyisim, islem_tarihi, islem_tipi, aciklama)
            messagebox.showinfo("Başarılı", message)
            self.clear_form()
        
    def clear_form(self):
        self.tc_kimlik_no_entry.delete(0, 'end')
        self.isim_soyisim_entry.delete(0, 'end')
        self.aciklama_entry.delete(0, 'end')
        self.islem_tipi_var.set('')

    def open_islem_tipi_editor(self):
        editor = IslemTanimlariWindow(self, self.table_controller)
        editor.wait_window()  # Wait for the window to close
        self.load_islem_tipleri()  # Reload işlem tipleri after editing

    def load_islem_tipleri(self):
        # Get işlem tipleri from database and update combobox
        islem_tipleri = self.table_controller.get_islem_tipleri_values()
        self.islem_tipi_combobox['values'] = islem_tipleri

    def validate_form(self, tc, name, date, type_):
        if not re.match(r'^\d{11}$', tc):
            messagebox.showerror("Hata", "T.C. Kimlik Numarası 11 haneli olmalıdır.")
            return False
        if not name:
            messagebox.showerror("Hata", "İsim Soyisim alanı zorunludur.")
            return False
        if not date:
            messagebox.showerror("Hata", "İşlem Tarihi alanı zorunludur.")
            return False
        if not type_:
            messagebox.showerror("Hata", "İşlem Tipi alanı zorunludur.")
            return False
        return True

if __name__ == "__main__":
    root = tk.Tk()
    app = DataEntryForm(root)
    root.mainloop()