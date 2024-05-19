import tkinter as tk
from tkinter import messagebox
import sqlite3

# Film sınıfı
class Film:
    def __init__(self, film_id, film_adi, yonetmen, tur):
        self.film_id = film_id
        self.film_adi = film_adi
        self.yonetmen = yonetmen
        self.tur = tur

# Kullanıcı sınıfı
class Kullanici:
    def __init__(self, kullanici_id, kullanici_adi, sifre):
        self.kullanici_id = kullanici_id
        self.kullanici_adi = kullanici_adi
        self.sifre = sifre
        self.izleme_gecmisi = []

# İçerik sınıfı
class Icerik:
    def __init__(self, icerik_id, icerik_adi, sure, tur):
        self.icerik_id = icerik_id
        self.icerik_adi = icerik_adi
        self.sure = sure
        self.tur = tur

# Film ekleme penceresi
class FilmEklePenceresi:
    def __init__(self, root):
        self.root = root
        self.root.title("Film Ekle")
        self.root.geometry("600x400")

        self.film_adi_label = tk.Label(root, text="Film Adı:")
        self.film_adi_label.pack()
        self.film_adi_entry = tk.Entry(root)
        self.film_adi_entry.pack()

        self.yonetmen_label = tk.Label(root, text="Yönetmen:")
        self.yonetmen_label.pack()
        self.yonetmen_entry = tk.Entry(root)
        self.yonetmen_entry.pack()

        self.tur_label = tk.Label(root, text="Tür:")
        self.tur_label.pack()
        self.tur_entry = tk.Entry(root)
        self.tur_entry.pack()

        self.ekle_button = tk.Button(root, text="Ekle", command=self.film_ekle)
        self.ekle_button.pack()

    def film_ekle(self):
        film_adi = self.film_adi_entry.get()
        yonetmen = self.yonetmen_entry.get()
        tur = self.tur_entry.get()

        # Veritabanına film ekle
        connection = sqlite3.connect("veritabani.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Filmler (film_adi, yonetmen, tur) VALUES (?, ?, ?)", (film_adi, yonetmen, tur))
        connection.commit()
        connection.close()

        tk.messagebox.showinfo("Başarılı", "Film başarıyla eklendi.")
        self.root.destroy()  # Pencereyi kapat

# Filmleri görüntüleme penceresi
class FilmleriGoruntulePenceresi:
    def __init__(self, root):
        self.root = root
        self.root.title("Filmleri Görüntüle")
        self.root.geometry("600x400")

        self.arama_label = tk.Label(root, text="Film Adı:")
        self.arama_label.pack()
        self.arama_entry = tk.Entry(root)
        self.arama_entry.pack()

        self.ara_button = tk.Button(root, text="Ara", command=self.film_ara)
        self.ara_button.pack()

        self.film_liste = tk.Listbox(root, width=50, height=15)
        self.film_liste.pack()

        self.izle_button = tk.Button(root, text="İzle", command=self.film_izle)
        self.izle_button.pack()

        self.izleme_listeme_ekle_button = tk.Button(root, text="İzleme Listeme Ekle", command=self.izleme_listeme_ekle)
        self.izleme_listeme_ekle_button.pack()

        self.geri_don_button = tk.Button(root, text="Geri Dön", command=self.geri_don)
        self.geri_don_button.pack()

        # Tüm filmleri listele
        self.list_all_films()

    def list_all_films(self):
        # Tüm filmleri veritabanından al ve listele
        connection = sqlite3.connect("veritabani.db")
        cursor = connection.cursor()
        cursor.execute("SELECT film_adi, yonetmen, tur FROM Filmler")
        filmler = cursor.fetchall()
        connection.close()

        for film in filmler:
            self.film_liste.insert(tk.END, f"{film[0]} - {film[1]} - {film[2]}")

    def film_izle(self):
        tk.messagebox.showinfo("Film İzleniyor", "Film izleniyor...")

    def izleme_listeme_ekle(self):
        selected_film = self.film_liste.get(tk.ACTIVE)

        # İzleme listesine film ekle
        connection = sqlite3.connect("veritabani.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO IzlemeListesi (film_adi) VALUES (?)", (selected_film,))
        connection.commit()
        connection.close()

        tk.messagebox.showinfo("İzleme Listeme Eklendi", "İzleme listeme eklendi.")

    def geri_don(self):
        self.root.destroy()  # Pencereyi kapat

    def film_ara(self):
        film_adi = self.arama_entry.get()

        # Veritabanından film ara
        connection = sqlite3.connect("veritabani.db")
        cursor = connection.cursor()
        cursor.execute("SELECT film_adi, yonetmen, tur FROM Filmler WHERE film_adi LIKE ?", ('%' + film_adi + '%',))
        filmler = cursor.fetchall()
        connection.close()

        self.film_liste.delete(0, tk.END)  # Önceki listeyi temizle
        for film in filmler:
            self.film_liste.insert(tk.END, f"{film[0]} - {film[1]} - {film[2]}")

# İzleme listesi penceresi
class IzlemeListesiPenceresi:
    def __init__(self, root):
        self.root = root
        self.root.title("İzleme Listem")
        self.root.geometry("600x400")

        self.izleme_liste = tk.Listbox(root, width=50, height=15)
        self.izleme_liste.pack()

        self.izle_button = tk.Button(root, text="İzle", command=self.film_izle)
        self.izle_button.pack()

        self.kaldir_button = tk.Button(root, text="İzleme Listemden Kaldır", command=self.kaldir)
        self.kaldir_button.pack()

        self.geri_don_button = tk.Button(root, text="Geri Dön", command=self.geri_don)
        self.geri_don_button.pack()

        # İzleme listesini göster
        self.show_izleme_listesi()

    def show_izleme_listesi(self):
        # İzleme listesini veritabanından al ve göster
        connection = sqlite3.connect("veritabani.db")
        cursor = connection.cursor()
        cursor.execute("SELECT film_adi FROM IzlemeListesi")
        izleme_listesi = cursor.fetchall()
        connection.close()

        self.izleme_liste.delete(0, tk.END)  # Önceki listeyi temizle
        for film in izleme_listesi:
            self.izleme_liste.insert(tk.END, film[0])

    def film_izle(self):
        tk.messagebox.showinfo("Film İzleniyor", "Film izleniyor...")

    def kaldir(self):
        selected_film = self.izleme_liste.get(tk.ACTIVE)

        # İzleme listesinden filmi kaldır
        connection = sqlite3.connect("veritabani.db")
        cursor = connection.cursor()
        cursor.execute("DELETE FROM IzlemeListesi WHERE film_adi=?", (selected_film,))
        connection.commit()
        connection.close()

        tk.messagebox.showinfo("İzleme Listemden Kaldır", "İzleme listesinden kaldırıldı.")

    def geri_don(self):
        self.root.destroy()  # Pencereyi kapat

# Film değerlendirme penceresi
class FilmDegerlendirPenceresi:
    def __init__(self, root):
        self.root = root
        self.root.title("Film Değerlendir")
        self.root.geometry("600x400")

        self.film_liste = tk.Listbox(root, width=50, height=10)
        self.film_liste.pack()

        self.degerlendir_button = tk.Button(root, text="Değerlendir", command=self.film_degerlendir)
        self.degerlendir_button.pack()

        self.puan_label = tk.Label(root, text="Puan Ver (1-10):")
        self.puan_label.pack()
        self.puan_entry = tk.Entry(root)
        self.puan_entry.pack()

        self.ortalama_label = tk.Label(root, text="Ortalama Puan:")
        self.ortalama_label.pack()
        self.ortalama_puan_label = tk.Label(root, text="")
        self.ortalama_puan_label.pack()

        # İzleme listesinden filmleri al ve listele
        connection = sqlite3.connect("veritabani.db")
        cursor = connection.cursor()
        cursor.execute("SELECT film_adi FROM Filmler")
        filmler = cursor.fetchall()
        connection.close()

        for film in filmler:
            self.film_liste.insert(tk.END, film[0])

    def film_degerlendir(self):
        selected_film = self.film_liste.get(tk.ACTIVE)
        puan = self.puan_entry.get()

        if puan.isdigit() and 1 <= int(puan) <= 10:
            # Puanı veritabanına kaydet
            connection = sqlite3.connect("veritabani.db")
            cursor = connection.cursor()
            cursor.execute("INSERT INTO FilmDegerlendirme (film_adi, puan) VALUES (?, ?)", (selected_film, puan))
            connection.commit()

            # Ortalama puanı hesapla ve göster
            cursor.execute("SELECT AVG(puan) FROM FilmDegerlendirme WHERE film_adi=?", (selected_film,))
            ortalama_puan = cursor.fetchone()[0]
            connection.close()

            if ortalama_puan:
                self.ortalama_puan_label.config(text=f"Ortalama Puan: {ortalama_puan:.2f}")
            else:
                self.ortalama_puan_label.config(text="Henüz değerlendirme yapılmadı.")
        else:
            tk.messagebox.showerror("Hata", "Geçersiz puan. Lütfen 1 ile 10 arasında bir sayı girin.")


# İçerikleri görüntüleme penceresi
class IcerikleriGoruntulePenceresi:
    def __init__(self, root):
        self.root = root
        self.root.title("İçerikleri Görüntüle")
        self.root.geometry("600x400")

        self.arama_label = tk.Label(root, text="İçerik Adı:")
        self.arama_label.pack()
        self.arama_entry = tk.Entry(root)
        self.arama_entry.pack()

        self.ara_button = tk.Button(root, text="Ara", command=self.icerik_ara)
        self.ara_button.pack()

        self.icerik_liste = tk.Listbox(root, width=50, height=15)
        self.icerik_liste.pack()

        self.geri_don_button = tk.Button(root, text="Geri Dön", command=self.geri_don)
        self.geri_don_button.pack()

        # Tüm içerikleri listele
        self.list_all_icerikler()

    def list_all_icerikler(self):
        # Tüm içerikleri veritabanından al ve listele
        connection = sqlite3.connect("veritabani.db")
        cursor = connection.cursor()
        cursor.execute("SELECT icerik_adi, sure, tur FROM Icerikler")
        icerikler = cursor.fetchall()
        connection.close()

        for icerik in icerikler:
            self.icerik_liste.insert(tk.END, f"{icerik[0]} - Süre: {icerik[1]} dakika - Tür: {icerik[2]}")

    def icerik_ara(self):
        icerik_adi = self.arama_entry.get()

        # Veritabanından içerik ara
        connection = sqlite3.connect("veritabani.db")
        cursor = connection.cursor()
        cursor.execute("SELECT icerik_adi, sure, tur FROM Icerikler WHERE icerik_adi LIKE ?", ('%' + icerik_adi + '%',))
        icerikler = cursor.fetchall()
        connection.close()

        self.icerik_liste.delete(0, tk.END)  # Önceki listeyi temizle
        for icerik in icerikler:
            self.icerik_liste.insert(tk.END, f"{icerik[0]} - Süre: {icerik[1]} dakika - Tür: {icerik[2]}")

    def geri_don(self):
        self.root.destroy()  # Pencereyi kapat
# İçerikleri görüntüleme penceresi
class IcerikleriGoruntulePenceresi:
    def __init__(self, root):
        self.root = root
        self.root.title("İçerikleri Görüntüle")
        self.root.geometry("600x400")

        self.arama_label = tk.Label(root, text="İçerik Adı:")
        self.arama_label.pack()
        self.arama_entry = tk.Entry(root)
        self.arama_entry.pack()

        self.ara_button = tk.Button(root, text="Ara", command=self.icerik_ara)
        self.ara_button.pack()

        self.icerik_liste = tk.Listbox(root, width=50, height=15)
        self.icerik_liste.pack()

        self.geri_don_button = tk.Button(root, text="Geri Dön", command=self.geri_don)
        self.geri_don_button.pack()

        # Tüm içerikleri listele
        self.list_all_icerikler()

    def list_all_icerikler(self):
        # Tüm içerikleri veritabanından al ve listele
        connection = sqlite3.connect("veritabani.db")
        cursor = connection.cursor()
        cursor.execute("SELECT icerik_adi, sure, tur FROM Icerikler")
        icerikler = cursor.fetchall()
        connection.close()

        for icerik in icerikler:
            self.icerik_liste.insert(tk.END, f"{icerik[0]} - Süre: {icerik[1]} dakika - Tür: {icerik[2]}")

    def icerik_ara(self):
        icerik_adi = self.arama_entry.get()

        # Veritabanından içerik ara
        connection = sqlite3.connect("veritabani.db")
        cursor = connection.cursor()
        cursor.execute("SELECT icerik_adi, sure, tur FROM Icerikler WHERE icerik_adi LIKE ?", ('%' + icerik_adi + '%',))
        icerikler = cursor.fetchall()
        connection.close()

        self.icerik_liste.delete(0, tk.END)  # Önceki listeyi temizle
        for icerik in icerikler:
            self.icerik_liste.insert(tk.END, f"{icerik[0]} - Süre: {icerik[1]} dakika - Tür: {icerik[2]}")

    def geri_don(self):
        self.root.destroy()  # Pencereyi kapat


# Ana sayfa
class MainPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Ana Sayfa")
        self.root.geometry("500x400")

        # Butonların boyutunu ve yerleşimini ayarla
        button_width = 20
        button_height = 2

        self.film_ekle_button = tk.Button(root, text="Film Ekle", command=self.open_film_ekle_penceresi, width=button_width, height=button_height)
        self.film_ekle_button.place(relx=0.5, rely=0.2, anchor='center')

        self.filmleri_goruntule_button = tk.Button(root, text="Filmleri Görüntüle", command=self.open_filmleri_goruntule_penceresi, width=button_width, height=button_height)
        self.filmleri_goruntule_button.place(relx=0.5, rely=0.35, anchor='center')

        self.icerikleri_goruntule_button = tk.Button(root, text="İçerikleri Görüntüle", command=self.open_icerikleri_goruntule_penceresi, width=button_width, height=button_height)
        self.icerikleri_goruntule_button.place(relx=0.5, rely=0.5, anchor='center')

        self.izleme_listem_button = tk.Button(root, text="İzleme Listem", command=self.open_izleme_listesi_penceresi, width=button_width, height=button_height)
        self.izleme_listem_button.place(relx=0.5, rely=0.65, anchor='center')

        self.film_degerlendir_button = tk.Button(root, text="Film Değerlendir", command=self.open_film_degerlendir_penceresi, width=button_width, height=button_height)
        self.film_degerlendir_button.place(relx=0.5, rely=0.8, anchor='center')

        self.back_button = tk.Button(root, text="Geri Dön", command=self.go_back, width=button_width, height=button_height)
        self.back_button.place(relx=1, rely=1, anchor='se')


    def open_film_ekle_penceresi(self):
        film_ekle_penceresi = tk.Toplevel(self.root)
        FilmEklePenceresi(film_ekle_penceresi)

    def open_filmleri_goruntule_penceresi(self):
        filmleri_goruntule_penceresi = tk.Toplevel(self.root)
        FilmleriGoruntulePenceresi(filmleri_goruntule_penceresi)

    def open_izleme_listesi_penceresi(self):
        izleme_listesi_penceresi = tk.Toplevel(self.root)
        IzlemeListesiPenceresi(izleme_listesi_penceresi)

    def open_film_degerlendir_penceresi(self):
        film_degerlendir_penceresi = tk.Toplevel(self.root)
        FilmDegerlendirPenceresi(film_degerlendir_penceresi)

    def open_icerikleri_goruntule_penceresi(self):
        icerikleri_goruntule_penceresi = tk.Toplevel(self.root)
        IcerikleriGoruntulePenceresi(icerikleri_goruntule_penceresi)


    def go_back(self):
        self.root.destroy()  # Ana sayfayı kapat
        login_page = tk.Tk()
        UserLoginApp(login_page)
        login_page.mainloop()

# Kullanıcı Giriş Sayfası
class UserLoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kullanıcı Giriş")
        self.root.geometry("400x300")

        self.username_label = tk.Label(root, text="Kullanıcı Adı:")
        self.username_label.pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        self.password_label = tk.Label(root, text="Şifre:")
        self.password_label.pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(root, text="Giriş Yap", command=self.login)
        self.login_button.pack()

        self.register_button = tk.Button(root, text="Kayıt Ol", command=self.register)
        self.register_button.pack()

        self.help_button = tk.Button(root, text="Kullanım Kılavuzu", command=self.show_help)
        self.help_button.place(relx=0, rely=1, anchor='sw')

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Kullanıcı adı ve şifre kontrolü
        connection = sqlite3.connect("veritabani.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Kullanicilar WHERE kullanici_adi=? AND sifre=?", (username, password))
        user = cursor.fetchone()
        connection.close()

        if user:
            messagebox.showinfo("Giriş Başarılı", f"Hoş Geldiniz, {username}!")
            self.open_main_page()
        else:
            messagebox.showerror("Hata", "Geçersiz kullanıcı adı veya şifre!")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Kullanıcıyı veritabanına ekle
        connection = sqlite3.connect("veritabani.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Kullanicilar (kullanici_adi, sifre) VALUES (?, ?)", (username, password))
        connection.commit()
        connection.close()

        messagebox.showinfo("Başarılı", "Kayıt işlemi başarıyla tamamlandı.")

    def open_main_page(self):
        # Ana sayfaya yönlendirme
        self.root.destroy()  # Giriş sayfasını kapat
        main_page = tk.Tk()
        MainPage(main_page)
        main_page.mainloop()

    def show_help(self):
        help_text = """
Kullanım Kılavuzu:

1. Kullanıcı Giriş Sayfası:
    - Kullanıcı adı ve şifrenizi ilgili alanlara girin.
    - "Giriş Yap" butonuna tıklayarak sisteme giriş yapın.
    - Eğer daha önce kayıt olmadıysanız, "Kayıt Ol" butonuna tıklayarak yeni bir hesap oluşturabilirsiniz.
    - Yardım almak için "Kullanım Kılavuzu" butonuna tıklayabilirsiniz.

2. Ana Sayfa:
    - "Film Ekle" butonuna tıklayarak yeni bir film ekleyebilirsiniz.
    - "Filmleri Görüntüle" butonuna tıklayarak mevcut filmleri listeleyebilir ve izleme listenize ekleyebilirsiniz.
    - "İçerikleri Görüntüle" butonuna tıklayarak mevcut içerikleri listeleyebilirsiniz.
    - "İzleme Listem" butonuna tıklayarak izleme listenizi görüntüleyebilir ve izleme listesinden filmleri kaldırabilirsiniz.
    - "Film Değerlendir" butonuna tıklayarak filmleri değerlendirebilir ve puanlayabilirsiniz.
    - "Geri Dön" butonuna tıklayarak giriş sayfasına geri dönebilirsiniz.
        """
        messagebox.showinfo("Kullanım Kılavuzu", help_text)



if __name__ == "__main__":
    # Veritabanı bağlantısını oluştur
    connection = sqlite3.connect("veritabani.db")
    cursor = connection.cursor()

    # Veritabanı bağlantısını oluştur
    connection = sqlite3.connect("veritabani.db")
    cursor = connection.cursor()

    # Tabloları oluştur
    cursor.execute("""CREATE TABLE IF NOT EXISTS Filmler (
                        film_id INTEGER PRIMARY KEY,
                        film_adi TEXT,
                        yonetmen TEXT,
                        tur TEXT
                    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS Kullanicilar (
                        kullanici_id INTEGER PRIMARY KEY,
                        kullanici_adi TEXT,
                        sifre TEXT,
                        izleme_gecmisi TEXT
                    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS Icerikler (
                         icerik_id INTEGER PRIMARY KEY,
                         icerik_adi TEXT,
                         sure INTEGER,
                         tur TEXT
                    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS IzlemeListesi (
                         id INTEGER PRIMARY KEY,
                         film_adi TEXT
                    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS FilmDegerlendirme (
                        id INTEGER PRIMARY KEY,
                        film_adi TEXT,
                        puan INTEGER
                    )""")

    # Veritabanına örnek kullanıcı ekle
    cursor.execute("INSERT INTO Kullanicilar (kullanici_adi, sifre) VALUES (?, ?)", ("kullanici1", "sifre1"))

    # Örnek filmleri ekle
    films = [
        ("Interstellar", "Christopher Nolan", "Bilim Kurgu"),
        ("Inception", "Christopher Nolan", "Bilim Kurgu"),
        ("The Shawshank Redemption", "Frank Darabont", "Drama"),
        ("The Godfather", "Francis Ford Coppola", "Drama"),
        ("The Dark Knight", "Christopher Nolan", "Aksiyon"),
        ("Forrest Gump", "Robert Zemeckis", "Drama"),
        ("Pulp Fiction", "Quentin Tarantino", "Suç"),
        ("The Matrix", "Lana Wachowski", "Bilim Kurgu"),
        ("Fight Club", "David Fincher", "Drama"),
        ("The Lord of the Rings: The Fellowship of the Ring", "Peter Jackson", "Fantastik"),
        ("The Lord of the Rings: The Two Towers", "Peter Jackson", "Fantastik"),
        ("The Lord of the Rings: The Return of the King", "Peter Jackson", "Fantastik"),
        ("Inglourious Basterds", "Quentin Tarantino", "Savaş"),
        ("The Godfather: Part II", "Francis Ford Coppola", "Drama"),
        ("The Shawshank Redemption", "Frank Darabont", "Drama"),
        ("The Dark Knight Rises", "Christopher Nolan", "Aksiyon"),
        ("The Green Mile", "Frank Darabont", "Drama"),
        ("Forrest Gump", "Robert Zemeckis", "Drama"),
        ("Pulp Fiction", "Quentin Tarantino", "Suç"),
        ("The Matrix", "Lana Wachowski", "Bilim Kurgu"),
        ("Fight Club", "David Fincher", "Drama"),
        ("The Lord of the Rings: The Fellowship of the Ring", "Peter Jackson", "Fantastik"),
        ("The Lord of the Rings: The Two Towers", "Peter Jackson", "Fantastik"),
        ("The Lord of the Rings: The Return of the King", "Peter Jackson", "Fantastik"),
        ("Inglourious Basterds", "Quentin Tarantino", "Savaş"),
        ("The Godfather: Part II", "Francis Ford Coppola", "Drama"),
        ("The Shawshank Redemption", "Frank Darabont", "Drama"),
        ("The Dark Knight Rises", "Christopher Nolan", "Aksiyon"),
        ("The Green Mile", "Frank Darabont", "Drama"),
        ("Forrest Gump", "Robert Zemeckis", "Drama"),
        ("Pulp Fiction", "Quentin Tarantino", "Suç"),
        ("The Matrix", "Lana Wachowski", "Bilim Kurgu"),
        ("Fight Club", "David Fincher", "Drama"),
        ("The Lord of the Rings: The Fellowship of the Ring", "Peter Jackson", "Fantastik"),
        ("The Lord of the Rings: The Two Towers", "Peter Jackson", "Fantastik"),
        ("The Lord of the Rings: The Return of the King", "Peter Jackson", "Fantastik"),
        ("Inglourious Basterds", "Quentin Tarantino", "Savaş"),
        ("The Godfather: Part II", "Francis Ford Coppola", "Drama"),
        ("The Shawshank Redemption", "Frank Darabont", "Drama"),
        ("The Dark Knight Rises", "Christopher Nolan", "Aksiyon"),
        ("The Green Mile", "Frank Darabont", "Drama"),
        ("Forrest Gump", "Robert Zemeckis", "Drama"),
        ("Pulp Fiction", "Quentin Tarantino", "Suç"),
        ("The Matrix", "Lana Wachowski", "Bilim Kurgu"),
        ("Fight Club", "David Fincher", "Drama"),
        ("The Lord of the Rings: The Fellowship of the Ring", "Peter Jackson", "Fantastik"),
        ("The Lord of the Rings: The Two Towers", "Peter Jackson", "Fantastik"),
        ("The Lord of the Rings: The Return of the King", "Peter Jackson", "Fantastik"),
        ("Inglourious Basterds", "Quentin Tarantino", "Savaş"),
        ("The Godfather: Part II", "Francis Ford Coppola", "Drama"),
        ("The Shawshank Redemption", "Frank Darabont", "Drama"),
        ("The Dark Knight Rises", "Christopher Nolan", "Aksiyon"),
        ("The Green Mile", "Frank Darabont", "Drama"),
        ("Forrest Gump", "Robert Zemeckis", "Drama"),
        ("Pulp Fiction", "Quentin Tarantino", "Suç"),
        ("The Matrix", "Lana Wachowski", "Bilim Kurgu"),
        ("Fight Club", "David Fincher", "Drama"),
        ("The Lord of the Rings: The Fellowship of the Ring", "Peter Jackson", "Fantastik"),
        ("The Lord of the Rings: The Two Towers", "Peter Jackson", "Fantastik"),
        ("The Lord of the Rings: The Return of the King", "Peter Jackson", "Fantastik"),
        ("Inglourious Basterds", "Quentin Tarantino", "Savaş"),
        ("The Godfather: Part II", "Francis Ford Coppola", "Drama"),
        ("The Shawshank Redemption", "Frank Darabont", "Drama"),
        ("The Dark Knight Rises", "Christopher Nolan", "Aksiyon"),
        ("The Green Mile", "Frank Darabont", "Drama"),
        ("Forrest Gump", "Robert Zemeckis", "Drama"),
        ("Pulp Fiction", "Quentin Tarantino", "Suç"),
        ("The Matrix", "Lana Wachowski", "Bilim Kurgu"),
        ("Fight Club", "David Fincher", "Drama"),
        ("The Lord of the Rings: The Fellowship of the Ring", "Peter Jackson", "Fantastik"),
        ("The Lord of the Rings: The Two Towers", "Peter Jackson", "Fantastik"),
        ("The Lord of the Rings: The Return of the King", "Peter Jackson", "Fantastik"),
        ("Inglourious Basterds", "Quentin Tarantino", "Savaş"),
        ("The Godfather: Part II", "Francis Ford Coppola", "Drama"),
        ("The Shawshank Redemption", "Frank Darabont", "Drama"),
        ("The Dark Knight Rises", "Christopher Nolan", "Aksiyon"),
        ("The Green Mile", "Frank Darabont", "Drama"),
        ("Forrest Gump", "Robert Zemeckis", "Drama"),
        ("Pulp Fiction", "Quentin Tarantino", "Suç"),
        ("The Matrix", "Lana Wachowski", "Bilim Kurgu"),
        ("Fight Club", "David Fincher", "Drama")
    ]

    cursor.executemany("INSERT INTO Filmler (film_adi, yonetmen, tur) VALUES (?, ?, ?)", films)

    # Örnek içerikleri ekle
    icerikler = [
        ("Breaking Bad", 50, "Dizi"),
        ("Game of Thrones", 60, "Dizi"),
        ("The Witcher", 45, "Dizi"),
        ("Lord of the Rings", 180, "Film"),
        ("Harry Potter", 150, "Film"),
        ("Breaking Bad", 50, "Dizi"),
        ("Game of Thrones", 60, "Dizi"),
        ("The Witcher", 45, "Dizi"),
        ("Lord of the Rings", 180, "Film"),
        ("Harry Potter", 150, "Film"),
        ("Friends", 22, "Dizi"),
        ("The Office", 22, "Dizi"),
        ("Stranger Things", 50, "Dizi"),
        ("The Crown", 60, "Dizi"),
        ("Narcos", 50, "Dizi"),
        ("Sherlock", 90, "Dizi"),
        ("Black Mirror", 60, "Dizi"),
        ("Money Heist", 50, "Dizi"),
        ("The Mandalorian", 40, "Dizi"),
        ("The Walking Dead", 45, "Dizi"),
        ("Ozark", 60, "Dizi"),
        ("Peaky Blinders", 60, "Dizi"),
        ("Breaking Bad", 49, "Film"),
        ("The Godfather", 175, "Film"),
        ("The Dark Knight", 152, "Film"),
        ("Pulp Fiction", 154, "Film"),
        ("Forrest Gump", 142, "Film"),
        ("Inception", 148, "Film"),
        ("The Matrix", 136, "Film"),
        ("Fight Club", 139, "Film"),
        ("The Lord of the Rings: The Fellowship of the Ring", 178, "Film"),
        ("The Shawshank Redemption", 142, "Film"),
        ("The Lord of the Rings: The Two Towers", 179, "Film"),
        ("The Lord of the Rings: The Return of the King", 201, "Film"),
        ("The Godfather: Part II", 202, "Film"),
        ("The Dark Knight Rises", 164, "Film"),
        ("The Silence of the Lambs", 118, "Film"),
        ("The Green Mile", 189, "Film"),
        ("The Godfather: Part III", 162, "Film"),
        ("The Matrix Reloaded", 138, "Film"),
        ("Inglourious Basterds", 153, "Film"),
        ("Goodfellas", 146, "Film"),
        ("Schindler's List", 195, "Film"),
        ("The Lord of the Rings: The Two Towers", 179, "Film"),
        ("The Lord of the Rings: The Return of the King", 201, "Film"),
        ("The Godfather: Part II", 202, "Film"),
        ("The Dark Knight Rises", 164, "Film"),
        ("The Silence of the Lambs", 118, "Film"),
        ("The Green Mile", 189, "Film"),
        ("The Godfather: Part III", 162, "Film"),
        ("The Matrix Reloaded", 138, "Film"),
        ("Inglourious Basterds", 153, "Film"),
        ("Goodfellas", 146, "Film"),
        ("Schindler's List", 195, "Film")
    ]

    cursor.executemany("INSERT INTO Icerikler (icerik_adi, sure, tur) VALUES (?, ?, ?)", icerikler)

    # Değişiklikleri kaydet
    connection.commit()

    # Veritabanı bağlantısını kapat
    connection.close()

    # Ana uygulamayı başlat
    root = tk.Tk()
    app = UserLoginApp(root)
    root.mainloop()
