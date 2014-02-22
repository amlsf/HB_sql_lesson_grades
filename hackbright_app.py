import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
# NOTE Returns tuple, there is a way to return a dictionary
    print """\
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?,?,?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)

def get_project_title(title):
    query = """SELECT id, title, description, max_grade FROM Projects WHERE Title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    # print row
# why is there this \ here? special character that says don't print the new line \n
    print """\
ID: %s
title: %s
description: %s
max_grade: %s"""%(row[0], row[1], row[2], row[3])

def add_project(title, description, max_grade):
    query = """INSERT into Projects values (NULL, ?,?,?)"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    lastid = DB.lastrowid
    print """Successfully added new project
ID: %s
title: %s
description: %s
max_grade: %s"""%(lastid, title, description, max_grade)
# how would you handle this ID autoincrement column, where it's abuild in function? (chicken and egg problem)
#   how do shortcut in insert fxn without needing column names? (USE NULL not None, but bad practice to not explicitly state column in case later add)


# TODO How would you wite query so just returns everything rather than one row at a time? 
# TODO NEED TO TEST THESE NEXT TWO FUNCTIONS
# TODO SHOW ALL THE GRADES FOR STUDENTS
def get_student_grade(project_title, student_github):
    query = """SELECT grade FROM Projects p JOIN Grades g ON (p.title = g.project_title) 
    JOIN Students s ON (s.github = g.student_github) 
    WHERE project_title = ? AND first_name = ? AND last_name = ? """
    DB.execute(query, (project_title, student_github))
    row = DB.fetchone()
    print """\
Student name: %s
project: %s
grade: %s"""%(student_github, project_title, row[0])


def give_grade(github, project, grade):
    query = """INSERT into Grades (github, project_title, grade) values (?,?,?)"""
    DB.execute(query, (github, project, grade))
    CONN.commit()
    print """Successfully added new grade
Github: %s
Project: %s
Grade: %s"""%(github, project, grade)    


def main():

    # numargs = {
    #     'give_grade': { 'num': 4, 'helptext': "Enter First_name, last_name, ...."}

    # }

    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split(None,1)
        # print "Tokens are: ",tokens
        command = tokens[0]
        # print "Command is: ", command
        args = tokens[1].split(',')
        # print "Args are : ", args

        # if numargs[command][num] != len(args):
        #     print "Error, missing argments"
        #     print numargs[commaand]['helptext']
        if command == "student":
            get_student_by_github(*args) 
        elif command == "add_student":
            make_new_student(*args)
        elif command == "project_title":
            get_project_title(*args)
        elif command == 'add_project':
            add_project(*args)

# TODO need to test these next two functions
        elif command == 'student_grade':
            get_student_grade(*args)
        elif command == 'give_grade':
            github = args[0]
            project = args[1]

            title = get_project_title(project)
            student = get_student_by_github(github)
            existing_grade = get_student_grade(project, github)
            if not title:
                print "error, that project doesn't exist, please create with the add_project command"
            elif not student:
                print "error, that student doesn't exist, please add student with add_student command"
            if existing_grade:
                print "error, this student already has a great for this project"
            else:
                give_grade(*args)  

#TODO Shouldn't max_grade automatically update the maximum grade from the grades table?
#TODO How would you set this up so that if not title or not student, it automatically takes you through appropriate steps to create them?

    CONN.close()

if __name__ == "__main__":
    main()
