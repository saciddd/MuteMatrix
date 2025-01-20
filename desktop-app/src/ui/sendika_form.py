import ttkbootstrap as ttk
from tkinter import StringVar, messagebox
from tkcalendar import DateEntry
from datetime import datetime
import platform
from ui.sendika_tanimlari import SendikaTanimlariWindow

class SendikaForm(ttk.Frame):
    def __init__(self, parent, sendika_controller):
        super().__init__(parent)
        self.sendika_controller = sendika_controller
        self.islem_tipi_var = StringVar(value="Üyelik")
        self.create_widgets()
        self.load_sendika_tanimlari()

    def create_widgets(self):
        # Form alanları
        form_frame = ttk.LabelFrame(self, text="Sendika İşlem Bilgileri", padding=10)
        form_frame.pack(fill="x", padx=5, pady=5)

        # TC ve İsim
        row1 = ttk.Frame(form_frame)
        row1.pack(fill="x", pady=5)
        
        ttk.Label(row1, text="T.C. Kimlik No:").pack(side="left", padx=5)
        self.tc_entry = ttk.Entry(row1)
        self.tc_entry.pack(side="left", padx=5)
        
        ttk.Label(row1, text="İsim Soyisim:").pack(side="left", padx=5)
        self.isim_entry = ttk.Entry(row1)
        self.isim_entry.pack(side="left", padx=5)

        # Tarih ve Sendika
        row2 = ttk.Frame(form_frame)
        row2.pack(fill="x", pady=5)
        
        ttk.Label(row2, text="İşlem Tarihi:").pack(side="left", padx=5)
        self.tarih_entry = ttk.DateEntry(row2)
        self.tarih_entry.pack(side="left", padx=5)
        
        ttk.Label(row2, text="Sendika:").pack(side="left", padx=5)
        self.sendika_combo = ttk.Combobox(row2, state="readonly")
        self.sendika_combo.pack(side="left", padx=5)
        
        self.sendika_button = ttk.Button(row2, text="⚙", width=3, 
                                       command=self.open_sendika_tanimlari)
        self.sendika_button.pack(side="left")

        # İşlem tipi ve eski sendika
        row3 = ttk.Frame(form_frame)
        row3.pack(fill="x", pady=5)
        
        ttk.Label(row3, text="İşlem Tipi:").pack(side="left", padx=5)
        ttk.Radiobutton(row3, text="Üyelik", variable=self.islem_tipi_var, 
                       value="Üyelik", style="success").pack(side="left", padx=5)
        ttk.Radiobutton(row3, text="Ayrılış", variable=self.islem_tipi_var, 
                       value="Ayrılış", style="danger").pack(side="left", padx=5)

        # Kaydet butonu
        self.kaydet_btn = ttk.Button(row3, text="Kaydet", 
                                   command=self.kaydet, style="primary")
        self.kaydet_btn.pack(side="right", padx=5)

    def open_sendika_tanimlari(self):
        editor = SendikaTanimlariWindow(self.winfo_toplevel(), self.sendika_controller)
        editor.grab_set()  # Bu pencereyi modal yap
        self.wait_window(editor)  # Pencere kapanana kadar bekle
        self.load_sendika_tanimlari()

    def load_sendika_tanimlari(self):
        sendikalar = self.sendika_controller.get_sendika_listesi()
        self.sendika_combo['values'] = sendikalar

    def kaydet(self):
        tc = self.tc_entry.get().strip()
        isim = self.isim_entry.get().strip()
        # Tarihi doğru formatta alalım
        tarih = datetime.strptime(self.tarih_entry.entry.get(), '%d.%m.%Y').strftime('%Y-%m-%d')
        sendika = self.sendika_combo.get()
        islem_tipi = self.islem_tipi_var.get()
        
        if not all([tc, isim, tarih, sendika]):
            messagebox.showerror("Hata", "Tüm alanları doldurunuz!")
            return

        try:
            self.sendika_controller.kaydet_sendika_islem(
                tc, isim, sendika, tarih, islem_tipi,
                platform.node()
            )
            messagebox.showinfo("Başarılı", "Kayıt başarıyla eklendi.")
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Hata", f"Kayıt eklenirken hata oluştu: {str(e)}")

    def clear_form(self):
        self.tc_entry.delete(0, 'end')
        self.isim_entry.delete(0, 'end')
        self.tarih_entry.entry.delete(0, 'end')  # Clear the entry
        self.tarih_entry.entry.insert(0, datetime.now().strftime('%d.%m.%Y'))  # Set current date
        self.sendika_combo.set('')
        self.islem_tipi_var.set('Üyelik')
