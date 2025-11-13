import random
from demo.models import *
from faker import Faker
fake=Faker()

def create_subject_marks():
    try:
        student_obj=Student.objects.all()
        for student in student_obj:
            subject_obj= Subject.objects.all()
            for subject in subject_obj:
                StudentMarks.objects.create(
                    subject=subject,
                    student=student,
                    marks=random.randint(30,100)
                )
    except Exception as e:
        print(e)

def seed_db(n):
    try:
        for _ in range(0,n):
            department_obj=Department.objects.all()
            index=random.randint(0,len(department_obj)-1)
            department=department_obj[index]
            student_id=f'CS{random.randint(1000,4000)}'
            student_name=fake.name()
            student_email=fake.email()
            student_age=random.randint(18,30)
            student_address=fake.address()

            student_id_obj=StudentId.objects.create(student_id=student_id)

            student_obj=Student.objects.create(department=department,
                                               student_id=student_id_obj,
                                               student_name=student_name,
                                               student_email=student_email,
                                               student_age=student_age,
                                               student_address=student_address
                                               )
    except Exception as e:
        print(e)



from django.db.models import Sum
def generate_rank():
    ranks=Student.objects.annotate(marks=Sum('studentmarks__marks')).order_by('-marks')

    i=1
    for rank in ranks:
        studentmark = StudentMarks.objects.filter(student=rank)
        total_marks=studentmark.aggregate(marks=Sum('marks'))['marks']
        StudentReportCard.objects.create(student=rank,student_rank=i,total_marks=total_marks)
        i+=1

    return 0