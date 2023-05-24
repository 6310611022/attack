from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from .forms import SignUpForm, UpdateUserForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('web:login'))
    return render(request,"web/index.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('web:index'))
        else:
            if User.objects.filter(username=username).count() == 0:
                return render(request, "web/login.html", {
                    'message': 'Invalid username and password.'
                })
            elif (User.objects.filter(username=username).count() == 1) and (User.objects.get(username=username).password != password):
                return render(request, "web/login.html", {
                    'message': 'Invalid password.'
                })
            
    return render(request, 'web/login.html')

def logout_view(request):
    logout(request)
    return render(request, "web/login.html", {
                'message': 'You are logged out.'
            })
    
    
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'web/login.html')

    else:
        form = SignUpForm()

    return render(request, 'web/signup.html', {'form':form}, status=200)

@login_required(login_url='/web/login')
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()

            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='/profile')
    else:
        user_form = UpdateUserForm(instance=request.user)

    return render(request, 'web/profile.html', {'user_form': user_form })

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'web/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = '/login'