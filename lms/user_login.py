from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from app.models import User_Profile
from app.EmailBackEnd import EmailBackEnd
from django.core.files.storage import FileSystemStorage

def REGISTER(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.warning(request,"Email are Already Exists !")
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.warning(request,"Username are Already Exists !")
            return redirect('register')

        user = User(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        return redirect('login')


    return render(request,'registration/register.html')

def LOGIN(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = EmailBackEnd.authenticate(request,username=email,password=password)

        if user != None:
            login(request,user)
            return redirect('home')
        else:
            messages.warning(request,"Somthing was wrong !")
            return redirect('login')

    return None

def LOGOUT(request):
    logout(request)
    return redirect('login')

def PROFILE(request):

    user_profile = User_Profile.objects.filter(user=request.user)
    data = {
        
    }

    if user_profile.exists():
        data = {
            'user_profile':user_profile.first
        }
        
    return render(request,'registration/profile.html',data)
    
    
def PROFILE_UPDATE(request):
    if request.method == "POST":
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        userid = request.user.id

        user = User.objects.get(id=userid)
        user.first_name = firstname
        user.last_name = lastname

        if password != None and password != "":
            user.set_password(password)
        
        user.save()
        messages.success(request,"Profile Updated !")
        return redirect('profile')

    return None

def IMAGE_UPLOAD(request):

    if request.method == "POST" and request.FILES['image']:
        image = request.FILES['image']
        fss = FileSystemStorage()
        file = fss.save('userprofileimage/ '+request.user.username+'.jpg',image)
        file_url = fss.url(file)

        user = User_Profile.objects.filter(user=request.user)
        if user.exists():
            userimg = User_Profile.objects.get(user=request.user)
            userimg.user = request.user
            userimg.profile_image = file_url
            userimg.save()
            messages.success(request,"Image Uploaded !")
            return redirect('profile')
        else:
            userimg = User_Profile(
                user=request.user,
                profile_image=file_url,
            )
            userimg.save()
            messages.success(request,"Image Uploaded !")
            return redirect('profile')

    return redirect('profile')
