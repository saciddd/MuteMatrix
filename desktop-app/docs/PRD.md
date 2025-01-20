# Product Requirements Document: MuteMatrix Sendika Takip Modülü

## 1. Giriş

### 1.1 Mevcut Sistem
MuteMatrix, personel işlemlerinin takibi için geliştirilmiş bir masaüstü uygulamasıdır. Şu anda:
- Personel işlem kayıtları (izin, görevlendirme vb.)
- Excel ve PDF export özellikleri
- Özelleştirilebilir tema desteği
- Filtreleme ve arama özellikleri
bulunmaktadır.

### 1.2 Yeni Modül İhtiyacı
Sendika üyelik işlemlerinin takibi ve maaş dönemlerine göre kesinti raporlaması ihtiyacı.

## 2. Sendika Takip Modülü Özellikleri

### 2.1 Kullanıcı Arayüzü
- Ana ekranda "Sendika Takip İşlemleri" butonu
- Yeni pencerede ana form ve tablo görünümü
- Veri giriş formu
  * T.C. Kimlik Numarası (text)
  * İsim Soyisim (text)
  * İşlem Tarihi (date_entry)
  * Sendika İsmi (combobox + dişli butonu)
  * İşlem Tipi (radio buttons: Üyelik/Ayrılış)
- Dönem seçim alanı
  * Yıl seçimi (mevcut yıl ±1)
  * Ay seçimi (1-12)
- Export butonları (Excel/PDF)
- Kayıt tablosu (renk kodlu)

### 2.2 Veritabanı Yapısı

#### 2.2.1 Ana Tablolar

PRD.md'yi güncelleyerek tamamlayalım:

```markdown


# Product Requirements Document: MuteMatrix Sendika Takip Modülü

## 1. Giriş
// ...existing code...

### 2.2 Veritabanı Yapısı

#### 2.2.1 Ana Tablolar
```sql
CREATE TABLE sendika_kayitlari (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tc_kimlik_no TEXT NOT NULL,
    isim_soyisim TEXT NOT NULL,
    sendika_ismi TEXT NOT NULL,
    islem_tarihi DATE NOT NULL,
    islem_tipi TEXT NOT NULL,
    kayit_zamani TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    bilgisayar_adi TEXT NOT NULL,
    maas_donemi TEXT NOT NULL
);

CREATE TABLE sendika_tanimlari (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sendika_ismi TEXT NOT NULL UNIQUE
);
```

### 2.3 İş Kuralları ve Hesaplamalar

#### 2.3.1 Maaş Dönemi Hesaplama Kuralları
- Her ayın 15'i kritik tarihtir
- 15'inden önceki işlemler o ayın maaş dönemine dahil edilir
- 15'i ve sonrasındaki işlemler sonraki ayın maaş dönemine dahil edilir
- Örnek: 14 Ocak → Ocak maaşı, 15 Ocak → Şubat maaşı

#### 2.3.2 Sendika Üyelik Kuralları
1. Yeni Üyelik (Eski sendika yok):
   - Üyelik tarihi itibariyle kesinti başlar
   - İlgili maaş dönemine atanır

2. Sendika Değişikliği (Eski sendika var):
   - İstifa tarihinden 1 ay sonra kesinti başlar
   - 1 ay sonraki tarihin denk geldiği maaş dönemine atanır
   - Örnek: 5 Ocak istifa → 5 Şubat kesinti → Şubat maaş dönemi

### 2.4 Raporlama Özellikleri

#### 2.4.1 Kesinti Listesi
- Yıl-Ay bazlı filtreleme
- Üyelik/Ayrılış durumlarına göre renk kodlaması
- Excel ve PDF export seçenekleri
- Rapor içeriği:
  * T.C. Kimlik No
  * İsim Soyisim
  * Sendika Adı
  * İşlem Tarihi
  * İşlem Tipi
  * Maaş Dönemi

### 2.5 Veri Doğrulama

#### 2.5.1 Giriş Kontrolleri
- T.C. Kimlik No: 11 haneli numerik
- İsim Soyisim: Zorunlu alan
- İşlem Tarihi: Geçerli tarih formatı
- Sendika: Listeden seçim
- İşlem Tipi: Üyelik/Ayrılış seçimi zorunlu

### 2.6 Kullanıcı Deneyimi
- Tema desteği (ana uygulama ile entegre)
- Sezgisel form düzeni
- Hızlı veri girişi
- Anlık geri bildirimler
- Modal pencere yaklaşımı

### 2.7 Teknik Gereksinimler
- Python 3.8+
- SQLite veritabanı
- ttkbootstrap, pandas, reportlab
- Modüler yapı
- Performans optimizasyonu

### 2.8 Gelecek Geliştirmeler
- Toplu veri girişi
- Detaylı filtreleme
- Sendika bazlı raporlama
- Otomatik yedekleme
- Veri doğrulama geliştirmeleri
```
