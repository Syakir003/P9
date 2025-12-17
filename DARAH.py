import mysql.connector
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

def get_stok_kritis(threshold=3):
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM darah WHERE stok <= %s", (threshold,))
        kritis = cursor.fetchone()[0] or 0
        return kritis
    finally:
        cursor.close()
        conn.close()

def get_stok_kadaluarsa(days=7):
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM darah WHERE tgl_kadaluarsa <= DATE_ADD(CURDATE(), INTERVAL %s DAY)", (days,))
        kadaluarsa = cursor.fetchone()[0] or 0
        return kadaluarsa
    finally:
        cursor.close()
        conn.close()

def get_all_stok():
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM darah")
        rows = cursor.fetchall()
        return rows
    finally:
        cursor.close()
        conn.close()
