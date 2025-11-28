from build_connection import BuildConnection
from entities import Student

class StudentModel:

    @staticmethod
    def create(stud_id, stud_name, year, email, course_id):
        db = BuildConnection()
        conn = db.make_connection()
        cur = conn.cursor()

        sql = """
            INSERT INTO student (stud_id, stud_name, year, email, course_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        
        cur.execute(sql, (stud_id, stud_name, year, email, course_id))
        conn.commit()

        cur.close()
        conn.close()

        return stud_id


    @staticmethod
    def get_all():
        db = BuildConnection()
        conn = db.make_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM student")
        rows = cur.fetchall()

        cur.close()
        conn.close()

        students = []
        for row in rows:
            student_obj = Student(
                stud_id=row[0],
                stud_name=row[1],
                year=row[2],
                email=row[3],
                course_id=row[4]
            )
            students.append(student_obj)

        return students


    @staticmethod
    def get_by_id(stud_id):
        db = BuildConnection()
        conn = db.make_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM student WHERE stud_id = %s", (stud_id,))
        row = cur.fetchone()

        cur.close()
        conn.close()

        if row is None:
            return None

        # return Student object
        return Student(
            stud_id=row[0],
            stud_name=row[1],
            year=row[2],
            email=row[3],
            course_id=row[4]
        )


    @staticmethod
    def delete(stud_id):
        db = BuildConnection()
        conn = db.make_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM student WHERE stud_id = %s", (stud_id,))
        conn.commit()

        cur.close()
        conn.close()

        return True