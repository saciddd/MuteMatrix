import ttkbootstrap as ttk
from tkinter import StringVar, messagebox
import calendar
from datetime import datetime

class SendikaTable(ttk.Frame):
    def __init__(self, parent, sendika_controller):
        super().__init__(parent)
        self.sendika_controller = sendika_controller
        self.create_filter_frame()
        self.create_table()
        self.create_context_menu()
        # Remove initial year/month selection to show all records at startup
        self.yil_var.set('')
        self.ay_var.set('')

    def create_filter_frame(self):
        filter_frame = ttk.Frame(self)
        filter_frame.pack(fill="x", padx=5, pady=5)

        # Maaş dönemi seçimi
        ttk.Label(filter_frame, text="Maaş Dönemi Seçimi:").pack(side="left", padx=5)
        
        # Yıl seçimi
        current_year = datetime.now().year
        self.yil_var = StringVar()
        self.yil_combo = ttk.Combobox(filter_frame, textvariable=self.yil_var, 
                                values=[current_year-1, current_year, current_year+1],
                                width=6, state="readonly")
        self.yil_combo.set(current_year)
        self.yil_combo.pack(side="left", padx=5)

        # Ay seçimi
        self.ay_var = StringVar()
        self.ay_combo = ttk.Combobox(filter_frame, textvariable=self.ay_var,
                               values=[f"{i:02d}" for i in range(1, 13)],
                               width=4, state="readonly")
        self.ay_combo.set(f"{datetime.now().month:02d}")
        self.ay_combo.pack(side="left", padx=5)

        # Tüm Kayıtlar butonu
        ttk.Button(filter_frame, text="Tüm Kayıtlar", 
                  command=self.show_all_records).pack(side="left", padx=5)

        # Export buttons
        ttk.Button(filter_frame, text="Excel'e Aktar", 
                  command=self.export_excel).pack(side="right", padx=5)
        ttk.Button(filter_frame, text="PDF'e Aktar", 
                  command=self.export_pdf).pack(side="right", padx=5)

        # Bind events
        self.yil_combo.bind('<<ComboboxSelected>>', self.filter_changed)
        self.ay_combo.bind('<<ComboboxSelected>>', self.filter_changed)

    def create_table(self):
        # Create scrollbars
        y_scrollbar = ttk.Scrollbar(self)
        y_scrollbar.pack(side="right", fill="y")

        # Create table
        columns = ("tc_no", "isim", "sendika", "islem_tarihi", "islem_tipi", "maas_donemi")
        self.table = ttk.Treeview(self, columns=columns, show="headings", 
                                 yscrollcommand=y_scrollbar.set)

        # Configure columns
        self.table.heading("tc_no", text="T.C. Kimlik No")
        self.table.heading("isim", text="İsim Soyisim")
        self.table.heading("sendika", text="Sendika")
        self.table.heading("islem_tarihi", text="İşlem Tarihi")
        self.table.heading("islem_tipi", text="İşlem Tipi")
        self.table.heading("maas_donemi", text="Maaş Dönemi")

        # Configure column widths
        self.table.column("tc_no", width=100)
        self.table.column("isim", width=150)
        self.table.column("sendika", width=150)
        self.table.column("islem_tarihi", width=100)
        self.table.column("islem_tipi", width=100)
        self.table.column("maas_donemi", width=100)

        # Configure tags for colors
        self.table.tag_configure("Üyelik", background="#d4edda")  # success
        self.table.tag_configure("Ayrılış", background="#f8d7da")  # danger

        self.table.pack(fill="both", expand=True)
        y_scrollbar.config(command=self.table.yview)

    def create_context_menu(self):
        self.context_menu = ttk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Sil", command=self.delete_record)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Yenile", command=self.load_data)
        
        self.table.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        item = self.table.identify_row(event.y)
        if item:
            self.table.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def delete_record(self):
        selected = self.table.selection()
        if selected:
            item = selected[0]
            values = self.table.item(item)['values']
            if values and messagebox.askyesno("Onay", "Bu kaydı silmek istediğinizden emin misiniz?"):
                if self.sendika_controller.delete_kayit(values[0]):
                    messagebox.showinfo("Başarılı", "Kayıt silindi.")
                    self.load_data()
                else:
                    messagebox.showerror("Hata", "Kayıt silinirken bir hata oluştu.")

    def filter_changed(self, event=None):
        self.load_data()

    def load_data(self):
        # Clear existing items
        for item in self.table.get_children():
            self.table.delete(item)

        # Get filtered data
        yil = int(self.yil_var.get()) if self.yil_var.get() else None
        ay = int(self.ay_var.get()) if self.ay_var.get() else None
        records = self.sendika_controller.get_kayitlar(yil, ay)

        # Insert data
        for record in records:
            # Convert date format from YYYY-MM-DD to DD.MM.YYYY
            islem_tarihi = datetime.strptime(record[4], '%Y-%m-%d').strftime('%d.%m.%Y')
            
            self.table.insert("", "end", values=(
                record[1],  # tc_no
                record[2],  # isim
                record[3],  # sendika
                islem_tarihi,  # formatted islem_tarihi
                record[5],  # islem_tipi
                record[8]   # maas_donemi (düzeltildi: 7 yerine 8)
            ), tags=(record[5],))  # Use islem_tipi for row color

    def show_all_records(self):
        self.yil_combo.set('')
        self.ay_combo.set('')
        self.load_data()

    def export_excel(self):
        import pandas as pd
        import os
        from datetime import datetime
        
        yil = self.yil_var.get()
        ay = self.ay_var.get()
        
        data = []
        for item in self.table.get_children():
            values = self.table.item(item)['values']
            # Convert date string to datetime for proper Excel date formatting
            islem_tarihi = datetime.strptime(values[3], '%d.%m.%Y')
            
            data.append({
                'TC Kimlik No': values[0],
                'İsim Soyisim': values[1],
                'Sendika': values[2],
                'İşlem Tarihi': islem_tarihi,  # Pass datetime object directly
                'İşlem Tipi': values[4],
                'Maaş Dönemi': values[5]
            })
            
        df = pd.DataFrame(data)
        
        # Configure Excel writer with date format
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        filename = f"Sendika_Kesinti_Listesi_{yil}_{ay}.xlsx"
        filepath = os.path.join(desktop_path, filename)
        
        with pd.ExcelWriter(filepath, engine='openpyxl', datetime_format='DD.MM.YYYY') as writer:
            df.to_excel(writer, index=False)
            
            # Auto-adjust column widths
            worksheet = writer.sheets['Sheet1']
            for idx, col in enumerate(df.columns):
                max_length = max(df[col].astype(str).apply(len).max(),
                               len(col)) + 2
                worksheet.column_dimensions[chr(65+idx)].width = max_length
        
        os.startfile(filepath)

    def export_pdf(self):
        import os
        from datetime import datetime
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        
        yil = self.yil_var.get()
        ay = self.ay_var.get()
        
        # Font registration
        font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'DejaVuSans.ttf')
        pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
        
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        filename = f"Sendika_Kesinti_Listesi_{yil}_{ay}.pdf"
        filepath = os.path.join(desktop_path, filename)
        
        doc = SimpleDocTemplate(
            filepath,
            pagesize=landscape(A4),
            rightMargin=1*cm,
            leftMargin=1*cm,
            topMargin=1*cm,
            bottomMargin=1*cm
        )
        
        elements = []
        
        # Title
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontName='DejaVuSans',
            fontSize=14,
            alignment=1
        )
        
        title = Paragraph(f"Sendika Kesinti Listesi - {yil}/{ay}", title_style)
        elements.append(title)
        
        # Table data
        data = [["TC Kimlik No", "İsim Soyisim", "Sendika", 
                 "İşlem Tarihi", "İşlem Tipi", "Maaş Dönemi"]]
        
        for item in self.table.get_children():
            values = self.table.item(item)['values']
            data.append([str(v) for v in values])
        
        # Create table
        t = Table(data)
        t.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
            ]))
        elements.append(t)
        doc.build(elements)
        os.startfile(filepath)