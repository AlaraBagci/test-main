class User:
    def __init__(self, user_id, email, role, password_hash=None):
        self.user_id = user_id
        self.email = email
        self.role = role
        self.password_hash = password_hash

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"


class Student:
    def __init__(self, stud_id, stud_name, year, email, course_id):
        self.stud_id = stud_id
        self.stud_name = stud_name
        self.year = year
        self.email = email
        self.course_id = course_id

    def __repr__(self):
        return f"<Student {self.stud_name} ({self.stud_id})>"


class Course:
    def __init__(self, course_id, course_name):
        self.course_id = course_id
        self.course_name = course_name

    def __repr__(self):
        return f"<Course {self.course_id}: {self.course_name}>"


class Module:
    def __init__(self, mod_id, mod_name, course_id, year, welfare_staff_id, module_lead_id):
        self.mod_id = mod_id
        self.mod_name = mod_name
        self.course_id = course_id
        self.year = year
        self.welfare_staff_id = welfare_staff_id
        self.module_lead_id = module_lead_id

    def __repr__(self):
        return f"<Module {self.mod_name} ({self.mod_id})>"


class Attendance:
    def __init__(self, week_no, mod_id, stud_id, att_per):
        self.week_no = week_no
        self.mod_id = mod_id
        self.stud_id = stud_id
        self.att_per = att_per

    def __repr__(self):
        return f"<Attendance week {self.week_no} | student {self.stud_id} | module {self.mod_id}>"


class Survey:
    def __init__(self, sur_id, week_no, stud_id, mod_id, stress_levels, hours_slept, comments):
        self.sur_id = sur_id
        self.week_no = week_no
        self.stud_id = stud_id
        self.mod_id = mod_id
        self.stress_levels = stress_levels
        self.hours_slept = hours_slept
        self.comments = comments

    def __repr__(self):
        return f"<Survey {self.sur_id} | student {self.stud_id} | module {self.mod_id}>"


class Deadline:
    def __init__(self, dead_id, mod_id, week_no, ass_name, due_date):
        self.dead_id = dead_id
        self.mod_id = mod_id
        self.week_no = week_no
        self.ass_name = ass_name
        self.due_date = due_date

    def __repr__(self):
        return f"<Deadline {self.ass_name} | module {self.mod_id} | due {self.due_date}>"