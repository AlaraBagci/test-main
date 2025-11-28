from build_connection import BuildConnection
from entities import Course

class CourseModel:

    @staticmethod
    def create(course_id, course_name):
        db = BuildConnection()
        conn = db.make_connection()
        cur = conn.cursor()

        sql = """
            INSERT INTO course (course_id, course_name)
            VALUES (%s, %s)
        """

        cur.execute(sql, (course_id, course_name))
        conn.commit()

        cur.close()
        conn.close()

        return course_id


    @staticmethod
    def get_all():
        db = BuildConnection()
        conn = db.make_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM course")
        rows = cur.fetchall()

        cur.close()
        conn.close()

        courses = []
        for row in rows:
            c = Course(
                course_id=row[0],
                course_name=row[1]
            )
            courses.append(c)

        return courses


    @staticmethod
    def get_by_id(course_id):
        db = BuildConnection()
        conn = db.make_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM course WHERE course_id = %s", (course_id,))
        row = cur.fetchone()

        cur.close()
        conn.close()

        if row is None:
            return None

        return Course(
            course_id=row[0],
            course_name=row[1]
        )


    @staticmethod
    def update(course_id, course_name):
        db = BuildConnection()
        conn = db.make_connection()
        cur = conn.cursor()

        sql = """
            UPDATE course
            SET course_name = %s
            WHERE course_id = %s
        """

        cur.execute(sql, (course_name, course_id))
        conn.commit()

        cur.close()
        conn.close()

        return True


    @staticmethod
    def delete(course_id):
        db = BuildConnection()
        conn = db.make_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM course WHERE course_id = %s", (course_id,))
        conn.commit()

        cur.close()
        conn.close()

        return True