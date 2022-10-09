students = [("Allen Anderson", "Computer Science"),
            ("Edgar Einstein", "Engineering"),
            ("Farrah Finn", "Fine Arts")]
     
def add_new_student(students, name, major):
    students.append(name, major)

def update_student(students, index, name, major):
    students[index] = ((name, major))

def find_students_by_name(students, name):
    return [student for student in students if name in student[0]]

def get_all_majors(students):
    return [student[1] for student in students]
    
#add_new_student(students,'x','y')
#print(students)
print(find_students_by_name(students, 'in'))
students[0][0] = ('new name')
print(students)