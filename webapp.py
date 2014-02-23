import hackbright_app_pt3
from flask import Flask, render_template, request

app = Flask(__name__)

# Code goes here

@app.route("/")
def get_github():
    return render_template("get_github.html")

def get_student():
    hackbright_app_pt3.connect_to_db()
    student_github =  request.args.get("student") #"chriszf"
    row = hackbright_app_pt3.get_student_by_github(student_github)
    html = render_template("student_info.html", first_name=row[0],
                                                last_name=row[1],
                                                github=row[2])
    return html

# def helloworld():
#     return "Hello world"


if __name__ == "__main__":
    app.run(debug=True)