from django.shortcuts import render, redirect
from core.forms import AnswerForm
from core.models import AnswerTable
import random

def home(request):
    form = AnswerForm()
    datas = AnswerTable.objects.all()
    import os
    print(os.path)
    if request.method == 'POST':
        form = AnswerForm(request.POST, request.FILES)
        if form.is_valid():
            data = AnswerTable()
            data.student_name = request.POST['student_name']
            data.subject_name = request.POST['subject_name']
            data.answer = request.FILES['answer']
            data.answer_key = request.FILES['answer_key']
            data.marks = random.randrange(100) # dummy random marks
            data.save()
            return redirect('home')
    return render(request, 'home.html', {'form': form, 'datas': datas})

def delete(request, student_id):
    if request.method == 'POST':
        AnswerTable.objects.get(id=student_id).delete()
        return redirect('home')
