from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@login_required(login_url="login")
def home(request):
    return render(request, "home.html", {})

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "login_user.html", {})

@login_required(login_url="login")
def logout_user(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("login")