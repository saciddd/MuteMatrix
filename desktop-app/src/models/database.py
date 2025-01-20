import os
import sqlite3

class Database:
    def __init__(self):
        base_path = os.path.abspath(os.path.dirname(__file__))
        db_name = os.path.join(base_path, "veritabani.db")  # Veritabanı dosyanızın adı
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()
        self.create_islem_tipleri_table()
        self.migrate_database()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tc_kimlik_no TEXT NOT NULL,
                isim_soyisim TEXT NOT NULL,
                islem_tarihi DATE NOT NULL,
                islem_tipi TEXT NOT NULL,
                aciklama TEXT,
                kayit_zamani TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                bilgisayar_adi TEXT NOT NULL
            )
        ''')
        
        # Sendika takip tablosu
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sendika_kayitlari (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tc_kimlik_no TEXT NOT NULL,
                isim_soyisim TEXT NOT NULL,
                sendika_ismi TEXT NOT NULL,
                islem_tarihi DATE NOT NULL,
                islem_tipi TEXT NOT NULL,
                kayit_zamani TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                bilgisayar_adi TEXT NOT NULL,
                maas_donemi TEXT NOT NULL
            )
        ''')
        
        # Sendika tanımları tablosu
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sendika_tanimlari (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sendika_ismi TEXT NOT NULL UNIQUE
            )
        ''')
        self.connection.commit()

    def create_islem_tipleri_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS islem_tipleri (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                islem_tipi TEXT NOT NULL UNIQUE
            )
        ''')
        self.connection.commit()

    def migrate_database(self):
        # Check if color column exists
        cursor = self.cursor.execute('PRAGMA table_info(islem_tipleri)')
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add color column if it doesn't exist
        if 'color' not in columns:
            try:
                self.cursor.execute('ALTER TABLE islem_tipleri ADD COLUMN color TEXT DEFAULT "default"')
                self.connection.commit()
            except sqlite3.OperationalError:
                # Column might have been added by another instance
                pass

    def insert_record(self, tc_kimlik_no, isim_soyisim, islem_tarihi, islem_tipi, aciklama, bilgisayar_adi):
        self.cursor.execute('''
            INSERT INTO records (tc_kimlik_no, isim_soyisim, islem_tarihi, islem_tipi, aciklama, bilgisayar_adi)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (tc_kimlik_no, isim_soyisim, islem_tarihi, islem_tipi, aciklama, bilgisayar_adi))
        self.connection.commit()

    def fetch_all_records(self):
        self.cursor.execute('''
            SELECT id, tc_kimlik_no, isim_soyisim, islem_tarihi, islem_tipi, 
                   aciklama, kayit_zamani, bilgisayar_adi 
            FROM records 
            ORDER BY id DESC
        ''')
        return self.cursor.fetchall()

    def fetch_record_by_id(self, record_id):
        self.cursor.execute('SELECT * FROM records WHERE id = ?', (record_id,))
        return self.cursor.fetchone()

    def get_filtered_records(self, filter_text):
        self.cursor.execute('''
            SELECT id, tc_kimlik_no, isim_soyisim, islem_tarihi, islem_tipi, 
                   aciklama, kayit_zamani, bilgisayar_adi 
            FROM records
            WHERE tc_kimlik_no LIKE ? OR isim_soyisim LIKE ? OR 
                  islem_tarihi LIKE ? OR islem_tipi LIKE ? OR aciklama LIKE ?
            ORDER BY id DESC
        ''', (f'%{filter_text}%', f'%{filter_text}%', f'%{filter_text}%', 
              f'%{filter_text}%', f'%{filter_text}%'))
        return self.cursor.fetchall()

    def get_islem_tipleri(self):
        try:
            self.cursor.execute('SELECT islem_tipi, color FROM islem_tipleri ORDER BY islem_tipi')
            return self.cursor.fetchall()
        except sqlite3.OperationalError:
            self.cursor.execute('SELECT islem_tipi, "default" FROM islem_tipleri ORDER BY islem_tipi')
            return self.cursor.fetchall()

    def get_islem_tipleri_values(self):
        self.cursor.execute('SELECT islem_tipi FROM islem_tipleri ORDER BY islem_tipi')
        return [row[0] for row in self.cursor.fetchall()]

    def add_islem_tipi(self, islem_tipi, color='default'):
        try:
            self.cursor.execute('INSERT INTO islem_tipleri (islem_tipi, color) VALUES (?, ?)', 
                              (islem_tipi, color))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def update_islem_tipi_color(self, islem_tipi, color):
        self.cursor.execute('UPDATE islem_tipleri SET color = ? WHERE islem_tipi = ?', 
                          (color, islem_tipi))
        self.connection.commit()

    def delete_islem_tipi(self, islem_tipi):
        self.cursor.execute('DELETE FROM islem_tipleri WHERE islem_tipi = ?', (islem_tipi,))
        self.connection.commit()

    def update_record(self, record_id, tc_kimlik_no, isim_soyisim, islem_tarihi, islem_tipi, aciklama):
        self.cursor.execute('''
            UPDATE records 
            SET tc_kimlik_no = ?, 
                isim_soyisim = ?, 
                islem_tarihi = ?, 
                islem_tipi = ?, 
                aciklama = ?
            WHERE id = ?
        ''', (tc_kimlik_no, isim_soyisim, islem_tarihi, islem_tipi, aciklama, record_id))
        self.connection.commit()

    def delete_record(self, record_id):
        self.cursor.execute('DELETE FROM records WHERE id = ?', (record_id,))
        self.connection.commit()

    # Sendika işlemleri için yeni metodlar
    def insert_sendika_kayit(self, tc_kimlik_no, isim_soyisim, sendika_ismi, 
                           islem_tarihi, islem_tipi, bilgisayar_adi, maas_donemi):
        self.cursor.execute('''
            INSERT INTO sendika_kayitlari 
            (tc_kimlik_no, isim_soyisim, sendika_ismi, islem_tarihi, 
             islem_tipi, bilgisayar_adi, maas_donemi)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (tc_kimlik_no, isim_soyisim, sendika_ismi, islem_tarihi, 
              islem_tipi, bilgisayar_adi, maas_donemi))
        self.connection.commit()

    def get_sendika_kayitlari(self, yil=None, ay=None):
        query = '''
            SELECT * FROM sendika_kayitlari 
            WHERE 1=1
        '''
        params = []
        
        if yil is not None and ay is not None:
            maas_donemi = f"{int(yil)}-{int(ay):02d}"
            query += ' AND maas_donemi = ?'
            params.append(maas_donemi)
            
        query += ' ORDER BY kayit_zamani DESC'
        
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def get_sendika_tanimlari(self):
        self.cursor.execute('SELECT sendika_ismi FROM sendika_tanimlari ORDER BY sendika_ismi')
        return [row[0] for row in self.cursor.fetchall()]

    def add_sendika_tanimi(self, sendika_ismi):
        try:
            self.cursor.execute('INSERT INTO sendika_tanimlari (sendika_ismi) VALUES (?)', 
                              (sendika_ismi,))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def delete_sendika_tanimi(self, sendika_ismi):
        self.cursor.execute('DELETE FROM sendika_tanimlari WHERE sendika_ismi = ?', 
                          (sendika_ismi,))
        self.connection.commit()

    def check_ayrilma_kaydi(self, tc_kimlik_no, baslangic_tarihi, bitis_tarihi):
        """Belirtilen tarih aralığında ayrılış kaydı var mı kontrol eder"""
        self.cursor.execute('''
            SELECT COUNT(*) FROM sendika_kayitlari
            WHERE tc_kimlik_no = ?
            AND islem_tipi = 'Ayrılış'
            AND islem_tarihi BETWEEN ? AND ?
        ''', (tc_kimlik_no, baslangic_tarihi, bitis_tarihi))
        
        return self.cursor.fetchone()[0] > 0

    def update_sendika_kayit(self, old_tc_no, tc_no, isim, sendika, tarih, islem_tipi, maas_donemi):
        self.cursor.execute('''
            UPDATE sendika_kayitlari 
            SET tc_kimlik_no = ?, 
                isim_soyisim = ?, 
                sendika_ismi = ?, 
                islem_tarihi = ?,
                islem_tipi = ?,
                maas_donemi = ?
            WHERE tc_kimlik_no = ?
        ''', (tc_no, isim, sendika, tarih, islem_tipi, maas_donemi, old_tc_no))
        self.connection.commit()
        return True

    def delete_sendika_kayit(self, tc_no):
        self.cursor.execute('DELETE FROM sendika_kayitlari WHERE tc_kimlik_no = ?', (tc_no,))
        self.connection.commit()
        return True

    def close(self):
        self.connection.close()
