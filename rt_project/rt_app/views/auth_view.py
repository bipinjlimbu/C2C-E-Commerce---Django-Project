from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import User

def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect('/')
    
    errors = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username:
            errors['username'] = "Username is required."
        if not password:
            errors['password'] = "Password is required."
            
        if errors:
            return render(request, 'auth/login_page.html', {'errors': errors})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('/')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'auth/login_page.html', {'errors': errors})
        
    return render(request, 'auth/login_page.html', {'errors': errors})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('/login/')