import mysql.connector
def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="uas_pbo_pmi"
    )
    
def login_user(nik, password):
    db = connect()
    cursor = db.cursor()

    cursor.execute("""
        SELECT p.id_pendonor, u.password, u.id_role
        FROM pendonor p
        JOIN pengguna u ON p.id_pengguna = u.id_pengguna
        WHERE p.nik = %s
    """, (nik,))

    result = cursor.fetchone()
    if not result:
        return False, "NIK tidak terdaftar"

    id_pendonor, pw_db, role_id = result

    if password != pw_db:
        return False, "Password salah"

    return True, {"id_pendonor": id_pendonor, "role_id": role_id}



def register_pendonor(nama, nik, tanggal_lahir, gol_darah, no_hp, password):
    db = connect()
    cursor = db.cursor()

    # cek NIK
    cursor.execute(
        "SELECT id_pendonor FROM pendonor WHERE nik = %s",
        (nik,)
    )
    if cursor.fetchone():
        return "NIK sudah terdaftar"

    try:
        cursor.execute(
            "SELECT id_role FROM role WHERE nama_role = 'pendonor'"
        )
        role_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO pengguna (password, id_role)
            VALUES (%s, %s)
        """, (password, role_id))

        id_pengguna = cursor.lastrowid

        # insert pendonor
        cursor.execute("""
            INSERT INTO pendonor (
                id_pengguna,
                nama_pendonor,
                nik,
                tanggal_lahir,
                gol_darah,
                no_hp
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            id_pengguna,
            nama,
            nik,
            tanggal_lahir,
            gol_darah,
            no_hp
        ))

        db.commit()
        return "Registrasi berhasil"

    except Exception as e:
        db.rollback()
        return f"Gagal registrasi: {e}"
