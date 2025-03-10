from database import insert_sample_data, filter_arsip, insert_arsip, update_arsip, delete_arsip

# 1. Tambahkan data contoh ke database
insert_sample_data()

# 2. Coba filter berdasarkan kategori
hasil_filter = filter_arsip(kategori="AV")
print("Hasil filter kategori 'AV':", hasil_filter)

# 3. Tambahkan data baru
insert_arsip(4, "Boks-04", "Berkas-004", "D321", "Indeks D", "Informasi D", "2022-2027", "Aktif", "T", "Deskripsi D")
print("Data baru berhasil ditambahkan!")

# 4. Edit data arsip
update_arsip(1, "Boks-01-Updated", "Berkas-001-Updated", "A123", "Indeks A Updated", "Informasi A Updated", "2020-2030", "Aktif", "AV", "Deskripsi A Updated")
print("Data berhasil diperbarui!")

# 5. Hapus data arsip
delete_arsip(2)
print("Data berhasil dihapus!")
