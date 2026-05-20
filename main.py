import customtkinter as ctk
from tkinter import ttk, filedialog
import pandas as pd
import os
import sqlite3  # SQL VERİTABANI MOTORU EKLENDİ


class DataWranglerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- ANA PENCERE AYARLARI ---
        self.title("DataWrangler V1.0 - Veri Ön İşleme Terminali")
        self.geometry("1100x600")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        # ==========================================
        # 1. SOL PANEL
        # ==========================================
        self.left_frame = ctk.CTkFrame(self, corner_radius=10)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.lbl_title = ctk.CTkLabel(self.left_frame, text="Kontrol Paneli", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_title.pack(pady=(20, 30))

        # DB DOSYASI FİLTRESİ EKLENDİ
        self.btn_select = ctk.CTkButton(self.left_frame, text="📂 Dosya Seç (CSV/Excel/DB)", command=self.load_file)
        self.btn_select.pack(pady=10, padx=20, fill="x")

        self.lbl_status = ctk.CTkLabel(self.left_frame, text="Durum: Bekleniyor...", text_color="gray")
        self.lbl_status.pack(pady=5)

        self.spacer = ctk.CTkLabel(self.left_frame, text="")
        self.spacer.pack(expand=True, fill="both")

        self.btn_save = ctk.CTkButton(self.left_frame, text="💾 Temizlenmiş Veriyi Kaydet", fg_color="#28a745",
                                      hover_color="#218838")
        self.btn_save.pack(pady=20, padx=20, fill="x")

        # ==========================================
        # 2. SAĞ PANEL (ÖNİZLEME VE AKSİYONLAR)
        # ==========================================
        self.right_frame = ctk.CTkFrame(self, corner_radius=10)
        self.right_frame.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="nsew")

        self.lbl_preview = ctk.CTkLabel(self.right_frame, text="Tablo Önizleme (İlk 20 Satır)",
                                        font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl_preview.pack(pady=(15, 5), padx=15, anchor="w")

        self.tree_frame = ctk.CTkFrame(self.right_frame)
        self.tree_frame.pack(fill="both", expand=True, padx=15, pady=10)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview.Heading", font=("Arial", 13, "bold"), background="#333333", foreground="white")
        style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b", borderwidth=0,
                        font=("Arial", 12), rowheight=35)
        style.map('Treeview', background=[('selected', '#1f538d')])

        self.tree = ttk.Treeview(self.tree_frame, show="headings")
        self.tree.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.lbl_diagnostic = ctk.CTkLabel(self.right_frame, text="Teşhis: Lütfen analiz edilecek bir dosya yükleyin.",
                                           text_color="#f39c12", font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_diagnostic.pack(pady=(10, 5))

        self.action_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.action_frame.pack(pady=15, fill="x", padx=15)

        self.btn_drop = ctk.CTkButton(self.action_frame, text="🗑️ Boşlukları Sil (Drop)", fg_color="#c0392b",
                                      hover_color="#a93226")
        self.btn_drop.pack(side="left", padx=10)

        self.entry_fill = ctk.CTkEntry(self.action_frame, placeholder_text="Örn: 0 veya Bilinmiyor", width=150)
        self.entry_fill.pack(side="left", padx=(40, 10))

        self.btn_fill = ctk.CTkButton(self.action_frame, text="✏️ Boşlukları Doldur (Fill)")
        self.btn_fill.pack(side="left")

    # ==========================================
    # FONKSİYONLAR
    # ==========================================
    def load_file(self):
        # Arama filtresine DB eklendi
        file_path = filedialog.askopenfilename(
            title="İşlenecek Veriyi Seç",
            filetypes=(("CSV Dosyaları", "*.csv"), ("Excel Dosyaları", "*.xlsx"), ("SQLite Veritabanı", "*.db"),
                       ("Tüm Dosyalar", "*.*"))
        )

        if not file_path:
            return

        filename = os.path.basename(file_path)
        self.lbl_status.configure(text=f"Yüklendi: {filename}", text_color="white")

        try:
            # --- YENİ OKUMA MOTORU ---
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path, nrows=20)

            elif file_path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(file_path, nrows=20)

            elif file_path.endswith('.db'):
                # 1. Veritabanına bağlan
                conn = sqlite3.connect(file_path)
                cursor = conn.cursor()

                # 2. İçerideki tablo isimlerini bul (Senin V2.0'ın ürettiği tabloyu bulmak için)
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()

                if not tables:
                    self.lbl_status.configure(text="Hata: DB içinde tablo yok!", text_color="red")
                    conn.close()
                    return

                first_table_name = tables[0][0]  # Bulduğu ilk tablonun adını alır

                # 3. Sadece ilk 20 satırı oku
                df = pd.read_sql_query(f"SELECT * FROM '{first_table_name}' LIMIT 20", conn)
                conn.close()  # İşimiz bitti, bağlantıyı kapatıyoruz ki dosya kilitlenmesin

            # --- TABLOYA YAZDIRMA ---
            self.tree.delete(*self.tree.get_children())

            self.tree["columns"] = list(df.columns)
            for col in df.columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=150, anchor="center")

            for index, row in df.iterrows():
                self.tree.insert("", "end", values=list(row))

            self.lbl_diagnostic.configure(text=f"Analiz: Tabloda boş kutular tespit edildi. Aksiyon seçin.")

        except Exception as e:
            self.lbl_status.configure(text="Okuma Hatası!", text_color="red")
            print("Hata Detayı:", e)


if __name__ == "__main__":
    app = DataWranglerApp()
    app.mainloop()