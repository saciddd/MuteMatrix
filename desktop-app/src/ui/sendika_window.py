import ttkbootstrap as ttk
from ui.sendika_form import SendikaForm
from ui.sendika_table import SendikaTable
from controllers.sendika_controller import SendikaController
from models.database import Database

class SendikaWindow(ttk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Sendika Takip İşlemleri")
        self.geometry("1024x768")
        
        # Controllers
        self.database = Database()
        self.sendika_controller = SendikaController(self.database)
        
        self.create_widgets()
        
        # Pencere kapatma işlemini özelleştirelim
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def create_widgets(self):
        # Form frame
        form_frame = ttk.Frame(self)
        form_frame.pack(fill="x", padx=10, pady=5)
        
        self.sendika_form = SendikaForm(form_frame, self.sendika_controller)
        self.sendika_form.pack(fill="x")
        
        # Separator
        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=10, pady=5)
        
        # Table frame
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.sendika_table = SendikaTable(table_frame, self.sendika_controller)
        self.sendika_table.pack(fill="both", expand=True)
        
    def on_closing(self):
        try:
            # Tüm widget'ları temizle
            for widget in self.winfo_children():
                if hasattr(widget, 'destroy'):
                    widget.destroy()
        finally:
            # Pencereyi kapat
            self.destroy()
