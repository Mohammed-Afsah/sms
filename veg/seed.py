from faker import Faker
import random
from .models import *
fake = Faker()
from django.db.models import Sum

def create_subject_marks(n):
    try:
        subjects = Subject.objects.all()
        students = Student.objects.all()

        for _ in range(n):
            student = random.choice(students)
            for subject in subjects:
              if not SubjectMarks.objects.filter(student=student, subject=subject).exists():
                SubjectMarks.objects.create(
                    student=student,
                    subject=subject,
                    marks=random.randint(0, 100)
                )
    except Exception as e:
        print(e)

def seed_db(n=20)->None:
    try: 
        for _ in range(n):

            department_objs = Department.objects.all()
            random_index = random.randint(0,len(department_objs)-1)

            student_id=f'STU-0{random.randint(100, 999)}'
            department=department_objs[random_index]
            student_name=fake.name()
            student_age=random.randint(20,30)
            student_email=fake.email()
            student_address=fake.address()

            student_id_obj=StudentID.objects.create(student_id=student_id)

            student_obj=Student.objects.create(
                department=department,
                student_id=student_id_obj,
                student_name=student_name,
                student_email=student_email,
                student_age=student_age,
                student_address=student_address,
            )

    except Exception as e:
        print(e)


def generate_reportcard():
   ranks=Student.objects.annotate(marks=Sum('studentmarks__marks')).order_by('-marks','student_age')
   i=1
   for rank in ranks:
     ReportCard.objects.create(
         student = rank,
         student_rank = i
     )
     i = i+1