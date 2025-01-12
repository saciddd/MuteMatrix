from src.models.database import Database

class FormController:
    def __init__(self):
        self.database = Database()

    def validate_input(self, tc_kimlik, isim_soyisim, islem_tarihi, islem_tipi, aciklama):
        if not tc_kimlik.isdigit() or len(tc_kimlik) != 11:
            return False, "T.C. Kimlik Numarası geçersiz."
        if not isim_soyisim:
            return False, "İsim Soyisim zorunludur."
        if not islem_tarihi:
            return False, "İşlem Tarihi zorunludur."
        if not islem_tipi:
            return False, "İşlem Tipi zorunludur."
        return True, ""

    def submit_form(self, tc_kimlik, isim_soyisim, islem_tarihi, islem_tipi, aciklama):
        is_valid, message = self.validate_input(tc_kimlik, isim_soyisim, islem_tarihi, islem_tipi, aciklama)
        if not is_valid:
            return message
        
        self.database.insert_record(tc_kimlik, isim_soyisim, islem_tarihi, islem_tipi, aciklama)
        return "Veri başarıyla kaydedildi."