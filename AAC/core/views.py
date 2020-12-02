from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from core.models import AnswerSheets, AnswerKeys, Grade
from core.forms import AnswerSheetForm, AnswerKeyForm
from django.contrib.auth.decorators import login_required
from core.calculate_mark import calculateMark


@login_required()
def home(request):
    form = AnswerKeyForm()
    datas = Grade.objects.all()
    if request.method == 'POST':
        form = AnswerKeyForm(request.POST)
        if form.is_valid():
            return redirect('home')

    return render(request, 'home.html', {'form': form, 'datas': datas})

@login_required()
def answerKeyUpload(request):
    form = AnswerKeyForm()
    dictionary = {}
    if request.method == 'POST':
        form = AnswerKeyForm(request.POST)
        if form.is_valid():
            subjectName = request.POST['subject_name']
            ansKey = request.POST['answer_key']
            marks = request.POST['marks']
            # convert string tuple into integer list
            marks = [int(s) for s in marks.split(',')]

            try:
                # dictionary creation from answer key input
                # exec() creates user inputs to actual variable that stores a tuple of values
                exec(ansKey)
                # iterate through marks with index i
                for i, m in enumerate(marks):
                    # stores user input value to dicionary
                    exec(f"dictionary[f'Qn{i+1}'] = [Qn{i+1}, m]")
                    pass
                # create new record or update existing based on availability of subject name
                create_Or_Update_AnswerKey(request, subjectName, dictionary)
            except:
                string = "Error! Answer Key creation failed<br/>"
                string += "Recheck:<br/>"
                string += "1) Number of questions and marks are same <br/>"
                string += "2) Answerkey is written in correct format"
                errorMessage = mark_safe(string)
                messages.success(request, errorMessage)

            return redirect('answer_key_upload')

    return render(request, 'upload_answerkey.html', {'form': form})


def create_Or_Update_AnswerKey(request, subjectName, key):
    # intialize a checker
    checker = None
    try:
        # check subject name is present in database
        checker = AnswerKeys.objects.get(subject_name=subjectName)
    except:
        pass

    if checker is None:
        data = AnswerKeys()
        data.answer_key = key
        data.subject_name = subjectName
        data.save()
        messages.success(request, mark_safe(
            f'Successfully added <b>{subjectName}</b> key'))
    else:
        checker.answer_key = key
        checker.save()
        messages.success(request, mark_safe(
            f'Successfully updated <b>{subjectName}</b> key'))


@login_required()
def answerSheetUpload(request):
    form = AnswerSheetForm()
    outData = AnswerKeys.objects.all()
    if request.method == 'POST':
        form = AnswerSheetForm(request.POST, request.FILES)
        if form.is_valid():
            # create new record or update existing based on availability of roll number
            create_Or_Update_AnswerSheet(request)
            return redirect('answer_sheet_upload')
    return render(request, 'upload_answersheet.html', {'form': form, 'outData': outData})

def getMarks(request, answerSheet, ansId):
    subjectName = request.POST['subject_name']
    checker = None
    answerKey = None
    try:
        checker = AnswerKeys.objects.get(subject_name=subjectName)
        answerKey = checker.answer_key
        totalMark, computedMark = calculateMark(answerSheet, answerKey)

        create_Or_Update_Grade(int(ansId), totalMark, computedMark)

        messages.success(request, f"{computedMark} mark out of {totalMark}")
    except:
        messages.success(request, "Failed Calculating Marks")
    return

def create_Or_Update_Grade(ansId, totalMark, computedMark):
    checker = None
    ansInstance = AnswerSheets.objects.get(id=ansId)
    try:
        checker = Grade.objects.get(answersheet_id=ansId)
    except:
        pass

    if checker is None:
        data = Grade()
        data.answersheet_id = ansId
        data.total_mark = totalMark
        data.computed_mark = computedMark
        data.grade = 'grade'
        data.subject_name = ansInstance.subject_name
        data.student_name = ansInstance.student_name
        data.save()
    else:
        checker.total_mark = totalMark
        checker.computed_mark = computedMark
        checker.grade = 'grade'
        checker.subject_name = ansInstance.subject_name
        checker.student_name = ansInstance.student_name
        checker.save()
    return

def create_Or_Update_AnswerSheet(request):
    # intialize a checker
    checker = None
    rollNumber = request.POST['roll_number']
    try:
        # check roll number is present in database
        checker = AnswerSheets.objects.get(roll_number=rollNumber)
    except:
        pass

    if checker is None:
        data = AnswerSheets()
        data.roll_number = rollNumber
        data.student_name = request.POST['student_name']
        data.subject_name = request.POST['subject_name']
        data.answer_sheet = request.FILES['answer_sheet']
        data.save()
        getMarks(request, data.answer_sheet.url, data.id)
        messages.success(request, mark_safe(
            f'Successfully uploaded answer sheet of <b>roll number:{rollNumber}</b>'))
    else:
        checker.student_name = request.POST['student_name']
        checker.subject_name = request.POST['subject_name']
        checker.answer_sheet = request.FILES['answer_sheet']
        checker.save()
        getMarks(request, checker.answer_sheet.url, checker.id)
        messages.success(request, mark_safe(
            f'Successfully updated  answer sheet of <b>roll number:{rollNumber}</b>'))
