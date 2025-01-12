def export_to_excel(data, filename):
    import pandas as pd
    
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)

def export_to_pdf(data, filename):
    from fpdf import FPDF

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for row in data:
        pdf.cell(200, 10, txt=str(row), ln=True)

    pdf.output(filename)

def get_exportable_data(records):
    exportable_data = []
    for record in records:
        exportable_data.append({
            "T.C. Kimlik Numarası": record[0],
            "İsim Soyisim": record[1],
            "İşlem Tarihi": record[2],
            "İşlem Tipi": record[3],
            "Açıklama": record[4] if len(record) > 4 else ""
        })
    return exportable_data