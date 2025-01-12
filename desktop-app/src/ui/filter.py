import ttkbootstrap as ttk

class FilterFrame(ttk.Frame):
    def __init__(self, parent, table_controller):
        super().__init__(parent)
        self.table_controller = table_controller
        self.create_widgets()

    def create_widgets(self):
        # Left side - Search
        search_frame = ttk.Frame(self)
        search_frame.pack(side="left", fill="y")
        
        self.filter_label = ttk.Label(search_frame, text="Arama:")
        self.filter_label.pack(side="left", padx=5)
        
        self.filter_entry = ttk.Entry(search_frame, width=30)
        self.filter_entry.pack(side="left", padx=5)
        self.filter_entry.bind("<KeyRelease>", self.on_filter_change)

        # Right side - Export buttons
        export_frame = ttk.Frame(self)
        export_frame.pack(side="right", fill="y")
        
        self.export_excel_button = ttk.Button(export_frame, text="Excel'e Aktar", command=self.export_to_excel)
        self.export_excel_button.pack(side="left", padx=5)
        
        self.export_pdf_button = ttk.Button(export_frame, text="PDF'e Aktar", command=self.export_to_pdf)
        self.export_pdf_button.pack(side="left", padx=5)

    def on_filter_change(self, event):
        filter_text = self.filter_entry.get()
        self.table_controller.apply_filter(filter_text)

    def get_visible_records(self):
        # Get currently visible records from the table
        records = []
        for item in self.table_controller.table_view.table.get_children():
            values = self.table_controller.table_view.table.item(item)['values']
            records.append(values)
        return records

    def export_to_excel(self):
        import pandas as pd
        import os
        import datetime
        
        # Get currently visible data from table
        data = self.get_visible_records()

        # Create a DataFrame
        df = pd.DataFrame(data, columns=["ID", "T.C. Kimlik Numarası", "İsim Soyisim", 
                                       "İşlem Tarihi", "İşlem Tipi", "Açıklama", 
                                       "Kayıt Zamanı", "Bilgisayar Adı"])

        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"Kayıtlar_{now}.xlsx"
        filepath = os.path.join(desktop_path, filename)

        df.to_excel(filepath, index=False)
        os.startfile(filepath)

    def export_to_pdf(self):
        import os
        import datetime
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4  # Remove landscape, use portrait A4
        from reportlab.lib.units import cm  # Add cm for margin adjustments
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        
        # Register Turkish font
        font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'DejaVuSans.ttf')
        pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
        
        # Get currently visible data
        data = self.get_visible_records()
        
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"Kayıtlar_{now}.pdf"
        filepath = os.path.join(desktop_path, filename)
        
        # Create the PDF document with margins
        doc = SimpleDocTemplate(
            filepath, 
            pagesize=A4,
            rightMargin=1*cm,
            leftMargin=1*cm,
            topMargin=1*cm,
            bottomMargin=1*cm
        )
        
        # Create styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontName='DejaVuSans',
            fontSize=16,
            alignment=1,  # Center alignment
            spaceAfter=30
        )
        
        timestamp_style = ParagraphStyle(
            'Timestamp',
            parent=styles['Normal'],
            fontName='DejaVuSans',
            fontSize=8,
            alignment=2  # Right alignment
        )
        
        # Create document elements
        elements = []
        
        # Add title
        title = Paragraph("Mutemetlik İşlem Kayıtları", title_style)
        timestamp = Paragraph(f"Rapor Tarihi: {now}", timestamp_style)
        elements.extend([title, timestamp, Spacer(1, 20)])
        
        # Prepare table data
        headers = ["ID", "T.C. Kimlik No", "İsim Soyisim", "İşlem Tarihi", 
                  "İşlem Tipi", "Açıklama", "Kayıt Zamanı", "PC Adı"]
        table_data = [headers]
        table_data.extend([[str(cell) for cell in row] for row in data])
        
        # Adjust table column widths for portrait mode
        col_widths = [
            0.7*cm,     # ID
            2.5*cm,     # TC No
            3*cm,       # İsim Soyisim
            2*cm,       # İşlem Tarihi
            2.5*cm,     # İşlem Tipi
            3*cm,       # Açıklama
            2.5*cm,     # Kayıt Zamanı
            2*cm        # PC Adı
        ]

        # Create table with specified column widths
        table = Table(table_data, colWidths=col_widths, repeatRows=1)
        
        # Create zebra striping and style
        style = TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),  # Slightly smaller header font
            ('FONTSIZE', (0, 1), (-1, -1), 8),  # Smaller content font
            ('FONTSIZE', (6, 1), (6, -1), 6),   # Kayıt Zamanı column (index 6) specific font size
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ])
        
        # Add zebra striping
        for row in range(1, len(table_data)):
            if row % 2 == 0:
                style.add('BACKGROUND', (0, row), (-1, row), colors.white)
            else:
                style.add('BACKGROUND', (0, row), (-1, row), colors.lightgrey)
        
        table.setStyle(style)
        elements.append(table)
        
        # Build PDF
        doc.build(elements)
        os.startfile(filepath)