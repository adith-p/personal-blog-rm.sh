from pathlib import Path
from django.conf import settings
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from blog.utls.serializer import JsonSerializer

from .models import AdminUser

# Create your views here.


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        print(username)
        print(password)

        if not AdminUser.objects.filter(username=username).exists():
            messages.error(request, message="User does not exist")
            return redirect("blog:bloglist")
        user = authenticate(request, username=username, password=password)

        print(user)
        if user:
            login(request, user)
            if request.user.is_authenticated:
                print("is_authenticated")
            return redirect("blog:bloglist")
        messages.add_message(request, level=1, message="invalid username or password")
    return render(request, template_name="user_auth/login.html")


def logout_user(request):
    logout(request)
    return redirect("blog:bloglist")


def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password1 != password2:
            messages.error(request, message="both password must be same")
            return redirect("user_auth:register")

        email = request.POST.get("email")

        if AdminUser.objects.filter(username=username).exists():
            messages.error(request, message="username already exist")
            return redirect("user_auth:register")

        user = AdminUser.objects.create_user(username=username, email=email)
        user.set_password(password1)
        user.save()

        login(request, user)
        messages.success(request, message="user created successfully")
        return redirect("blog:bloglist")
    return render(request, template_name="user_auth/register.html")


def profile(request):
    p = Path(f"{settings.BASE_DIR}/posts")
    post_list = [i for i in p.iterdir() if i.is_file()]

    json_data = JsonSerializer(post_list).serialize()
    return render(
        request,
        template_name="user_auth/profile.html",
        context={"json_data": json_data},
    )
