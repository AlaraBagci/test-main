from flask import Flask, request, jsonify

# Import models
from models.students import StudentModel
from models.course import CourseModel
from models.module import ModuleModel
from models.attendance import AttendanceModel
from models.survey import SurveyModel
from models.deadlines import DeadlinesModel

# Import entities (for converting to dict)
from entities import Student, Course, Module, Attendance, Survey, Deadline

app = Flask(__name__)

def to_dict(obj):
    return obj.__dict__


# STUDENT ENDPOINTS
@app.get("/students")
def get_students():
    students = StudentModel.get_all()
    return jsonify([to_dict(s) for s in students])


@app.get("/students/<stud_id>")
def get_student(stud_id):
    s = StudentModel.get_by_id(stud_id)
    if not s:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(to_dict(s))


@app.post("/students")
def create_student():
    data = request.json
    StudentModel.create(
        data["stud_id"],
        data["stud_name"],
        data["year"],
        data["email"],
        data["course_id"]
    )
    return jsonify({"message": "Student created"}), 201


@app.delete("/students/<stud_id>")
def delete_student(stud_id):
    StudentModel.delete(stud_id)
    return jsonify({"message": "Student deleted"})

# COURSE ENDPOINTS
@app.get("/courses")
def get_courses():
    courses = CourseModel.get_all()
    return jsonify([to_dict(c) for c in courses])


@app.get("/courses/<course_id>")
def get_course(course_id):
    c = CourseModel.get_by_id(course_id)
    if not c:
        return jsonify({"error": "Course not found"}), 404
    return jsonify(to_dict(c))


@app.post("/courses")
def create_course():
    data = request.json
    CourseModel.create(data["course_id"], data["course_name"])
    return jsonify({"message": "Course created"}), 201


@app.put("/courses/<course_id>")
def update_course(course_id):
    data = request.json
    CourseModel.update(course_id, data["course_name"])
    return jsonify({"message": "Course updated"})


# MODULE ENDPOINTS
@app.get("/modules")
def get_modules():
    modules = ModuleModel.get_all()
    return jsonify([to_dict(m) for m in modules])


@app.get("/modules/<mod_id>")
def get_module(mod_id):
    m = ModuleModel.get_by_id(mod_id)
    if not m:
        return jsonify({"error": "Module not found"}), 404
    return jsonify(to_dict(m))


@app.post("/modules")
def create_module():
    data = request.json
    ModuleModel.create(
        data["mod_id"],
        data["mod_name"],
        data["course_id"],
        data["year"],
        data["welfare_staff_id"],
        data["module_lead_id"]
    )
    return jsonify({"message": "Module created"}), 201


# ATTENDANCE ENDPOINTS
@app.get("/attendance")
def get_attendance():
    att = AttendanceModel.get_all()
    return jsonify([to_dict(a) for a in att])


@app.get("/attendance/<week_no>/<mod_id>/<stud_id>")
def get_att_record(week_no, mod_id, stud_id):
    a = AttendanceModel.get_record(week_no, mod_id, stud_id)
    if not a:
        return jsonify({"error": "Record not found"}), 404
    return jsonify(to_dict(a))


@app.post("/attendance")
def create_attendance():
    data = request.json
    AttendanceModel.create(
        data["week_no"],
        data["mod_id"],
        data["stud_id"],
        data["att_per"]
    )
    return jsonify({"message": "Attendance recorded"}), 201


# SURVEY ENDPOINTS
@app.get("/surveys")
def get_surveys():
    surveys = SurveyModel.get_all()
    return jsonify([to_dict(s) for s in surveys])


@app.get("/surveys/<sur_id>")
def get_survey(sur_id):
    s = SurveyModel.get_by_id(sur_id)
    if not s:
        return jsonify({"error": "Survey not found"}), 404
    return jsonify(to_dict(s))


@app.post("/surveys")
def create_survey():
    data = request.json
    SurveyModel.create(
        data["sur_id"],
        data["week_no"],
        data["stud_id"],
        data["mod_id"],
        data["stress_levels"],
        data["hours_slept"],
        data["comments"]
    )
    return jsonify({"message": "Survey submitted"}), 201


# DEADLINES ENDPOINTS
@app.get("/deadlines")
def get_deadlines():
    deadlines = DeadlinesModel.get_all()
    return jsonify([to_dict(d) for d in deadlines])


@app.get("/deadlines/<dead_id>")
def get_deadline(dead_id):
    d = DeadlinesModel.get_by_id(dead_id)
    if not d:
        return jsonify({"error": "Deadline not found"}), 404
    return jsonify(to_dict(d))


@app.post("/deadlines")
def create_deadline():
    data = request.json
    DeadlinesModel.create(
        data["dead_id"],
        data["mod_id"],
        data["week_no"],
        data["ass_name"],
        data["due_date"]
    )
    return jsonify({"message": "Deadline added"}), 201


if __name__ == "__main__":
    app.run(debug=True)