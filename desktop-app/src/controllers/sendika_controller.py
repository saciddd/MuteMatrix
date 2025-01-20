from datetime import datetime, date, timedelta
import calendar

class SendikaController:
    def __init__(self, database):
        self.database = database

    def hesapla_maas_donemi(self, islem_tarihi, eski_sendika_var=False):
        """Maaş dönemini hesaplar"""
        if isinstance(islem_tarihi, str):
            islem_tarihi = datetime.strptime(islem_tarihi, '%Y-%m-%d').date()

        if eski_sendika_var:
            # Bir ay sonrası için hesaplama
            if islem_tarihi.month == 12:
                next_month = 1
                next_year = islem_tarihi.year + 1
            else:
                next_month = islem_tarihi.month + 1
                next_year = islem_tarihi.year
                
            islem_tarihi = date(next_year, next_month, islem_tarihi.day)

        # 15'inden önce ise aynı ay, sonra ise gelecek ay
        if islem_tarihi.day < 15:
            maas_ayi = islem_tarihi.month
            maas_yili = islem_tarihi.year
        else:
            if islem_tarihi.month == 12:
                maas_ayi = 1
                maas_yili = islem_tarihi.year + 1
            else:
                maas_ayi = islem_tarihi.month + 1
                maas_yili = islem_tarihi.year

        return f"{maas_yili}-{maas_ayi:02d}"

    def check_eski_sendika(self, tc_kimlik_no, islem_tarihi):
        """Belirtilen TC için son 1 ay içinde ayrılış kaydı var mı kontrol eder"""
        if isinstance(islem_tarihi, str):
            islem_tarihi = datetime.strptime(islem_tarihi, '%Y-%m-%d').date()
        
        # Son 1 ay öncesinin tarihi
        bir_ay_once = islem_tarihi - timedelta(days=30)
        
        # Ayrılış kaydı kontrolü
        return self.database.check_ayrilma_kaydi(tc_kimlik_no, bir_ay_once, islem_tarihi)

    def kaydet_sendika_islem(self, tc_kimlik_no, isim_soyisim, sendika_ismi, 
                            islem_tarihi, islem_tipi, bilgisayar_adi):
        # Üyelik ise eski sendika kontrolü yap
        eski_sendika_var = False
        if islem_tipi == "Üyelik":
            eski_sendika_var = self.check_eski_sendika(tc_kimlik_no, islem_tarihi)
        
        maas_donemi = self.hesapla_maas_donemi(islem_tarihi, eski_sendika_var)
        
        self.database.insert_sendika_kayit(
            tc_kimlik_no, isim_soyisim, sendika_ismi, islem_tarihi,
            islem_tipi, bilgisayar_adi, maas_donemi
        )

    def get_sendika_listesi(self):
        return self.database.get_sendika_tanimlari()

    def get_kayitlar(self, yil=None, ay=None):
        """Sendika kayıtlarını getirir ve tarihleri formatlar"""
        records = self.database.get_sendika_kayitlari(yil, ay)
        formatted_records = []
        
        for record in records:
            # record[4] islem_tarihi alanı
            if record[4]:  # If date is not None
                try:
                    # Convert any date format to YYYY-MM-DD
                    date_obj = datetime.strptime(record[4], '%Y-%m-%d')
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    record = list(record)  # Convert tuple to list
                    record[4] = formatted_date
                    formatted_records.append(tuple(record))
                except ValueError:
                    formatted_records.append(record)
            else:
                formatted_records.append(record)
                
        return formatted_records

    def add_sendika_tanimi(self, sendika_ismi):
        """Yeni sendika tanımı ekler"""
        return self.database.add_sendika_tanimi(sendika_ismi)
        
    def delete_sendika_tanimi(self, sendika_ismi):
        """Sendika tanımını siler"""
        return self.database.delete_sendika_tanimi(sendika_ismi)

    def update_kayit(self, old_tc_no, tc_no, isim, sendika, tarih, islem_tipi):
        """Sendika kaydını günceller"""
        try:
            eski_sendika_var = False
            if islem_tipi == "Üyelik":
                eski_sendika_var = self.check_eski_sendika(tc_no, tarih)
            
            maas_donemi = self.hesapla_maas_donemi(tarih, eski_sendika_var)
            
            return self.database.update_sendika_kayit(
                old_tc_no, tc_no, isim, sendika, tarih, islem_tipi, maas_donemi
            )
        except Exception as e:
            print(f"Error updating record: {e}")
            return False

    def delete_kayit(self, tc_no):
        """Sendika kaydını siler"""
        try:
            return self.database.delete_sendika_kayit(tc_no)
        except Exception as e:
            print(f"Error deleting record: {e}")
            return False
