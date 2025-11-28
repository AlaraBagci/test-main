from build_connection import BuildConnection
from entities import Survey

class SurveyModel:

    @staticmethod
    def create(sur_id, week_no, stud_id, mod_id, stress_levels, hours_slept, comments):
        db = BuildConnection()
        conn = db.make_connection()
        cur = conn.cursor()

        sql = """
            INSERT INTO surveys (
                sur_id, week_no, stud_id, mod_id,
                stress_levels, hours_slept, comments
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cur.execute(sql, (sur_id, week_no, stud_id, mod_id, stress_levels, hours_slept, comments))
        conn.commit()

        cur.close()
        conn.close()

        return sur_id


    @staticmethod
    def get_all():
        db = BuildConnection()
        conn = db.make_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM surveys")
        rows = cur.fetchall()

        cur.close()
        conn.close()

        surveys = []
        for row in rows:
            s = Survey(
                sur_id=row[0],
                week_no=row[1],
                stud_id=row[2],
                mod_id=row[3],
                stress_levels=row[4],
                hours_slept=row[5],
                comments=row[6]
            )
            surveys.append(s)

        return surveys


    @staticmethod
    def get_by_id(sur_id):
        db = BuildConnection()
        conn = db.make_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM surveys WHERE sur_id = %s", (sur_id,))
        row = cur.fetchone()

        cur.close()
        conn.close()

        if row is None:
            return None

        return Survey(
            sur_id=row[0],
            week_no=row[1],
            stud_id=row[2],
            mod_id=row[3],
            stress_levels=row[4],
            hours_slept=row[5],
            comments=row[6]
        )


    @staticmethod
    def get_student_week(stud_id, week_no, mod_id):
        """
        Returns a Survey object for the unique survey for this student+week+module.
        """
        db = BuildConnection()
        conn = db.make_connection()
        cur = conn.cursor()

        sql = """
            SELECT * FROM surveys
            WHERE stud_id = %s AND week_no = %s AND mod_id = %s
        """

        cur.execute(sql, (stud_id, week_no, mod_id))
        row = cur.fetchone()

        cur.close()
        conn.close()

        if row is None:
            return None

        return Survey(
            sur_id=row[0],
            week_no=row[1],
            stud_id=row[2],
            mod_id=row[3],
            stress_levels=row[4],
            hours_slept=row[5],
            comments=row[6]
        )


    @staticmethod
    def update(sur_id, stress_levels, hours_slept, comments):
        db = BuildConnection()
        conn = db.make_connection()
        cur = conn.cursor()

        sql = """
            UPDATE surveys
            SET stress_levels = %s,
                hours_slept = %s,
                comments = %s
            WHERE sur_id = %s
        """

        cur.execute(sql, (stress_levels, hours_slept, comments, sur_id))
        conn.commit()

        cur.close()
        conn.close()

        return True


    @staticmethod
    def delete(sur_id):
        db = BuildConnection()
        conn = db.make_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM surveys WHERE sur_id = %s", (sur_id,))
        conn.commit()

        cur.close()
        conn.close()

        return True