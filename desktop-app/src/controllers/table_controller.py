import platform
from models.database import Database

class TableController:
    def __init__(self, table_view):
        self.table_view = table_view
        self.database = Database()

    def load_data(self):
        if self.table_view:
            data = self.database.fetch_all_records()
            self.table_view.display_data(data)

    def update_table(self):
        self.load_data()

    def get_record_info(self, record_id):
        record = self.database.fetch_record_by_id(record_id)
        if record:
            return {
                "timestamp": record['timestamp'],
                "computer_name": record['computer_name']
            }
        return None

    def filter_data(self, filter_criteria):
        filtered_data = self.database.get_filtered_records(filter_criteria)
        self.table_view.display_data(filtered_data)

    def apply_filter(self, filter_text):
        filtered_data = self.database.get_filtered_records(filter_text)
        self.table_view.display_data(filtered_data)

    def submit_form(self, tc_kimlik, isim_soyisim, islem_tarihi, islem_tipi, aciklama):
        bilgisayar_adi = platform.node()
        self.database.insert_record(tc_kimlik, isim_soyisim, islem_tarihi, islem_tipi, aciklama, bilgisayar_adi)
        self.update_table()
        return "Veri başarıyla kaydedildi."

    # Tablodaki verileri saklayan Get Data fonksiyonu
    def get_data(self):
        return self.database.fetch_all_records()

    def get_islem_tipleri(self):
        return self.database.get_islem_tipleri()

    def add_islem_tipi(self, islem_tipi, color='default'):
        return self.database.add_islem_tipi(islem_tipi, color)

    def update_islem_tipi_color(self, islem_tipi, color):
        return self.database.update_islem_tipi_color(islem_tipi, color)

    def delete_islem_tipi(self, islem_tipi):
        return self.database.delete_islem_tipi(islem_tipi)

    def get_islem_tipleri_values(self):
        return self.database.get_islem_tipleri_values()

    def update_record(self, record_id, tc_kimlik, isim_soyisim, islem_tarihi, islem_tipi, aciklama):
        try:
            self.database.update_record(record_id, tc_kimlik, isim_soyisim, 
                                      islem_tarihi, islem_tipi, aciklama)
            self.load_data()
            return True
        except Exception as e:
            print(f"Error updating record: {e}")
            return False

    def delete_record(self, record_id):
        try:
            self.database.delete_record(record_id)
            self.load_data()
            return True
        except Exception as e:
            print(f"Error deleting record: {e}")
            return False