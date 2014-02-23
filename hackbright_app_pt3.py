import sqlite3
# TODO (optional) try fancy stuff here: http://docs.python.org/2/library/sqlite3.html

DB = None
CONN = None

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()
    print "enter your query separated by commas"
# TODO (optional) add better helptext 

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
# NOTE Returns tuple, there is a way to return a dictionary (see notes)
# TODO Would this still work with the give_grade function? 
    return row
    # Student: %s %s
    # Github account: %s"""%(row[0], row[1], row[2])
    # return {'firstname':row[0],'lastname':row[1],'github':row[2]}

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
    if row:
        print """\
        ID: %s
        title: %s
        description: %s
        max_grade: %s"""%(row[0], row[1], row[2], row[3])

    return row

def add_project(title, description, max_grade):
    query = """INSERT into Projects values (NULL, ?,?,?)"""
# NOTE This is not good form, but just wanted to try it. Generally want to explicity state what columns you are adding to
# how would you handle this ID autoincrement column, where it's abuild in function? (chicken and egg problem)
#   how do shortcut in insert fxn without needing column names? (USE NULL not None, but bad practice to not explicitly state column in case later add)
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    lastid = DB.lastrowid
    print """Successfully added new project
ID: %s
title: %s
description: %s
max_grade: %s"""%(lastid, title, description, max_grade)


# TODO How would you wite query so just returns everything rather than one row at a time? 
def get_student_grade(project_title, student_github):
    query = """SELECT grade FROM Grades WHERE project_title = ? AND student_github = ?"""
    DB.execute(query, (project_title, student_github))
    row = DB.fetchone()
    if row:
        print """\
    Student github: %s
    Project: %s
    Grade: %s"""%(student_github, project_title, row[0])

    return row

def give_grade(github, project, grade):
    query = """INSERT into Grades (student_github, project_title, grade) values (?,?,?)"""
    DB.execute(query, (github, project, grade))
    CONN.commit()
    print """Successfully added new grade
Github: %s
Project: %s
Grade: %s"""%(github, project, grade)    


def show_grades(student_github):
    query = """SELECT project_title, grade FROM Grades WHERE student_github = ?"""
    DB.execute(query, (student_github,))
    row = 1
# TODO try fetchall() 
    while row:
        row = DB.fetchone()
    # TODO print row (why does this return u'Markov' in front of Markov?)     
        print """
        Project: %s
        Grade: %s"""%(row[0], row[1])
    # TODO why does this return one final None at the end? 

    # return row
    # TODO (optional) append answer to list of tuples to print out


def main():

    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split(None,1)
        # print "Tokens are: ",tokens
        command = tokens[0]
        # print "Command is: ", command
        args = tokens[1].split(',')
# TODO (optional) could add a strip here for extra spaces?
        # print "Args are : ", args
# TODO split creates a list, can you pass that as arg in function?

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
        elif command == 'student_grade':
            get_student_grade(*args)

        elif command == 'give_grade':
            github = args[0]
            project = args[1]

            title = get_project_title(project)
            student = get_student_by_github(github)
            grade = get_student_grade(project, github)

# TODO: possible to make it so that the below doesn't print the functions above in addition to the error msgs below?
#   Try: Change functions to return instead of print entirely, then change to print function in elif statements
# TODO: Need to check that grade input is below max grade
            if not title:
                print "error, that project doesn't exist, please create with the add_project command"
            elif not student:
                print "error, that student doesn't exist, please add student with add_student command"
            elif grade:
                print "error, this student already has a grade for this project"
            else:
                give_grade(*args)
        elif command == 'show_grades':
            show_grades(*args)
# TODO  else: How to get a catch all for all errors? Try and Except?
        #     print "invalid command"

# # TODO (optional) could use this to catch errors and give helptext)
#     # numargs = {
#     #     'give_grade': { 'num': 4, 'helptext': "Enter First_name, last_name, ...."}

#     # }


#TODO Can you set max_grade automatically update the maximum grade from the grades table?
#TODO How would you set this up so that if not title or not student, it automatically takes you through appropriate steps to create them?
    # can do a series of raw_inputs and if statements

    CONN.close()

if __name__ == "__main__":
    main()
