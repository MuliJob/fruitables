"""User authentication and authorization"""
from django.shortcuts import render, redirect


from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login
from django.contrib import messages


from . forms import CreateUserForm, LoginForm



def register(request):
    """User registration"""
    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, "Account created successfully! You can now log in.")

            return redirect("login")

    context = {
        'form':form
      }

    return render(request, 'auth/register.html', context=context)



def my_login(request):
    """User login"""

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            print("Form is valid")

            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')


            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect("shop")
            else:
                messages.error(request, "Invalid email or password.")

    context = {'form': form}
    return render(request, 'auth/login.html', context=context)


def user_logout(request):
    """Logout function"""
    auth.logout(request)

    return redirect("")
