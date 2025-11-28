from build_connection import BuildConnection
from entities import Deadline

class DeadlinesModel:

    @staticmethod
    def create(dead_id, mod_id, week_no, ass_name, due_date):
        db = BuildConnection()
        conn = db.make_connection()
        cur = conn.cursor()

        sql = """
            INSERT INTO deadlines (
                dead_id, mod_id, week_no, ass_name, due_date
            )
            VALUES (%s, %s, %s, %s, %s)
        """

        cur.execute(sql, (dead_id, mod_id, week_no, ass_name, due_date))
        conn.commit()

        cur.close()
        conn.close()

        return dead_id


    @staticmethod
    def get_all():
        db = BuildConnection()
        conn = db.make_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM deadlines")
        rows = cur.fetchall()

        cur.close()
        conn.close()

        deadlines = []
        for row in rows:
            d = Deadline(
                dead_id=row[0],
                mod_id=row[1],
                week_no=row[2],
                ass_name=row[3],
                due_date=row[4]
            )
            deadlines.append(d)

        return deadlines


    @staticmethod
    def get_by_id(dead_id):
        db = BuildConnection()
        conn = db.make_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM deadlines WHERE dead_id = %s", (dead_id,))
        row = cur.fetchone()

        cur.close()
        conn.close()

        if row is None:
            return None

        return Deadline(
            dead_id=row[0],
            mod_id=row[1],
            week_no=row[2],
            ass_name=row[3],
            due_date=row[4]
        )


    @staticmethod
    def get_by_module(mod_id):
        db = BuildConnection()
        conn = db.make_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM deadlines WHERE mod_id = %s", (mod_id,))
        rows = cur.fetchall()

        cur.close()
        conn.close()

        deadlines = []
        for row in rows:
            d = Deadline(
                dead_id=row[0],
                mod_id=row[1],
                week_no=row[2],
                ass_name=row[3],
                due_date=row[4]
            )
            deadlines.append(d)

        return deadlines


    @staticmethod
    def update(dead_id, ass_name, due_date, week_no, mod_id):
        db = BuildConnection()
        conn = db.make_connection()
        cur = conn.cursor()

        sql = """
            UPDATE deadlines
            SET ass_name = %s,
                due_date = %s,
                week_no = %s,
                mod_id = %s
            WHERE dead_id = %s
        """

        cur.execute(sql, (ass_name, due_date, week_no, mod_id, dead_id))
        conn.commit()

        cur.close()
        conn.close()

        return True


    @staticmethod
    def delete(dead_id):
        db = BuildConnection()
        conn = db.make_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM deadlines WHERE dead_id = %s", (dead_id,))
        conn.commit()

        cur.close()
        conn.close()

        return True