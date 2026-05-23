# DataWrangler V1.0 - Veri Ön İşleme (Data Preprocessing) Terminali

DataWrangler, Makine Öğrenmesi ve Veri Bilimi projelerindeki en büyük darboğaz olan "Kirli Veri" problemini çözmek için tasarlanmış, modern arayüzlü bir masaüstü ETL ve veri temizleme aracıdır. 

Milyonlarca satırlık veri setlerini RAM'i boğmadan işler, eksik (NaN) verileri otomatik olarak teşhis eder ve kullanıcıya profesyonel bir arayüz üzerinden temizleme operasyonları sunar.

## 🚀 Temel Özellikler

* **Çoklu Format Desteği (Multi-Format I/O):** Düz metin dosyalarını (`.csv`, `.xlsx`) ve ilişkisel veritabanlarını (`.db` SQLite) sorunsuzca okur ve dışa aktarır.
* **Akıllı Bellek Yönetimi:** Dosya boyutu ne olursa olsun (örn: 1 milyon satır), GUI'nin kilitlenmesini önlemek için ekrana sadece ilk 20 satırın (Head) önizlemesini yansıtır, asıl işlemleri arka planda ana DataFrame üzerinde yapar.
* **Otomatik Diagnostik:** Veri yüklendiği anda arka planda tüm seti tarar ve toplam `NaN` (boş) veri hücresi sayısını tespit edip kullanıcıya bildirir.
* **Dinamik Veri Temizliği:**
  * **Drop (Silme):** Eksik veri barındıran tüm satırları veri setinden temizler.
  * **Fill (Doldurma) ve Akıllı Tip Dönüşümü (Type Casting):** Boşlukları kullanıcının girdiği spesifik bir değerle doldurur. Girdi metin ise `string`, sayı ise `integer/float` olarak otomatik algılanır, böylece sayısal veri tipleri bozulmaz.
* **Güvenlik Duvarı (Error Handling):** Hatalı veya desteklenmeyen formatlarda dosyalar yüklendiğinde `mainloop`'un kilitlenmesini engelleyen Event-Driven (Olay Güdümlü) hata yakalama mekanizmasına sahiptir.

## 🛠️ Kullanılan Teknolojiler
* **Python**
* **Pandas:** Arka plandaki veri manipülasyonu ve analiz motoru.
* **CustomTkinter:** Modern, karanlık tema destekli grafik kullanıcı arayüzü (GUI).
* **SQLite3:** Veritabanı bağlantı ve sorgulama işlemleri (Dahili kütüphane).

## Programın Kullanımı
1. Kodu çalıştırdığınız anda aşağıdaki pencere karşınıza gelir:

<img width="1367" height="784" alt="Ekran görüntüsü 2026-05-23 184541" src="https://github.com/user-attachments/assets/902e31b9-511c-434a-8d06-e6ad5513b323" />

2. Sol taraftaki kontrol panelinden "Select File (CSV/Excel/DB)" butonuna basıp veri temizliği yapmak istediğiniz dosyayı seçmelisiniz. Dosyayı seçtikten sonra dosyadaki eksik veriler hesaplanır ve sağ panele aşağıdaki gibi tablonuzun ilk 20 satırı gelir ve eğer herhangi bir eksik veri yoksa "No missing values detected" yazısı çıkar:

<img width="1369" height="781" alt="Ekran görüntüsü 2026-05-23 192746" src="https://github.com/user-attachments/assets/32d6809e-ddbe-48ac-9702-5a6d6e41efb2" />

3. Eğer X kadar eksik veri mevcutsa "Found X missing (NaN) values in the dataset!" şeklinde bir yazı çıkar. Eğer bu eksik veri bulunan satırları silmek isterseniz "Drop Missing Values" şeklinde olan kırmızı butona basın. Eğer istediğiniz bir değeri eksik veriler yerine girmek isterseniz "Fill Missing Values" adındaki yeşil butona basın ve istediğiniz yazıyı veya sayıyı girin. İstediğiniz işlemleri yaptıktan sonra eğer temizlenmiş veriyi kaydetmek isterseniz sol panelin altındaki "Save Cleaned Data" butonuna basıp yeni dosyayı isdetiğiniz yere kaydedebilirsiniz.

## 💻 Kurulum ve Çalıştırma (Geliştiriciler İçin)

Projeyi kendi bilgisayarınızda kod olarak çalıştırmak için gerekli kütüphaneleri kurun:

```bash
pip install pandas openpyxl customtkinter
```
Ardından ana dosyayı çalıştırın:

```bash
python main.py
```

## 📦 Masaüstü Uygulaması (EXE) Haline Getirme
Bu programı Python yüklü olmayan herhangi bir Windows bilgisayarda normal bir program (Masaüstü Uygulaması) gibi çalıştırmak isterseniz, tek tıklamalı bir .exe dosyasına dönüştürebilirsiniz.

1. **PyInstaller'ı Yükleyin:** Terminalinizi (veya CMD) açıp aşağıdaki komutu girin:
```bash
pip install pyinstaller
```
2. **EXE Dosyasını Oluşturun:** Proje klasörünüzün içinde terminali açın ve şu komutu çalıştırın:
```bash
pyinstaller --noconsole --onefile main.py
```
Not: --noconsole parametresi, program çalışırken arkada siyah CMD penceresinin açılmasını engeller, sadece arayüz görünür.

3. **Programı Çalıştırın:** İşlem bittiğinde proje klasörünüzde "dist" adında yeni bir klasör oluşacak. Bu klasörün içindeki "main.exe" dosyasını masaüstüne alıp istediğiniz gibi kullanabilirsiniz.
