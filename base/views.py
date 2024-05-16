from django.shortcuts import render, redirect
from django.conf import settings
import random, string
from .models import User, ResetPassword
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.db.models import Q

# For SMTP Setup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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
 
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user is not None:
            token_string = string.ascii_letters + string.digits
            token_length = 15
            token = ''.join(random.choices(token_string, k=token_length))

            message = MIMEMultipart()
            message['From'] = settings.EMAIL_HOST_USER
            message['To'] = email
            message['Subject'] = 'Password Reset'
            body = f'Click the link to reset your password: http://127.0.0.1:8000/reset_password/{email}/{token}'
            message.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)

            try:
                server.starttls()
                server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                server.sendmail(settings.EMAIL_HOST_USER, email, message.as_string())
            except Exception as e:
                error_message = e
                return render(request, 'forgot_password.html', {'error_message':error_message})
            finally:
                server.quit()

            try:
                count = ResetPassword.objects.all().filter(Q(email=email) & Q(isUsed=False) | Q(isUsed=True))
                count.delete()
            except ObjectDoesNotExist:
                pass

            ResetPassword.objects.create(email=email, token=token, isUsed=False)

            success_message = f"Reset password link sent to {email}"
            return render(request, 'forgot_password.html', {'success_message':success_message})
        else:
            error_message = "No such user exists!"
            return render(request, 'forgot_password.html', {'error_message':error_message})
        
    return render(request, 'forgot_password.html')

def reset_password(request, email, token):
    try:
        check = ResetPassword.objects.get(email=email, token=token)
    except ResetPassword.DoesNotExist:
        check = None

    if request.method == 'POST' and check is not None:
        if request.POST.get('password') == request.POST.get('confirm_password'):
            update_user = User.objects.get(email=email)
            update_user.password = request.POST.get('password')

            isUsed = ResetPassword.objects.get(email=email, token=token)
            verify_token = True

            if isUsed.isUsed == True:
                verify_token = False
            
            if verify_token:
                isUsed.isUsed = True
                isUsed.save()
                update_user.save()

                success_message = "Password updated successfully!"
                return render(request, 'reset_password.html', {'email':email, 'token':token, 'success_message':success_message})
            else:
                error_message = "Token expired! Request a new password reset link."
                return render(request, 'reset_password.html', {'email':email, 'token':token, 'error_message':error_message})
        else:
            error_message = "Password didn't matched"
            return render(request, 'reset_password.html', {'email':email, 'token':token, 'error_message':error_message})
    
    if check is not None:
        return render(request, 'reset_password.html', {'email':email, 'token':token})
    else:
        return HttpResponse("Invalid Token, Please check the link sent to email!")