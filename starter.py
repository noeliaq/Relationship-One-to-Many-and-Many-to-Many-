"""
Exercise: School Enrollment System
Module 3 | Lesson 8 | ~35 min

Objective:
  Build a school database with both a one-to-many relationship
  (Department -> Teacher -> Course) and a many-to-many relationship
  (Course <-> Student), using SQLAlchemy's relationship() and an
  association table.
"""

from sqlalchemy import (
    create_engine, String, Integer, ForeignKey, Table, Column, select
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from typing import List

engine = create_engine("sqlite:///:memory:", echo=False)


class Base(DeclarativeBase):
    pass


# ── TODO: Uncomment and complete the association table ────────────────────────
# This table links students to courses (many-to-many).
# It has no extra columns — just two foreign keys, both part of the PK.
#
student_courses = Table(
    "student_courses",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("course_id",  Integer, ForeignKey("courses.id"),  primary_key=True),
)


# ── TODO: Implement the Department model ──────────────────────────────────────
# Table name: "departments"
# Columns:
#   id   — Integer, primary key
#   name — String, required, unique
# Relationship: one department -> many teachers
class Department(Base):
    __tablename__ = "departments"
    # TODO: id, name columns
    id: Mapped [int] = mapped_column( primary_key=True)
    name: Mapped [str] = mapped_column (String(100), nullable= False) 
    # TODO: relationship to Teacher (back_populates="department")
    teachers: Mapped[list["Teacher"]]= relationship(back_populates= "department" )  #attribute name, list of teachers, backpopulates= two way mirror link , establish synchornization
    def __repr__(self):
        return f"Department (name = '{self.name}))"


# ── TODO: Implement the Teacher model ─────────────────────────────────────────
# Table name: "teachers"
# Columns:
#   id            — Integer, primary key
#   name          — String, required
#   department_id — Integer, ForeignKey("departments.id")
# Relationships:
#   department (many-to-one, back_populates="teachers")  # many teachers belog to one department 
#   courses    (one-to-many, back_populates="teacher")  # one teacher can have many courses
class Teacher(Base):
    __tablename__ = "teachers"
    # TODO: columns and relationships
    id: Mapped [int] = mapped_column( primary_key= True)
    name: Mapped[str] = mapped_column(String(100), nullable= False)
    department_id: Mapped [int] = mapped_column(ForeignKey("departments.id"))

    department: Mapped["Department"] = relationship(back_populates="teachers")  #many teacher belongs to one department 
    courses: Mapped[list["Course"]]= relationship (back_populates="teacher") #one teacher can have many courses 

    def __repr__(self):
        return f"Teacher (name = '{self.name}))"
# ── TODO: Implement the Course model ──────────────────────────────────────────
# Table name: "courses"
# Columns:
#   id         — Integer, primary key
#   title      — String, required
#   teacher_id — Integer, ForeignKey("teachers.id")
# Relationships:
#   teacher  (many-to-one, back_populates="courses")
#   students (many-to-many via student_courses, back_populates="courses")
class Course(Base):
    __tablename__ = "courses"
    # TODO: columns and relationships
    # TODO: students = relationship("Student", secondary=student_courses, back_populates="courses")
    id: Mapped[int] = mapped_column(primary_key= True)
    title: Mapped[str] = mapped_column (String(200), nullable= False)
    teacher_id: Mapped[int] = mapped_column (ForeignKey("teachers.id"))

    teacher: Mapped ["Teacher"] = relationship(back_populates="courses") #many courses belong to one teacher

    students: Mapped[list["Student"]] =relationship(secondary=student_courses, back_populates= "courses")  #a student can have many courses , one course can have many students
    def __repr__(self):
        return f"Course (title = '{self.title}))"

# ── TODO: Implement the Student model ─────────────────────────────────────────
# Table name: "students"
# Columns:
#   id    — Integer, primary key
#   name  — String, required
#   email — String, unique, required
# Relationship:
#   courses (many-to-many via student_courses, back_populates="students")
class Student(Base):
    __tablename__ = "students"
    # TODO: columns and relationships
    id: Mapped [int] = mapped_column (primary_key= True)
    name: Mapped [str] = mapped_column (String(200), nullable= False)
    email: Mapped [str] = mapped_column (String(200), unique=True, nullable= False)

    #Tells SQLAlchemy and Python type checkers that course.students will behave like a Python list containing Student objects.
    courses: Mapped[list["Course"]] =relationship(secondary=student_courses, back_populates="students") #table nmae 

    def __repr__(self):
        return f"Student (name = '{self.name}))"
# ── Test block ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        # ── Seed: 2+ departments, 4+ teachers, 5+ courses ────────────────────
        cs   = Department(name="Computer Science")
        math = Department(name="Mathematics")
        session.add_all([cs, math])
        session.flush()

        t1 = Teacher(name="Dr. Alice Park",   department_id=cs.id)
        t2 = Teacher(name="Prof. Bob Chen",   department_id=cs.id)
        t3 = Teacher(name="Dr. Carol White",  department_id=math.id)
        t4 = Teacher(name="Prof. Dan Rivera", department_id=math.id)
        session.add_all([t1, t2, t3, t4])
        session.flush()

        c1 = Course(title="Intro to Python", teacher_id=t1.id)
        c2 = Course(title="Data Structures",  teacher_id=t1.id)
        c3 = Course(title="Web Development",  teacher_id=t2.id)
        c4 = Course(title="Calculus I",       teacher_id=t3.id)
        c5 = Course(title="Linear Algebra",   teacher_id=t4.id)
        session.add_all([c1, c2, c3, c4, c5])
        session.flush()

        # ── Seed: 6+ students with various enrollments ───────────────────────
        s1 = Student(name="Zoe Adams",   email="zoe@school.edu")
        s2 = Student(name="Raj Patel",   email="raj@school.edu")
        s3 = Student(name="Nina Brown",  email="nina@school.edu")
        s4 = Student(name="Marco Diaz",  email="marco@school.edu")
        s5 = Student(name="Yuki Tanaka", email="yuki@school.edu")
        s6 = Student(name="Olu Okafor",  email="olu@school.edu")
        session.add_all([s1, s2, s3, s4, s5, s6])
        session.flush()

        # TODO: enroll students in courses using the relationship
        # Example: s1.courses.append(c1)

        s1.courses.append(c1)
        s2.courses.append(c1)
        s3.courses.append(c1)
        s4.courses.append(c1)
        s5.courses.append(c5)
        s6.courses.append(c4)


        session.commit()

    # ── Demo 1: each department and its teachers ────────────────────────────
    print("=== Departments and Teachers ===")
    # TODO: query all departments and print each one with its teachers
    with Session(engine) as session: 
        #table
        departments  = session.query(Department).all() #gives all departments
        for department in departments: #loops through each department one by one
            print(f"\n{department.name} ({len(department.teachers)} teachers):")
            for teacher in department.teachers: #access to relationship define in Department model
                print(f"- {teacher.name}")

    # ── Demo 2: each teacher and the courses they teach ─────────────────────
    print("\n=== Teachers and Their Courses ===")
    # TODO: query all teachers and print each one with the courses they teach
    
    with Session(engine) as session:
        teachers = session.query(Teacher).all() #queies teacher table 
        for teacher in teachers: 
            print(f"\n{teacher.name} ({len(teacher.courses)} courses)") #lenght of how many courses teacher teaches
            for course in teacher.courses:  #loops through collection of Course objects 
                print(f"- {course.title}")

    # ── Demo 3: each course with its enrolled students ──────────────────────
    print("\n=== Courses and Enrolled Students ===")
    # TODO: query all courses and print each one with its students

    with Session(engine) as session:
        courses = session.query(Course).all()
        for course in courses:
            print(f"\n {course.title} ({len(course.students)} student(s)")   #course from loop , students from attribute Course table 
            for student in course.students:
                print (f"- {student.name}") 


    # ── Demo 4: each student and the courses they're enrolled in ────────────
    print("\n=== Students and Their Courses ===")
    # TODO: query all students and print each one with their courses
    with Session(engine) as session:
        students = session.query(Student).all()
        for student in students:
            print(f"\n{student.name}")
            for course in student.courses:
                print(f"- {course.title}")
   

    # ── Demo 5: any course with more than 3 students ────────────────────────
    print("\n=== Courses With More Than 3 Students ===")
    # TODO: hint - course.students is already a Python list, so len() works.
    # No need for func.count() / group_by() here.
    with Session(engine) as session:
        courses = session.query(Course).all()
        for course in courses:
            if len(course.students) > 3:

            # student_count = len(course.students) #course is the loop, students is the attribute inside Course model
                print (f" {course.title} ({len(course.students)} student(s)")
                for student in course.students:
                    print (f"\n - {student.name}")


"""RESULTS

(venv) noeliaquiroga@Noelias-MacBook-Pro sqlAlchemy_Relationships % python3 starter.py
=== Departments and Teachers ===

Computer Science (2 teachers):
- Dr. Alice Park
- Prof. Bob Chen

Mathematics (2 teachers):
- Dr. Carol White
- Prof. Dan Rivera

=== Teachers and Their Courses ===

Dr. Alice Park (2 courses)
- Intro to Python
- Data Structures

Prof. Bob Chen (1 courses)
- Web Development

Dr. Carol White (1 courses)
- Calculus I

Prof. Dan Rivera (1 courses)
- Linear Algebra

=== Courses and Enrolled Students ===

 Intro to Python (4 student(s)
- Zoe Adams
- Raj Patel
- Nina Brown
- Marco Diaz

 Data Structures (0 student(s)

 Web Development (0 student(s)

 Calculus I (1 student(s)
- Olu Okafor

 Linear Algebra (1 student(s)
- Yuki Tanaka

=== Students and Their Courses ===

Zoe Adams
- Intro to Python

Raj Patel
- Intro to Python

Nina Brown
- Intro to Python

Marco Diaz
- Intro to Python

Yuki Tanaka
- Linear Algebra

Olu Okafor
- Calculus I

=== Courses With More Than 3 Students ===
 Intro to Python (4 student(s)

 - Zoe Adams

 - Raj Patel

 - Nina Brown

 - Marco Diaz
(venv) noeliaquiroga@Noelias-MacBook-Pro sqlAlchemy_Relationships % 
"""