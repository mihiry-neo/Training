from db_connection import load_db_connection

def execute_query(cursor, title, query):
    print(f"{title}")
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    if not rows:
        print("No results found.")

def run_join_queries():
    conn = load_db_connection()
    cursor = conn.cursor()

    queries = [
        {
            "title": "Inner Join: Students x Courses x Enrollments",
            "sql": """
                SELECT s.name, c.title, e.grade
                FROM students s 
                INNER JOIN enrollments e ON s.id = e.student_id
                INNER JOIN courses c ON c.id = e.course_id
            """
        },
        {
            "title": "Inner Join: All courses with at least one student involved",
            "sql": """
                SELECT c.title, COUNT(e.student_id) 
                FROM courses c
                INNER JOIN enrollments e ON c.id = e.course_id
                GROUP BY c.id
            """
        },
        {
            "title": "Left Join: Students and their Enrollments",
            "sql": """
                SELECT s.name, e.grade
                FROM students s
                LEFT JOIN enrollments e ON s.id = e.student_id
            """
        },
        {
            "title": "Left Join: Students enrolled in exactly zero or more than one course",
            "sql": """
                SELECT s.name, COUNT(e.course_id) AS total_courses
                FROM students s 
                LEFT JOIN enrollments e ON s.id = e.student_id
                GROUP BY s.id
                HAVING total_courses != 1
            """
        },
        {
            "title": "Right Join: Courses and number of students enrolled in them",
            "sql": """
                SELECT c.title, COUNT(e.student_id)
                FROM courses c
                RIGHT JOIN enrollments e ON c.id = e.course_id
                GROUP BY c.id
            """
        },
        {
            "title": "Right Join: Show all enrollments where courses are null",
            "sql": """
                SELECT e.*
                FROM courses c
                RIGHT JOIN enrollments e ON c.id = e.course_id
                WHERE c.id IS NULL
            """
        },
        {
            "title": "Full Outer Join: All Students + All Enrollments",
            "sql": """
                SELECT s.name, e.grade
                FROM students s
                LEFT JOIN enrollments e ON s.id = e.student_id
                UNION
                SELECT s.name, e.grade
                FROM students s
                RIGHT JOIN enrollments e ON s.id = e.student_id
            """
        },
        {
            "title": "Full Outer Join: All Courses + All Enrollments",
            "sql": """
                SELECT c.title, e.grade
                FROM courses c
                LEFT JOIN enrollments e ON c.id = e.course_id
                UNION
                SELECT c.title, e.grade
                FROM courses c
                RIGHT JOIN enrollments e ON c.id = e.course_id
            """
        },
        {
            "title": "Cross Join: All possible Student + Courses combination",
            "sql": """
                SELECT s.name, c.title
                FROM students s
                CROSS JOIN courses c
            """
        },
        {
            "title": "Cross Join: All possible Courses + Enrollments combination",
            "sql": """
                SELECT c.title, e.grade
                FROM courses c
                CROSS JOIN enrollments e
            """
        },
        {
            "title": "Left Anti Join: All students who are not enrolled in any course",
            "sql":"""
                Select s.id, s.name
                from students s
                left join enrollments e on s.id = e.student_id
                where e.student_id is null
                """
        },
        {
            "title": "Left Anti Join: All students who haven't received any grade",
            "sql":"""
                Select s.id, s.name
                from students s
                left join enrollments e on s.id = e.student_id
                where e.grade is null
                """
        },
        {
            "title": "Right Anti Join: Courses that have no students enrolled",
            "sql":"""
                Select c.id, c.title
                from courses c
                left join enrollments e on c.id = e.course_id
                where e.course_id is null
                """
        },
        {
            "title": "Right Anti Join: Enrollments with students id not in Students table",
            "sql":"""
            Select e.*
            from enrollments e
            left join students s on s.id = e.student_id
            where s.id is null
            """
        },
        {
            "title":"Union: Students and Course Instructor Name (No duplicates)",
            "sql":"""
            select s.name from students s
            union
            select c.instructor_name from courses c
            """
        },
        {
            "title":"Union: Students and Course Instructor Name (with duplicates)",
            "sql":"""
            select s.name from students s
            union all
            select c.instructor_name from courses c
            """
        },
        {
            "title":"Finding students with the same age",
            "sql":"""
            SELECT s1.id AS student1_id, s1.name AS student1_name,
            s2.id AS student2_id, s2.name AS student2_name,
            s1.age
            FROM students s1
            JOIN students s2 ON s1.age = s2.age AND s1.id < s2.id;
            """
        }

    ]

    for q in queries:
        execute_query(cursor, q["title"], q["sql"])

    cursor.close()
    conn.close()


run_join_queries()
