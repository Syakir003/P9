import mysql.connector

def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="uas_pbo_pmi"
    )

def get_pendaftaran_pending():
    db = connect()
    cur = db.cursor()
    cur.execute("""
        SELECT
        pd.id_daftar,
        p.nama_pendonor,
        p.nik,
        p.gol_darah,
        pd.tanggal_daftar,
        pd.status
    FROM pendaftaran_donor pd
    JOIN pendonor p ON pd.id_pendonor = p.id_pendonor
    WHERE pd.status = 'menunggu'
    ORDER BY pd.tanggal_daftar DESC;
    """)
    data = cur.fetchall()
    cur.close()
    db.close()
    return data


def update_status_pendaftaran(id_pendaftaran, status):
    db = connect()
    cur = db.cursor()
    cur.execute("""
        UPDATE pendaftaran_donor
        SET status = %s
        WHERE id_daftar = %s
    """, (status, id_pendaftaran))
    db.commit()
    cur.close()
    db.close()
    
    
def terima_pendaftaran(id_daftar):
    db = connect()
    cur = db.cursor()

    # Ambil id_pendonor
    cur.execute("""
        SELECT id_pendonor
        FROM pendaftaran_donor
        WHERE id_daftar = %s
    """, (id_daftar,))
    id_pendonor = cur.fetchone()[0]

    # Update status pendaftaran
    cur.execute("""
        UPDATE pendaftaran_donor
        SET status = 'diterima'
        WHERE id_daftar = %s
    """, (id_daftar,))

    # Auto buat jadwal donor (contoh: H+1 jam 08:00)
    cur.execute("""
        INSERT INTO jadwal_donor
        (id_pendonor, tanggal_donor, waktu_donor, lokasi)
        VALUES (%s, DATE_ADD(CURDATE(), INTERVAL 1 DAY), '08:00:00', 'PMI Kota')
    """, (id_pendonor,))

    db.commit()
    cur.close()
    db.close()

