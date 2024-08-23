from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .utils import generate_slug

User=get_user_model()

class StudentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

# Create your models here.
class Recipe(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    recipe_name = models.CharField(max_length=100)
    slug=models.SlugField(unique=True)
    recipe_description = models.TextField(max_length=100)
    recipe_image = models.ImageField(upload_to="recipe")
    recipe_view_count = models.IntegerField(default=1)
  

  

    def save(self, *args, **kwargs):
        self.slug = generate_slug(self.recipe_name)
        super(Recipe,self).save(*args, **kwargs)
    

  
class Department(models.Model):
    department=models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.department
    class Meta:
        ordering = ['department']

class StudentID(models.Model):
    student_id = models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.student_id
    
class Student(models.Model):
    department=models.ForeignKey(Department,related_name="depart",on_delete=models.CASCADE)
    student_id=models.OneToOneField(StudentID,related_name="studentid",on_delete=models.CASCADE)
    student_name=models.CharField(max_length=100)
    student_age=models.IntegerField(default=18)
    student_email=models.EmailField(unique=True)
    student_address=models.TextField()
    is_deleted = models.BooleanField(default=False)

    objects=StudentManager()
    admin_objects=models.Manager()

    def __str__(self) -> str:
        return self.student_name
    class Meta:
        ordering=['student_name']
        verbose_name='student'

class Subject(models.Model):
    subject_name = models.CharField(max_length=100)

    def __str__(self) -> str:
         return self.subject_name


class SubjectMarks(models.Model):
    student=models.ForeignKey(Student,related_name="studentmarks",on_delete=models.CASCADE)
    subject=models.ForeignKey(Subject,related_name="subject",on_delete=models.CASCADE)
    marks=models.IntegerField()

    def __str__(self) -> str:
        return f'{self.student.student_name}{self.subject.subject_name}'
    
    class Meta:
        unique_together=['subject','student']


class ReportCard(models.Model):
      student=models.ForeignKey(Student,related_name="studentreportcard",on_delete=models.CASCADE)
      student_rank=models.IntegerField()
      date_of_reportcard_generation=models.DateField(auto_now_add=True)

      class Meta:
          unique_together =['student_rank', 'date_of_reportcard_generation']
     
