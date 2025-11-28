from build_connection import BuildConnection
from entities import Attendance

class AttendanceModel:

    @staticmethod
    def create(week_no, mod_id, stud_id, att_per):
        db = BuildConnection()
        conn = db.make_connection()
        cur = conn.cursor()

        sql = """
            INSERT INTO attendance (week_no, mod_id, stud_id, att_per)
            VALUES (%s, %s, %s, %s)
        """

        cur.execute(sql, (week_no, mod_id, stud_id, att_per))
        conn.commit()

        cur.close()
        conn.close()

        return True


    @staticmethod
    def get_all():
        db = BuildConnection()
        conn = db.make_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM attendance")
        rows = cur.fetchall()

        cur.close()
        conn.close()

        attendance_list = []
        for row in rows:
            a = Attendance(
                week_no=row[0],
                mod_id=row[1],
                stud_id=row[2],
                att_per=row[3]
            )
            attendance_list.append(a)

        return attendance_list


    @staticmethod
    def get_record(week_no, mod_id, stud_id):
        db = BuildConnection()
        conn = db.make_connection()
        cur = conn.cursor()

        sql = """
            SELECT * FROM attendance
            WHERE week_no = %s AND mod_id = %s AND stud_id = %s
        """

        cur.execute(sql, (week_no, mod_id, stud_id))
        row = cur.fetchone()

        cur.close()
        conn.close()

        if row is None:
            return None

        return Attendance(
            week_no=row[0],
            mod_id=row[1],
            stud_id=row[2],
            att_per=row[3]
        )


    @staticmethod
    def update(week_no, mod_id, stud_id, att_per):
        db = BuildConnection()
        conn = db.make_connection()
        cur = conn.cursor()

        sql = """
            UPDATE attendance
            SET att_per = %s
            WHERE week_no = %s AND mod_id = %s AND stud_id = %s
        """

        cur.execute(sql, (att_per, week_no, mod_id, stud_id))
        conn.commit()

        cur.close()
        conn.close()

        return True


    @staticmethod
    def delete(week_no, mod_id, stud_id):
        db = BuildConnection()
        conn = db.make_connection()
        cur = conn.cursor()

        sql = """
            DELETE FROM attendance
            WHERE week_no = %s AND mod_id = %s AND stud_id = %s
        """

        cur.execute(sql, (week_no, mod_id, stud_id))
        conn.commit()

        cur.close()
        conn.close()

        return True