from django.shortcuts import render, redirect
from .models import User

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            request.session['user_id'] = user.id
            return redirect('dashboard')
        else:
            error_message = "Invalid credentials!"
            return render(request, 'login.html', {'error_message':error_message})
        
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        try:
            if password == confirm_password:
                User.objects.create(username=username, email=email, password=password)
                return redirect('login')
            else:
                error_message = "Password didn't matched"
                return render(request, 'register.html', {'error_message':error_message})
        except Exception:
            return redirect('login')

    return render(request, 'register.html')

def dashboard(request):
    id = request.session.get('user_id')
    if id is not None:
        try:
            data = User.objects.get(id=id)
            return render(request, 'dashboard.html', {'data':data})
        except User.DoesNotExist:
            del request.session['user_id']
            
    return redirect('login')

def logout(request):
    request.session.clear()
    
    return redirect('login')