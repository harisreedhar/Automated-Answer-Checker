from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout as logouts
from django.contrib import messages
import random
import json

def register_view(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully registered")
            return redirect(reverse('register'))
    return render(request, 'register.html', {'form': form})

def logout(request):
    if request.method == 'POST':
        logouts(request)
        return redirect('home')
