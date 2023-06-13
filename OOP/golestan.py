from collections import OrderedDict

class Student:
  def __init__(self, name, identical_num, entering_year, field):
    self.name = name
    self.identical_num = identical_num
    self.field = field
    self.entering_year = entering_year
    self.classes = OrderedDict() # {class_id:mark}

class Professor:
  def __init__(self, name, identical_num, field):
    self.name = name
    self.identical_num = identical_num
    self.field = field  
    self.classes = [] # [class_id}

class Class:
  def __init__(self, name, class_id, field):
    self.name = name
    self.class_id = class_id
    self.field = field
    self.professor = None
    self.students = OrderedDict() # {student_id:mark}
  
class Golestan:
  def __init__(self):
    self.students = OrderedDict()
    self.profs = dict()
    self.classes = dict()

  def person_validation(self, identical_num):
    if identical_num in self.students or identical_num in self.profs :
       print('this identical number previously registered')
       return False
    print('welcome to golestan')
    return True

  def register_student(self, name, identical_num, entering_year, field):
    if self.person_validation(identical_num):
      self.students[identical_num] = Student(name, identical_num, entering_year, field)

  def register_professor(self, name, identical_num, field):
    if self.person_validation(identical_num):
      self.profs[identical_num] = Professor(name, identical_num, field)

  def make_class(self, name, class_id, field):
      if class_id in self.classes :
        print('this class id previously used')
      else:
        self.classes[class_id] = Class(name, class_id, field)
        print('class added successfully')

  def add_student(self, identical_num, class_id):
    if identical_num not in self.students: print('invalid student')
    elif class_id not in self.classes: print('invalid class')
    else:
      stu, cls = self.students[identical_num], self.classes[class_id]
      if  stu.field != cls.field: print('student field is not match')
      elif class_id in stu.classes: print('student is already registered')
      else:
        stu.classes[class_id] = None
        cls.students[identical_num] = None
        print('student added successfully to the class')

  def add_professor(self, identical_num, class_id):
    if identical_num not in self.profs: print('invalid professor')
    elif class_id not in self.classes: print('invalid class')
    else:
      prof, cls = self.profs[identical_num], self.classes[class_id]
      if  prof.field != cls.field: print('professor field is not match')
      elif cls.professor: print('this class has a professor')
      else:
        cls.professor = identical_num
        prof.classes.append(class_id)
        print('professor added successfully to the class')
  
  def student_status(self, identical_num):
    if identical_num not in self.students: print('invalid student')
    else:
      stu = self.students[identical_num]
      print(stu.name, stu.entering_year, stu.field, *[self.classes[cls_id].name for cls_id in stu.classes])

  def professor_status(self, identical_num):
    if identical_num not in self.profs: print('invalid professor')
    else:
      prof = self.profs[identical_num]
      print(prof.name, prof.field, *[self.classes[cls_id].name for cls_id in prof.classes])
  
  def class_status(self, class_id):
    if class_id not in self.classes: print('invalid class')
    else:
      cls = self.classes[class_id]
      print(getattr(self.profs.get(cls.professor),'name',None), *[self.students[stu_id].name for stu_id in cls.students])
      
  def set_final_mark(self, professor_identical_num, student_identical_num, class_id, mark):
    if professor_identical_num not in self.profs: print('invalid professor')
    elif student_identical_num not in self.students: print('invalid student')
    elif class_id not in self.classes: print('invalid class')
    else:
      prof, cls, stu = self.profs[professor_identical_num], self.classes[class_id], self.students[student_identical_num]
      if cls.professor != professor_identical_num: print('professor class is not match')
      elif class_id not in stu.classes: print('student did not registered')
      else:
        stu.classes[class_id] = mark
        print('student final mark added or changed')

  def mark_student(self, identical_num, class_id):
    if identical_num not in self.students: print('invalid student')
    elif class_id not in self.students[identical_num].classes: print('student did not registered')
    else: print(self.students[identical_num].classes[class_id])
  
  def mark_list(self, class_id):
    if class_id not in self.classes: print('invalid class')
    elif not self.classes[class_id].professor: print('no professor')
    elif not self.classes[class_id].students: print('no student')
    else:
      cls = self.classes[class_id]
      res = [self.students[stu_id].classes[class_id] for stu_id in cls.students]
      print(*res)
    
  def top_mark(self, class_id):
    if class_id not in self.classes: print('invalid class')
    else:
      cls = self.classes[class_id]
      res = [self.students[stu_id].classes[class_id] for stu_id in cls.students]
      if not res: print(None)
      else: print(max(res))

  def average_mark_student(self, identical_num):
    if identical_num not in self.students: print('invalid student')
    else:
      marks = [float(stu_mark) for (cls_id, stu_mark) in self.students[identical_num].classes.items() if stu_mark != None]
      if not marks: print('None')
      else: print('%.2f'%(sum(marks)/len(marks)))

  def get_student_mark_for_course(self, student, course):
    return self.students[student].classes.get(course, None)

  def average_mark_professor(self, identical_num):
    if identical_num not in self.profs: print('invalid professor')
    else:
      marks = []
      for course in self.profs[identical_num].classes:
        for student in self.classes[course].students:
          marks.append(self.students[student].classes[course])
      marks = [float(m) for m in marks if m!=None]
      if not marks: print('None')
      else: print('%.2f'%(sum(marks)/len(marks)))

  def avg_marks_stu(self, identical_num):
    marks = [float(stu_mark) for (cls_id, stu_mark) in self.students[identical_num].classes.items() if stu_mark != None]
    return sum(marks)/len(marks)

  def top_student(self, field, entering_year):
    cases = [stu_id for stu_id in self.students if self.students[stu_id].field == field and self.students[stu_id].entering_year == entering_year]
    if not cases: print('None')
    else: 
      top_stu_id = cases[0]
      top_stu_mark = self.avg_marks_stu(cases[0])
      for c in cases:
        if top_stu_mark < self.avg_marks_stu(c):
          top_stu_id = c
          top_stu_mark = self.avg_marks_stu(c)
      print(self.students[top_stu_id].name)

g = Golestan()
while True:
  cmd = input()
  if cmd == 'end': break
  cmd = cmd.split()
  Golestan.__dict__[cmd[0]](g, *cmd[1:])
