import string
from functools import reduce

class Student:
    def __init__(self, name, idno):
        self.name = name
        self.idno = idno
        self.courses = []
        self.grades = []

    def enroll(self, course):
        if course not in self.courses:
            self.courses.append(course)
            self.grades.append(0.0)

    def drop(self, course):
        if course in self.courses:
            index = self.courses.index(course)
            del self.courses[index]
            del self.grades[index]

    def setGrade(self, course, grade):
        if course in self.courses and isValidUnit(grade):
            self.grades[self.courses.index(course)] = grade

    def gpa(self):
        if len(self.courses) == 0:
            return 0.0
        unitsum = reduce(lambda x,y: x + y, list(map(lambda x : x.unit, self.courses)))
        return reduce(lambda x,y: x + y, list(map(lambda i: self.courses[i].unit*self.grades[i]/unitsum, range(len(self.courses)))))

    def displayGPA(self):
        print('GPA: ' + ('%.2f' % self.gpa()))

    def display(self, withGPA=False):
        print(str(self.idno) + ' ' + self.name, end='')
        if withGPA:
            print(' ', end='')
            self.displayGPA()
        else:
            print('')

class StudentList:
    def __init__(self):
        self.students = []

    def getStudentWithID(self, idno):
        if isValidID(idno):
            return next((x for x in self.students if x.idno == idno), None)
        else:
            return None

    def addStudent(self, name, idno):
        if isValidID(idno):
            if self.getStudentWithID(idno) == None:
                self.students.append(Student(name, idno))
                self.sortList()
            else:
                print('Student with ID#' + str(idno) + ' already exists!')
        else:
            print('Invalid ID number!')

    def deleteStudent(self, idno):
        student = self.getStudentWithID(idno)
        if student != None:
            self.students.remove(student)
        else:
            print('Student not found!')

    def sortList(self):
        self.students.sort(key=lambda x : x.idno)

    def displayAll(self):
        [1 for x in self.students if x.display() and False]

    def displayTopN(self, n):
        byGPA = sorted(self.students, key=lambda x : x.gpa()*-1)
        if n <= len(byGPA):
            [1 for i in range(n) if byGPA[i].display(True) and False]
        else:
            [1 for i in range(len(byGPA)) if byGPA[i].display(True) and False]

class Course:
    def __init__(self, code, unit):
        self.code = code
        self.unit = unit
        self.students = []
        self.grades = []

    def addStudent(self, student):
        if student not in self.students:
            self.students.append(student)
            self.grades.append(0.0)

    def deleteStudent(self, student):
        if student in self.students:
            index = self.students.index(student)
            del self.students[index]
            del self.grades[index]

    def delete(self):
        for student in self.students:
            student.drop(self)
        self.students.clear()
        self.grades.clear()

    def setGrade(self, student, grade):
        if student in self.students and isValidUnit(grade):
             self.grades[self.students.index(student)] = grade

    def display(self):
        print(self.code + ' ' + str(self.unit))

class CourseList:
    def __init__(self):
        self.courses = []

    def getCourseWithCode(self, code):
        if isValidCode(code):
            return next((x for x in self.courses if x.code == code), None)
        else:
            return None
        
    def addCourse(self, code, unit):
        if isValidCode(code) and isValidUnit(unit):
            if self.getCourseWithCode(code) == None:
                self.courses.append(Course(code, unit))
            else:
                print('Course with code ' + code + ' already exists!')
        else:
            print('Code or unit invalid!')

    def deleteCourse(self, code):
        course = self.getCourseWithCode(code)
        if course != None:
            course.delete()
            self.courses.remove(course)
        else:
            print('Course not found!')

    def displayAll(self):
        [1 for x in self.courses if x.display() and False]

def safeTC(x, type):
    try:
        return type(x)
    except(NameError, ValueError):
        print('Invalid input!')
        return type(0)

inputUpStr = lambda msg : input(msg).strip().upper()

inputInt = lambda msg : safeTC(input(msg), int)

inputFloat = lambda msg : safeTC(input(msg), float)

isValidID = lambda x : 10000000 <= x <= 99999999

def isValidCode(code):
    if len(code) != 7:
        return False
    allowed = '-' + string.ascii_uppercase + string.digits
    for letter in code:
        if letter not in allowed:
            return False
    return True

isValidUnit = lambda x : 0 <= x <= 4

def menuBuilder(header, items):
    print('\n' + header.replace('', ' '))
    for i in range(len(items)):
        print(str(i+1) + ': ' + items[i])
    return input('> ')

def editStudentMenu(student, students):
    print(str(student.idno) + ' ' + student.name)
    c = menuBuilder('EDIT STUDENT', ('ID NUMBER', 'NAME', 'EXIT'))
    if c == '1':
        idno = inputInt('Enter ID number: ')
        if isValidID(idno):
            if students.getStudentWithID(idno) == None:
                student.idno = idno
            else:
                print('Student with ID#' + str(idno) + ' already exists!')
        else:
            print('Invalid ID number!')
    elif c == '2':
        student.name = inputUpStr('Enter name: ')
    elif c == '3':
        return False
    else:
        print('Invalid input!')
    return True

def editCourseMenu(course, courses):
    course.display()
    c = menuBuilder('EDIT COURSE', ('COURSE CODE', 'UNITS', 'EXIT'))
    if c == '1':
        code = inputUpStr('Enter course code: ')
        if isValidCode(code) and courses.getCourseWithCode(code) == None:
            course.code = code
        else:
            print('Invalid code!')
    elif c == '2':
        unit = inputFloat('Enter units: ')
        if isValidUnit(unit):
            course.unit = unit
        else:
            print('Invalid units!')
    elif c == '3':
        return False
    else:
        print('Invalid input!')
    return True

def studentMenu(students):
    c = menuBuilder('STUDENT MENU', ('ADD STUDENT','EDIT STUDENT', \
        'DELETE STUDENT', 'VIEW ALL STUDENTS', 'VIEW TOP 5 STUDENTS', 'EXIT'))
    if c == '1':
        students.addStudent(inputUpStr('Enter name: '), \
            inputInt('Enter student ID: '))
    elif c == '2':
        idno = inputInt('Enter student ID: ')
        if isValidID(idno):
            student = students.getStudentWithID(idno)
            if student != None:
                while editStudentMenu(student, students):
                    pass
            else:
                print('Student not found!')
        else:
            print('Invalid ID!')
    elif c == '3':
        students.deleteStudent(inputInt('Enter student ID: '))
    elif c == '4':
        students.displayAll()
    elif c == '5':
        students.displayTopN(5)
    elif c == '6':
        return False
    else:
        print('Invalid input!')
    return True

def courseMenu(courses):
    c = menuBuilder('COURSE MENU', ('ADD COURSE', 'EDIT COURSE', \
        'DELETE COURSE', 'VIEW ALL COURSES', 'EXIT'))
    if c == '1':
        courses.addCourse(inputUpStr('Enter course code: '), \
            inputFloat('Enter unit: '))
    elif c == '2':
        code = inputUpStr('Enter course code: ')
        if isValidCode(code):
            course = courses.getCourseWithCode(code)
            if course != None:
                while editCourseMenu(course, courses):
                    pass
            else:
                print('Course not found!')
        else:
            print('Invalid course code!')
    elif c == '3':
        courses.deleteCourse(inputUpStr('Enter course code: '))
    elif c == '4':
        courses.displayAll()
    elif c == '5':
        return False
    else:
        print('Invalid input!')
    return True

def enrollMenu(students, courses):
    c = menuBuilder('ENROLLMENT MENU', ('ENROLL STUDENT', 'DROP STUDENT', \
        'SET GRADE', 'VIEW REPORT CARD', 'EXIT'))
    if c == '1':
        student = students.getStudentWithID(inputInt('Enter student ID: '))
        course = courses.getCourseWithCode(inputUpStr('Enter course code: '))
        if student != None and course != None:
            student.enroll(course)
            course.addStudent(student)
        else:
            print('Student or course does not exist!')
    elif c == '2':
        student = students.getStudentWithID(inputInt('Enter student ID: '))
        course = courses.getCourseWithCode(inputUpStr('Enter course code: '))
        if student != None and course != None:
            if course in student.courses:
                student.drop(course)
                course.deleteStudent(student)
            else:
                print('Student is not enrolled in course!')
        else:
            print('Student or course does not exist!')
    elif c == '3':
        student = students.getStudentWithID(inputInt('Enter student ID: '))
        course = courses.getCourseWithCode(inputUpStr('Enter course code: '))
        if student != None and course != None:
            if course in student.courses:
                grade = inputFloat('Enter new grade: ')
                if isValidUnit(grade):
                    student.setGrade(course, grade)
                    course.setGrade(student, grade)
                else:
                    print('Invalid grade!')
            else:
                print('Student is not enrolled in course!')
        else:
            print('Student or course does not exist!')
    elif c == '4':
        student = students.getStudentWithID(inputInt('Enter student ID: '))
        if student != None:
            student.display()
            for i in range(len(student.courses)):
                print(student.courses[i].code + ' '*3 + str(student.grades[i]))
            student.displayGPA()
        else:
            print('Student not found!')
    elif c == '5':
        return False
    else:
        print('Invalid input!')
    return True

def mainMenu(students, courses):
    c = menuBuilder('MAIN MENU', ('STUDENTS', 'COURSES', \
        'ENROLLMENT', 'EXIT'))
    if c == '1':
        while studentMenu(students):
            pass
    elif c == '2':
        while courseMenu(courses):
            pass
    elif c == '3':
        while enrollMenu(students, courses):
            pass
    elif c == '4':
        return False
    else:
        print('Invalid input!')
    return True

def start():
    students = StudentList()
    courses = CourseList()

    print('='*10 + ' ENROLLMENT SYSTEM ' + '='*10)
    while mainMenu(students, courses):
        pass

start()
