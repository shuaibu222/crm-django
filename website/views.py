from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignupForm, AddRecordForm
from .models import Record

def home(request):
    records = Record.objects.all()
    return render(request, 'home.html', {'records':records})

def login_user(request):
    if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You are now logged in!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('login_user')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, 'You are now logged out!')
    return redirect('home')

def register_user(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('home')
	else:
		form = SignupForm()
		return render(request, 'register.html', {'form':form})

	return render(request, 'register.html', {'form':form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'record':record})
    else:
        messages.error(request, 'You must be logged in!')
        return redirect('login_user')

def delete_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(id=pk)
        record.delete()
        messages.success(request, 'Record deleted successfully!')
        return redirect('home')
    else:
        messages.error(request, 'You must be logged in!')
        return redirect('login_user')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                    form.save()
                    messages.success(request, 'Record added successfully!')
                    return redirect('home')
        else:
            form = AddRecordForm()
            return render(request, 'add_record.html',{'form':form})
    else:
        messages.error(request, 'You must be logged in!')
        return redirect('login_user')

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, 'Record updated successfully!')
                return redirect('home')
        else:
            form = AddRecordForm(instance=current_record)
            return render(request, 'update_record.html',{'form':form})
    else:
        messages.error(request, 'You must be logged in!')
        return redirect('login_user')