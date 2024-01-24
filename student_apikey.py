from flask import request,Flask,jsonify
from functools import wraps
app = Flask(__name__) 

API_KEY = 'your_api_key'

def require_api_key(func):
    @wraps(func)
    def decorated(*args,**kwargs):
        if request.headers.get('Api-key')==API_KEY:
            return func(*args,**kwargs)
        else:
            return jsonify({"error":"Unauthorized"}),401
    return decorated

books=[
    {"id": 1, "student_id": "6530301000"},
    {"id": 2, "student_id": "6530300414"},
    {"id": 3, "student_id": "6530300879"}
]
@app.route("/")
def greet():
    return "<p>Welcome to Student Management API</p>"

@app.route("/students", methods=["GET"])
def get_all_students():
    return jsonify({"students": students})

@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if student:
        return jsonify(student)
    else:
        return jsonify({"error": "Student not found"}), 404

@app.route("/students", methods=["POST"])
def create_student():
    data = request.get_json()
    new_student = {
        "id": len(students) + 1,
        "student_id": data.get("student_id", None)
    }

    # Check for duplicate student_id
    if any(s["student_id"] == new_student["student_id"] for s in students):
        return jsonify({"error": "Cannot create new student. Duplicate student_id"}), 500

    students.append(new_student)
    return jsonify(new_student), 201

@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if student:
        data = request.get_json()
        student.update(data)
        return jsonify(student)
    else:
        return jsonify({"error": "Student not found"}), 404

@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    global students
    student = next((s for s in students if s["id"] == student_id), None)
    if student:
        students = [s for s in students if s["id"] != student_id]
        return jsonify({"message": "Student deleted successfully"}), 200
    else:
        return jsonify({"error": "Student not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)