# DataWrangler V1.0 - Data Preprocessing Terminal
 
DataWrangler is a ETL and data cleaning tool to solve the "Dirty Data" problem, which is a biggest problem in the Machine Learning and Data science projects.
it processes datasets with millions of rows without overwhelming RAM, automatically diagnoses missing (NaN) values, and offers cleaning operations to users via a interface.

## Key Features
* **Multi-Format Support (Multi-Format I/O):** Seamleslly reads end exports flat text files ('.csv', '.xlsx') and relational databases ('.db' SQLite)
* **Smart Memory Management:** Regardless of the file size (e.g. 1 million rows), it only displays a preview of the first 20 rows on the screen to prevent the GUI freezing. It performs the actual operations on the main Dataframe in the background.
* **Automatic Diagnostics:** When the data is loaded, it scans the entire dataset in the background and notifies the users of total number of "NaN" cells.
* **Dynamic Data Cleaning:** 
  * **Drop:** Removes all rows containing missing data from database.
  * **Fill and Smart Type Casting:** Fill empty cells with specific value entered by the users. if the input is text, it is automatically detected as a "string"; if it is a number, it is detected as an `integer/float`. This prevents numerical data types from being corrupted.
* **Security Wall (Error Handling):** Features an Event-Driven error handling mechanism that prevents the `mainloop` from freezing when invalid or unsupported file formats are loaded.

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
