from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q,Sum

from django.contrib.auth import get_user_model

User=get_user_model
# Create your views here.
@login_required(login_url="/login/")
def recipe(request):
    if request.method =="POST":
      data=request.POST
      recipe_name=data.get("recipe_name")
      recipe_description=data.get("recipe_description")
      recipe_image = request.FILES.get("recipe_image")
    
      Recipe.objects.create(recipe_name=recipe_name, recipe_description=recipe_description, recipe_image=recipe_image)
      return redirect("/recipe/")
    queryset = Recipe.objects.all()

    if request.GET.get('search'):
       queryset=queryset.filter(recipe_name__icontains=request.GET.get('search'))

    context= {"recipe":queryset}
    return render(request, 'recipe.html',context)

@login_required(login_url="/login/")
def delete_recipe(request,id):
   queryset = Recipe.objects.get(id=id)
   queryset.delete()
   return redirect("/recipe/")

@login_required(login_url="/login/")
def update_recipe(request,slug):
   queryset = Recipe.objects.get(slug=slug)

   if request.method == "POST":
      data=request.POST

      recipe_name=data.get("recipe_name")
      recipe_description=data.get("recipe_description")
      recipe_image = request.FILES.get("recipe_image")

      queryset.recipe_name=recipe_name 
      queryset.recipe_description=recipe_description

      if recipe_image:
         queryset.recipe_image=recipe_image

      queryset.save()
      return redirect("/recipe/")   

   context={"recipe":queryset}
   return render(request,'updaterecipe.html',context)

def login_page(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request,"invalid username")
            return redirect('/login/')
        user=authenticate(username=username,password=password)
        if user is None:
            messages.error(request,"invalid Password")
            return redirect('/login/')
        else:
            login(request,user)
            return redirect('/recipe/')
    
    return render(request,'Login.html')


@login_required(login_url="/login/")
def logout_page(request):
   logout(request)
   return redirect('/login/')

def register_page(request):
   if request.method == 'POST':
     first_name = request.POST.get('first_name')
     last_name = request.POST.get('last_name')
     username=request.POST.get('username')
     password=request.POST.get('password')

     user=User.objects.filter(username=username)
     if user.exists():
        messages.info(request,'username already exists')
        return redirect('/register')


     user=User.objects.create(first_name=first_name, last_name=last_name, username=username)
     user.set_password(password)
     user.save()

     messages.success(request,"account created successfully")
     return redirect("/register/")
   return render(request,'Register.html')


def get_student(request):
   queryset = Student.objects.all()

   if request.GET.get('search'):
      search=request.GET.get('search')

     
      queryset=queryset.filter( Q(student_name__icontains = search) |
      Q(department__department__icontains= search) |
      Q(student_id__student_id__icontains = search) |
      Q(student_email__icontains = search) |
      Q(student_age__icontains = search)
      )

   paginator = Paginator(queryset,10)
   page_number = request.GET.get("page",1)
   page_obj=paginator.get_page(page_number)
   
   return render(request,'report/student.html',{'queryset':page_obj})


from .seed import generate_reportcard
def see_marks(request,student_id):
   
   queryset=SubjectMarks.objects.filter(student__student_id__student_id=student_id)
   total_marks=queryset.aggregate(total_marks=Sum('marks'))
     
   return render(request,'report/see_marks.html',{'queryset':queryset,'total_marks':total_marks})
