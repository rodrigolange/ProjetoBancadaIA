from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import HttpResponse


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        print(form.errors)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/usuarios")
        else:
            return HttpResponse(form.errors)
    form = NewUserForm
    return render(request=request, template_name="usuarios/register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/BancadaIA")
            else:
                messages.error(request, 'username or password not correct')
                return redirect('usuarios:login_request')

        else:
            messages.error(request, 'username or password not correct')
            return redirect('usuarios:login_request')

    form = AuthenticationForm()
    context = {
        "login_form": form

    }
    return render(request=request, template_name="usuarios/login.html", context=context)


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("usuarios:login_request")
