from db_connection import load_db_connection
import random
from faker import Faker
import pymysql

fake = Faker()

def create_table():
    try:
        conn = load_db_connection()
        cursor = conn.cursor()
        print("Connecting....")

        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

        cursor.execute("DROP table if exists students")
        cursor.execute("DROP table if exists courses")
        cursor.execute("DROP table if exists enrollments")

        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

        cursor.execute("""
        Create table students(
                    id int primary key,
                    name varchar(50),
                    email varchar(100),
                    age int,
                    gender enum("Male","Female"))
        """
        )

        cursor.execute("""
        Create table courses(
                    id int primary key,
                    title varchar(100),
                    department varchar(100),
                    instructor_name varchar(100))
        """)

        cursor.execute("""
        Create table enrollments(
                    id int primary key,
                    student_id int,
                    course_id int,
                    grade varchar(2),
                    Foreign key (student_id) references students(id),
                    Foreign key (course_id) references courses(id))    
        """)


        Students = []
        for i in range(1,31):
            Students.append((i,fake.name(),fake.email(),random.randint(18,25),random.choice(["Male","Female"])))
        cursor.executemany("Insert into students (id, name, email, age, gender) values (%s, %s, %s, %s, %s)",Students)

        Courses = []
        departments = ["CS", "Pyscology", "Philosophy", "Physics", "Literature"]
        for i in range(1,8):
            Courses.append((i,fake.job(), random.choice(departments), fake.name()))
        cursor.executemany("Insert into courses (id, title, department, instructor_name) values (%s, %s, %s, %s)", Courses)

        Enrollments = []
        grades = ['A','B','C','D','E']
        enrollment_id = 1
        for student_id in range(1,28):
            enrolled_courses = random.sample(range(1,6),k=2)
            for course_id in enrolled_courses:
                Enrollments.append((enrollment_id, student_id, course_id, random.choice(grades)))
                enrollment_id += 1

        
        cursor.executemany("Insert into enrollments (id, student_id, course_id, grade) values (%s, %s, %s, %s)", Enrollments)




        conn.commit()
        cursor.close()
        conn.close()
        print("All the tables are created successfully")
    
    except pymysql.Error as err:
        print("❌ MySQL Error:", err)
    except Exception as e:
        print("❌ General Error:", e)

if __name__ == "__main__":
    create_table()
