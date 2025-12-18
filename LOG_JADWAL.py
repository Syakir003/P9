import mysql.connector
def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="uas_pbo_pmi"
    )
    
def get_jadwal_donor():
    db = connect()
    cur = db.cursor()

    cur.execute("""
        SELECT
            jd.id_jadwal,
            p.nama_pendonor,
            p.gol_darah,
            jd.tanggal_donor,
            jd.waktu_donor,
            jd.lokasi,
            jd.status
        FROM jadwal_donor jd
        JOIN pendonor p ON jd.id_pendonor = p.id_pendonor
        ORDER BY jd.tanggal_donor, jd.waktu_donor
    """)

    data = cur.fetchall()
    cur.close()
    db.close()
    return data

