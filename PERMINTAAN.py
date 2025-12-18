import mysql.connector

class Permintaan:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="uas_pbo_pmi"
        )
        self.cursor = self.conn.cursor()
        
        
        
    def get_id_rs_by_pengguna(self, id_pengguna):
        sql = "SELECT id_rs FROM rumah_sakit WHERE id_pengguna = %s"
        self.cursor.execute(sql, (id_pengguna,))
        result = self.cursor.fetchone()
        return result[0] if result else None


    # =====================================
    # SIMPAN HEADER PERMINTAAN
    # =====================================
    def simpan_permintaan_rs(self, id_rs, no_permintaan):
        sql = """
        INSERT INTO permintaan_rs
        (id_rs, no_permintaan, tanggal_permintaan, status)
        VALUES (%s, %s, CURDATE(), 'menunggu')
        """
        self.cursor.execute(sql, (id_rs, no_permintaan))
        self.conn.commit()
        return self.cursor.lastrowid

    # =====================================
    # SIMPAN DETAIL PERMINTAAN
    # =====================================
    def simpan_detail_permintaan(self, id_permintaan, id_darah, jumlah, keperluan):
        sql = """
        INSERT INTO detail_permintaan
        (id_permintaan, id_darah, jumlah, keperluan)
        VALUES (%s, %s, %s, %s)
        """
        self.cursor.execute(sql, (id_permintaan, id_darah, jumlah, keperluan))
        self.conn.commit()

    # =====================================
    # AMBIL DATA UNTUK TABLE (JOIN)
    # =====================================
    def get_semua_permintaan(self):
        sql = """
        SELECT 
            p.no_permintaan,
            d.id_darah,
            d.jumlah,
            d.keperluan,
            p.status
        FROM permintaan_rs p
        JOIN detail_permintaan d 
            ON p.id_permintaan = d.id_permintaan
        ORDER BY p.tanggal_permintaan DESC
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    # =====================================
    # HAPUS PERMINTAAN (CASCADE MANUAL)
    # =====================================
    def hapus_permintaan(self, id_permintaan):
        self.cursor.execute(
            "DELETE FROM detail_permintaan WHERE id_permintaan=%s",
            (id_permintaan,)
        )
        self.cursor.execute(
            "DELETE FROM permintaan_rs WHERE id_permintaan=%s",
            (id_permintaan,)
        )
        self.conn.commit()
        
    def get_permintaan_by_rs(self, id_rs):
        query = """
            SELECT 
                p.no_permintaan,
                darah.gol_darah,
                dp.jumlah,
                dp.keperluan,
                p.status
            FROM permintaan_rs p
            JOIN detail_permintaan dp 
                ON p.id_permintaan = dp.id_permintaan
            JOIN darah 
                ON dp.id_darah = darah.id_darah
            WHERE p.id_rs = %s
            ORDER BY p.tanggal_permintaan DESC
        """
        self.cursor.execute(query, (id_rs,))
        return self.cursor.fetchall()


# =====================================
# AMBIL DATA PERMINTAAN MENUNGGU

    def get_permintaan_menunggu(self):
        sql = """
        SELECT
            p.id_permintaan,
            r.nama_rs,
            p.no_permintaan,
            p.tanggal_permintaan,
            p.status
        FROM permintaan_rs p
        JOIN rumah_sakit r ON p.id_rs = r.id_rs
        WHERE p.status = 'menunggu'
        ORDER BY p.tanggal_permintaan DESC
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()


    def get_detail_permintaan(self, id_permintaan):
        sql = """
        SELECT
            d.id_darah,
            darah.gol_darah,
            d.jumlah,
            d.keperluan
        FROM detail_permintaan d
        JOIN darah ON d.id_darah = darah.id_darah
        WHERE d.id_permintaan = %s
        """
        self.cursor.execute(sql, (id_permintaan,))
        return self.cursor.fetchall()
    
    def update_status_permintaan(self, id_permintaan, status):
        sql = """
        UPDATE permintaan_rs
        SET status = %s
        WHERE id_permintaan = %s
        """
        self.cursor.execute(sql, (status, id_permintaan))
        self.conn.commit()

