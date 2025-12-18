import mysql.connector
import datetime

def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="uas_pbo_pmi"
    )
    

def get_total_stok():
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT SUM(stok) AS total_stok FROM darah")
        total = cursor.fetchone()[0] or 0
        return total
    finally:
        cursor.close()
        conn.close()

def get_stok_kadaluarsa(days=7):
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT SUM(stok)
            FROM darah
            WHERE tgl_kadaluarsa <= DATE_ADD(CURDATE(), INTERVAL %s DAY)
        """, (days,))
        return cursor.fetchone()[0] or 0
    finally:
        cursor.close()
        conn.close()


def get_all_stok():
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT
                id_darah AS no_kantong,
                gol_darah,
                RIGHT(gol_darah, 1) AS rhesus,
                tgl_donor,
                tgl_kadaluarsa,
                status_darah,
                '-' AS lokasi,
                '-' AS aksi
            FROM darah
            ORDER BY tgl_kadaluarsa ASC
        """)
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

        
def get_stok_kritis():
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM darah WHERE stok < 100")
    total = cursor.fetchone()[0]
    cursor.close()
    db.close()
    return total
        
def stok_kadaluarsa():
    db = connect()
    cursor = db.cursor()
    cursor.execute("""
        SELECT SUM(stok)
        FROM darah
        WHERE DATEDIFF(tgl_kadaluarsa, CURDATE()) <= 7
    """)
    total = cursor.fetchone()[0] or 0
    cursor.close()
    db.close()
    return total

        

def laporan_darah():
    db = connect()
    cursor = db.cursor()

    query = """
    SELECT 
        gol_darah,
        RIGHT(gol_darah, 1) AS rhesus,
        stok,
        CASE
            WHEN stok >= 100 THEN 'Aman'
            WHEN stok >= 50 THEN 'Kritis'
            ELSE 'Darurat'
        END AS status,
        CASE
            WHEN DATEDIFF(tgl_kadaluarsa, CURDATE()) < 7 THEN 'Ya'
            ELSE 'Tidak'
        END AS hampir_kadaluarsa,
        tgl_kadaluarsa
    FROM darah
    ORDER BY gol_darah
    """

    cursor.execute(query)
    result = cursor.fetchall()

    cursor.close()
    db.close()
    return result

