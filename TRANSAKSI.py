import mysql.connector
from datetime import date
class PendaftaranDonor:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="uas_pbo_pmi"
        )
        self.cursor = self.conn.cursor()
        
    def cek_daftar_aktif(self, id_pendonor):
        sql = """
        SELECT COUNT(*)
        FROM pendaftaran_donor
        WHERE id_pendonor = %s
        AND status = 'menunggu'
        """
        self.cursor.execute(sql, (id_pendonor,))
        return self.cursor.fetchone()[0]


    def simpan_pendaftaran(self, id_pendonor, berat_badan):
        sql = """
        INSERT INTO pendaftaran_donor
        (id_pendonor, berat_badan)
        VALUES (%s, %s)
        """
        self.cursor.execute(sql, (id_pendonor, berat_badan))
        self.conn.commit()
        
        
def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="uas_pbo_pmi"
    )


def get_donor_masuk_hari_ini():
    db = connect()
    cur = db.cursor()
    cur.execute("""
        SELECT COUNT(*) 
        FROM transaksi
        WHERE DATE(tanggal_transaksi) = CURDATE()
        AND tipe_transaksi = 'MASUK'
    """)
    total = cur.fetchone()[0] or 0
    cur.close()
    db.close()
    return total



def get_darah_keluar_hari_ini():
    db = connect()
    cur = db.cursor()
    cur.execute("""
        SELECT COUNT(*) 
        FROM transaksi
        WHERE DATE(tanggal_transaksi) = CURDATE()
        AND tipe_transaksi = 'KELUAR'
    """)
    total = cur.fetchone()[0] or 0
    cur.close()
    db.close()
    return total



def get_total_transaksi_bulan_ini():
    db = connect()
    cur = db.cursor()
    cur.execute("""
        SELECT COUNT(*) 
        FROM transaksi
        WHERE MONTH(tanggal_transaksi) = MONTH(CURDATE())
        AND YEAR(tanggal_transaksi) = YEAR(CURDATE())
    """)
    total = cur.fetchone()[0] or 0
    cur.close()
    db.close()
    return total



def get_riwayat_transaksi():
    db = connect()
    cur = db.cursor()
    cur.execute("""
        SELECT
            t.id_transaksi,
            t.tanggal_transaksi,
            t.tipe_transaksi,
            d.gol_darah,
            t.jumlah,
            t.id_petugas
        FROM transaksi t
        JOIN darah d ON t.id_darah = d.id_darah
        ORDER BY t.tanggal_transaksi DESC
    """)
    rows = cur.fetchall()
    cur.close()
    db.close()
    return rows


def get_riwayat_transaksi_masuk():
    db = connect()
    cur = db.cursor()
    cur.execute("""
        SELECT
            t.id_transaksi,
            t.tanggal_transaksi,
            t.tipe_transaksi,
            darah.gol_darah,
            t.jumlah,
            p.nama_pendonor,
            t.status,
            ''
        FROM transaksi t
        LEFT JOIN darah d ON t.id_darah = darah.id_darah
        LEFT JOIN pendonor p ON t.id_pendonor = p.id_pendonor
        WHERE t.tipe_transaksi = 'MASUK'
        ORDER BY t.tanggal_transaksi DESC
    """)
    rows = cur.fetchall()
    cur.close()
    db.close()
    return rows


def get_riwayat_transaksi_keluar():
    db = connect()
    cur = db.cursor()
    cur.execute("""
        SELECT
            t.id_transaksi,
            t.tanggal_transaksi,
            t.tipe_transaksi,
            darah.gol_darah,
            t.jumlah,
            r.nama_rs,
            t.status,
            ''
        FROM transaksi t
        LEFT JOIN darah d ON t.id_darah = darah.id_darah
        LEFT JOIN rumah_sakit r ON t.id_rs = r.id_rs
        WHERE t.tipe_transaksi = 'KELUAR'
        ORDER BY t.tanggal_transaksi DESC
    """)
    rows = cur.fetchall()
    cur.close()
    db.close()
    return rows



def darah_masuk_today():
    db = connect()
    cur = db.cursor()
    cur.execute("""
        SELECT
            t.id_transaksi,
            d.gol_darah,
            t.jumlah,
            t.tanggal_transaksi
        FROM transaksi t
        JOIN darah d ON t.id_darah = d.id_darah
        WHERE t.tipe_transaksi = 'MASUK'
        AND t.tanggal_transaksi = CURDATE()
    """)
    data = cur.fetchall()
    cur.close()
    db.close()
    return data

def cek_daftar_aktif(self, id_pendonor):
    sql = """
    SELECT COUNT(*)
    FROM pendaftaran_donor
    WHERE id_pendonor = %s
    AND status = 'menunggu'
    """
    self.cursor.execute(sql, (id_pendonor,))
    return self.cursor.fetchone()[0]


def simpan_pendaftaran(self, id_pendonor, berat_badan):
    sql = """
    INSERT INTO pendaftaran_donor
    (id_pendonor, berat_badan)
    VALUES (%s, %s)
    """
    self.cursor.execute(sql, (id_pendonor, berat_badan))
    self.conn.commit()


def darah_keluar_today():
    db = connect()
    cur = db.cursor()
    cur.execute("""
        SELECT
            t.id_transaksi,
            d.gol_darah,
            t.jumlah,
            t.tanggal_transaksi
        FROM transaksi t
        JOIN darah d ON t.id_darah = d.id_darah
        WHERE t.tipe_transaksi = 'KELUAR'
        AND t.tanggal_transaksi = CURDATE()
    """)
    data = cur.fetchall()
    cur.close()
    db.close()
    return data

