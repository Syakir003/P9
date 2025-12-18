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
    
    
from datetime import date, time

def terima_pendaftaran(id_daftar):
    db = connect()
    cur = db.cursor()

    # 1. Ambil id_pendonor
    cur.execute("""
        SELECT id_pendonor
        FROM pendaftaran_donor
        WHERE id_daftar = %s
    """, (id_daftar,))
    
    result = cur.fetchone()
    if not result:
        cur.close()
        db.close()
        return

    id_pendonor = result[0]

    # 2. Update status pendaftaran
    cur.execute("""
        UPDATE pendaftaran_donor
        SET status = 'diterima'
        WHERE id_daftar = %s
    """, (id_daftar,))

    # 3. Insert jadwal donor
    cur.execute("""
        INSERT INTO jadwal_donor
        (id_pendonor, tanggal_donor, waktu_donor, lokasi, status)
        VALUES (%s, %s, %s, %s, 'terjadwal')
    """, (
        id_pendonor,
        date.today(),          # tanggal otomatis
        time(9, 0),            # jam default 09:00
        "PMI Kota"             # lokasi default
    ))

    db.commit()
    cur.close()
    db.close()

