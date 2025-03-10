import sqlite3

# Fungsi koneksi ke database
def connect_db():
    return sqlite3.connect("arsip.db")

# Fungsi membuat tabel jika belum ada
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS arsip (
            no_urut INTEGER PRIMARY KEY,
            no_boks TEXT NOT NULL,
            no_berkas TEXT NOT NULL,
            kode_klasifikasi TEXT NOT NULL,
            indeks TEXT NOT NULL,
            informasi TEXT NOT NULL,
            kurun_waktu TEXT NOT NULL,
            jangka_simpan TEXT CHECK(jangka_simpan IN ('Aktif', 'Inaktif')),
            kategori TEXT CHECK(kategori IN ('AV', 'AT', 'R', 'T')),
            deskripsi TEXT
        )
    """)
    conn.commit()
    conn.close()

# Fungsi menambahkan data
def insert_arsip(no_urut, no_boks, no_berkas, kode_klasifikasi, indeks, informasi, kurun_waktu, jangka_simpan, kategori, deskripsi):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO arsip (no_urut, no_boks, no_berkas, kode_klasifikasi, indeks, informasi, kurun_waktu, jangka_simpan, kategori, deskripsi)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (no_urut, no_boks, no_berkas, kode_klasifikasi, indeks, informasi, kurun_waktu, jangka_simpan, kategori, deskripsi))
    conn.commit()
    conn.close()

# Fungsi memperbarui data
def update_arsip(no_urut, no_boks, no_berkas, kode_klasifikasi, indeks, informasi, kurun_waktu, jangka_simpan, kategori, deskripsi):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE arsip
        SET no_boks=?, no_berkas=?, kode_klasifikasi=?, indeks=?, informasi=?, kurun_waktu=?, jangka_simpan=?, kategori=?, deskripsi=?
        WHERE no_urut=?
    """, (no_boks, no_berkas, kode_klasifikasi, indeks, informasi, kurun_waktu, jangka_simpan, kategori, deskripsi, no_urut))
    conn.commit()
    conn.close()

# Fungsi menghapus data
def delete_arsip(no_urut):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM arsip WHERE no_urut=?", (no_urut,))
    conn.commit()
    conn.close()

# Fungsi memfilter data
def filter_arsip(kategori=None, jangka_simpan=None):
    conn = connect_db()
    cursor = conn.cursor()
    query = "SELECT * FROM arsip WHERE 1=1"
    params = []
    
    if kategori:
        query += " AND kategori=?"
        params.append(kategori)
    if jangka_simpan:
        query += " AND jangka_simpan=?"
        params.append(jangka_simpan)
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

# Fungsi menambahkan data contoh
def insert_sample_data():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.executemany("""
        INSERT INTO arsip (no_urut, no_boks, no_berkas, kode_klasifikasi, indeks, informasi, kurun_waktu, jangka_simpan, kategori, deskripsi) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        (1, "Boks-01", "Berkas-001", "A123", "Indeks A", "Informasi A", "2020-2025", "Aktif", "AV", "Deskripsi A"),
        (2, "Boks-02", "Berkas-002", "B456", "Indeks B", "Informasi B", "2021-2026", "Inaktif", "AT", "Deskripsi B"),
        (3, "Boks-03", "Berkas-003", "C789", "Indeks C", "Informasi C", "2019-2024", "Aktif", "R", "Deskripsi C"),
    ])
    conn.commit()
    conn.close()
    print("Data contoh berhasil ditambahkan!")

# Jalankan pembuatan tabel saat file dieksekusi
create_table()
