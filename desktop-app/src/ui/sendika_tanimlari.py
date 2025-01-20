import ttkbootstrap as ttk
from tkinter import messagebox

class SendikaTanimlariWindow(ttk.Toplevel):
    def __init__(self, parent, sendika_controller):
        super().__init__(parent)
        self.sendika_controller = sendika_controller
        self.title("Sendika Tanımları")
        self.geometry("400x500")
        
        self.create_widgets()
        self.load_sendika_tanimlari()

    def create_widgets(self):
        # Entry frame
        entry_frame = ttk.Frame(self)
        entry_frame.pack(pady=10, padx=10, fill="x")

        self.sendika_entry = ttk.Entry(entry_frame)
        self.sendika_entry.pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        ttk.Button(entry_frame, text="Ekle", 
                  command=self.add_sendika).pack(side="right")

        # Listbox frame
        list_frame = ttk.Frame(self)
        list_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.sendika_listbox = ttk.Treeview(list_frame, 
            columns=("sendika"), show="headings")
        self.sendika_listbox.heading("sendika", text="Sendika İsmi")
        self.sendika_listbox.pack(fill="both", expand=True)

        # Buttons frame
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10, padx=10, fill="x")

        ttk.Button(button_frame, text="Sil", 
                  command=self.delete_sendika).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Kapat", 
                  command=self.destroy).pack(side="right", padx=5)

    def load_sendika_tanimlari(self):
        for item in self.sendika_listbox.get_children():
            self.sendika_listbox.delete(item)
            
        sendikalar = self.sendika_controller.get_sendika_listesi()
        for sendika in sendikalar:
            self.sendika_listbox.insert("", "end", values=(sendika,))

    def add_sendika(self):
        sendika = self.sendika_entry.get().strip()
        if sendika:
            if self.sendika_controller.add_sendika_tanimi(sendika):
                self.sendika_entry.delete(0, "end")
                self.load_sendika_tanimlari()
            else:
                messagebox.showwarning("Uyarı", "Bu sendika zaten tanımlı!")
        else:
            messagebox.showwarning("Uyarı", "Sendika ismi boş olamaz!")

    def delete_sendika(self):
        selected = self.sendika_listbox.selection()
        if selected:
            sendika = self.sendika_listbox.item(selected[0])["values"][0]
            if messagebox.askyesno("Onay", f"{sendika} silinecek. Emin misiniz?"):
                self.sendika_controller.delete_sendika_tanimi(sendika)
                self.load_sendika_tanimlari()
