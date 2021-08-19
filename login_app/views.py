from django.shortcuts import redirect, render, HttpResponse
from django.contrib import messages
from .models import User, UserManager
import bcrypt

def register(request):
    pass
    if request.method == "GET":
        return render (request, 'login_and_regis.html')
    elif request.method == "POST":
        # Validates input data meets standards in models
        errors = User.objects.registration_validator(request.POST)
        if len(errors)>0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        # Sends data and creates objects is everything is verified
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            new_user = User.objects.create(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                email=request.POST['email'],
                password=pw_hash,
            )
            # Saves data in sessions for future use.
            request.session['user_id'] = new_user.id
            request.session['first_name']=new_user.first_name

            return redirect('/success')
    else:
        return redirect ('/')

def success(request):
    # Checks method and redirects on unapproved reuest method.
    if request.method == "GET":
        if 'user_id' in request.session:
            context = {
                "user" : request.session
            }
            return render(request,'success.html', context)
        else:
            return redirect ('/')
    return redirect ('/')

def users(request):
    context = {
    "users" : User.objects.all(),
    }
    return render(request, 'users.html', context)

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    elif len(errors)==0:
        logged_user=User.objects.get(email=request.POST['email'])
        request.session['user_id']=logged_user.id
        request.session['first_name']=logged_user.first_name
        return redirect('/success')
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')