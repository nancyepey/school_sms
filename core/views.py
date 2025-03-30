from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser, PasswordResetRequest
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
#login required
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        # role = request.POST.get('role')  # Get role from the form (student, teacher, or admin)
        role = 'admin'
        
        # Create the user
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            name=name,
            password=password,
        )
        
        # Assign the appropriate role
        if role == 'student':
            user.is_student = True
        elif role == 'teacher':
            user.is_teacher = True
        elif role == 'admin':
            user.is_admin = True

        user.save()  # Save the user with the assigned role
        login(request, user)
        messages.success(request, 'Signup successful!')
        return redirect('index')  # Redirect to the index or home page
    return render(request, 'authentication/register.html')  # Render signup template



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            next_param = request.POST.get('next')
            print(next_param)
            # if next_param:
            #     url = next_param
            #     #new code
            #     if url != '':
            #         if url == "/":
            #             pass
            #         else:
            #             return redirect(url)
            # else:
            #     # Redirect user based on their role
            #     if user.is_admin:
            #         url = reverse('admin_dashboard')
            #     elif user.is_teacher:
            #         url = reverse('teacher_dashboard')
            #     elif user.is_student:
            #         url = reverse('dashboard')
            #     else:
            #         messages.error(request, 'Invalid user role')
            #         return redirect('index')
            # return redirect(url)
                
            
            # # Redirect user based on their role
            if user.is_admin:
                return redirect('admin_dashboard')
            elif user.is_teacher:
                return redirect('teacher_dashboard')
            elif user.is_student:
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid user role')
                return redirect('index')  # Redirect to index in case of error
            
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'authentication/login.html')  # Render login template




def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = CustomUser.objects.filter(email=email).first()
        
        if user:
            token = get_random_string(32)
            reset_request = PasswordResetRequest.objects.create(user=user, email=email, token=token)
            reset_request.send_reset_email()
            messages.success(request, 'Reset link sent to your email.')
        else:
            messages.error(request, 'Email not found.')
    
    return render(request, 'authentication/forgot-password.html')  # Render forgot password template


@login_required
def reset_password_view(request, token):
    reset_request = PasswordResetRequest.objects.filter(token=token).first()
    
    if not reset_request or not reset_request.is_valid():
        messages.error(request, 'Invalid or expired reset link')
        return redirect('index')

    if request.method == 'POST':
        new_password = request.POST['new_password']
        reset_request.user.set_password(new_password)
        reset_request.user.save()
        messages.success(request, 'Password reset successful')
        return redirect('login')

    return render(request, 'authentication/reset_password.html', {'token': token})  # Render reset password template


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')
