from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from core.forms import AnswerSheetForm, AnswerKeyForm
from core.models import AnswerSheets, AnswerKeys
import random
import json

@login_required()
def home(request):
    form = AnswerKeyForm()
    datas = AnswerSheets.objects.all()
    if request.method == 'POST':
        form = AnswerKeyForm(request.POST)
        if form.is_valid():
            print(request.POST)
            return redirect('home')
    return render(request, 'home.html', {'form': form, 'datas': datas})

@login_required()
def answerKeyUpload(request):
    form = AnswerKeyForm()
    outData = ""
    if request.method == 'POST':
        form = AnswerKeyForm(request.POST)
        if form.is_valid():
            data = AnswerKeys()
            data.subject_name = request.POST['subject_name']
            dictionary = {
                'Qn1':[request.POST['answer_1'], request.POST['mark_1']],
                'Qn2':[request.POST['answer_2'], request.POST['mark_2']],
                'Qn3':[request.POST['answer_3'], request.POST['mark_3']]
            }
            data.answer_key = dictionary
            data.save()
            messages.success(request, 'Form submission successful')
            return redirect('answer_key_upload')
    return render(request, 'upload_answerkey.html', {'form': form, 'outData': outData})

@login_required()
def answerSheetUpload(request):
    form = AnswerSheetForm()
    outData = AnswerKeys.objects.all()
    print(outData)
    if request.method == 'POST':
        form = AnswerSheetForm(request.POST, request.FILES)
        if form.is_valid():
            data = AnswerSheets()
            data.roll_number = request.POST['roll_number']
            data.student_name = request.POST['student_name']
            data.subject_name = request.POST['subject_name']
            data.answer_sheet = request.FILES['answer_sheet']
            data.save()
            messages.success(request, 'Form submission successful')
            return redirect('answer_sheet_upload')
    return render(request, 'upload_answersheet.html', {'form': form, 'outData': outData})

@login_required()
def delete(request, student_id):
    if request.method == 'POST':
        AnswerSheets.objects.get(id=student_id).delete()
        return redirect('home')

@login_required()
def teachers(request):
    form = KeyForm()
    dictionary = {}
    if request.method == 'POST':
        form = KeyForm(request.POST)
        if form.is_valid():
            # for i in range(3):
            #     data = request.POST[f'answer{i}']
            #     mark = request.POST[f'mark{i}']
            #     dictionary[f'id{i}'] = [data, int(mark)]

            # json_object = json.dumps(dictionary)
            # with open("/home/hari/Documents/College_Project/test_project/core/sample.json", "w") as outfile:
            #     outfile.write(json_object)
            data = request.POST['number']
            print(data)
            return redirect('teachers')

    return render(request, 'teachers.html', {'form': form})

