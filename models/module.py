from build_connection import BuildConnection
from entities import Module

class ModuleModel:

    @staticmethod
    def create(mod_id, mod_name, course_id, year, welfare_staff_id, module_lead_id):
        db = BuildConnection()
        conn = db.make_connection()
        cur = conn.cursor()

        sql = """
            INSERT INTO module 
            (mod_id, mod_name, course_id, year, welfare_staff_id, module_lead_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cur.execute(sql, (mod_id, mod_name, course_id, year, welfare_staff_id, module_lead_id))
        conn.commit()

        cur.close()
        conn.close()

        return mod_id


    @staticmethod
    def get_all():
        db = BuildConnection()
        conn = db.make_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM module")
        rows = cur.fetchall()

        cur.close()
        conn.close()

        modules = []
        for row in rows:
            m = Module(
                mod_id=row[0],
                mod_name=row[1],
                course_id=row[2],
                year=row[3],
                welfare_staff_id=row[4],
                module_lead_id=row[5]
            )
            modules.append(m)

        return modules


    @staticmethod
    def get_by_id(mod_id):
        db = BuildConnection()
        conn = db.make_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM module WHERE mod_id = %s", (mod_id,))
        row = cur.fetchone()

        cur.close()
        conn.close()

        if row is None:
            return None

        return Module(
            mod_id=row[0],
            mod_name=row[1],
            course_id=row[2],
            year=row[3],
            welfare_staff_id=row[4],
            module_lead_id=row[5]
        )


    @staticmethod
    def update(mod_id, mod_name, course_id, year, welfare_staff_id, module_lead_id):
        db = BuildConnection()
        conn = db.make_connection()
        cur = conn.cursor()

        sql = """
            UPDATE module
            SET mod_name = %s,
                course_id = %s,
                year = %s,
                welfare_staff_id = %s,
                module_lead_id = %s
            WHERE mod_id = %s
        """

        cur.execute(sql, (mod_name, course_id, year, welfare_staff_id, module_lead_id, mod_id))
        conn.commit()

        cur.close()
        conn.close()

        return True


    @staticmethod
    def delete(mod_id):
        db = BuildConnection()
        conn = db.make_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM module WHERE mod_id = %s", (mod_id,))
        conn.commit()

        cur.close()
        conn.close()

        return True