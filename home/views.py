from django.shortcuts import render,redirect
from django.http import HttpResponse
from veg.seed import *
from .utils import send_email_with_attachment
from django.conf import settings
from .models import Cars
# Create your views here.

def send_email(request):
    subject="this email is from django with attachment"
    message="This email is from django with this is message"
    recipient_list = ["mohammedafsahkhan@gmail.com"]
    file_path=f"{settings.BASE_DIR}/main.xlsx"
    send_email_with_attachment(subject,message,recipient_list,file_path)
    return redirect("/")

def home(request):
    # seed_db(100)

    Cars.objects.create(carname=f"Nexon-{random.randint(0,100)}")
    peoples=[
        {"name":"afsah","age":23},
        {"name":"varun","age":17},
        {"name":"kashi","age":28}
    ]
    text= """
        Lorem ipsum dolor sit, amet consectetur adipisicing elit. Unde doloribus tenetur nobis odio quaerat ad quis in corporis exercitationem dolorum! Quo odio necessitatibus ex sint nisi pariatur esse, earum quibusdam.
    """
    vegetables=["pumpkin","tomato","potato"]
    return render(request,"index.html",context={"peoples":peoples,"text":text,"vegetables":vegetables,"page":"django main"})


def about(request):
    context={"page":"about"}
    return render(request,"about.html",context)
def contact(request):
    context={"page":"contact"}
    return render(request,"contact.html",context)