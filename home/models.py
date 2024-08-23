from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
class Student(models.Model):
    # id=models.AutoField()
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    email=models.EmailField(null=True,blank=True)
    address=models.TextField(null=True,blank=True)
    file=models.FileField(null=True,blank=True)
    image=models.ImageField(null=True,blank=True)
    
class Cars(models.Model):
    carname=models.CharField(max_length=100)
    speed=models.FloatField(null=True)

    def __str__(self) -> str:
        return self.carname
    
@receiver(post_save,sender=Cars)
def call_car_api(sender,instance,**kwargs):
    print("Car Object Created")
    print(sender,instance,kwargs)