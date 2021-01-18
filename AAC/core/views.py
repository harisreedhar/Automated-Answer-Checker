from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from core.models import AnswerSheets, AnswerKeys, Grade
from core.forms import AnswerSheetForm, AnswerKeyForm, CheckHtrForm
from django.contrib.auth.decorators import login_required
from core.calculate_mark import calculateMark, computeGrade


@login_required()
def home(request):
    form = AnswerKeyForm()
    datas = Grade.objects.all().order_by('roll_number')
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
                    exec(f"dictionary[f'Q{i+1}'] = [Q{i+1}, m]")
                    pass
                # create new record or update existing based on availability of subject name
                create_Or_Update_AnswerKey(request, subjectName, dictionary)
            except:
                string = ""
                string += "* Questions and Marks have different length <br/>"
                string += "* Answerkey is not written in correct format"
                errorMessage = mark_safe(string)
                messages.error(request, errorMessage)

            return redirect('answer_key_upload')

    return render(request, 'upload_answerkey.html', {'form': form})


def create_Or_Update_AnswerKey(request, subjectName, key):
    # intialize a checker
    checker = None
    try:
        # check subject name is present in database
        checker = AnswerKeys.objects.get(subject_name=subjectName)
    except:
        checker = None

    if checker is None:
        data = AnswerKeys()
        data.answer_key = key
        data.subject_name = subjectName
        data.save()
        messages.success(request, mark_safe(
            f'Successfully added answerkey of <b>{subjectName}</b>'))
    else:
        checker.answer_key = key
        checker.save()
        messages.success(request, mark_safe(
            f'Successfully updated answerkey of <b>{subjectName}</b>'))


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
        printMarks = mark_safe(f"<h3><b>Grade: {computeGrade(computedMark/totalMark)}</b></h3><h5> <b>{computedMark}</b> marks out of {totalMark}</h5>")
        messages.info(request, printMarks)
    except:
        messages.error(request, "Failed Calculating Marks")
        return False
    return True

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
        data.grade = computeGrade(computedMark/totalMark)
        data.subject_name = ansInstance.subject_name
        data.student_name = ansInstance.student_name
        data.roll_number = ansInstance.roll_number
        data.save()
    else:
        checker.total_mark = totalMark
        checker.computed_mark = computedMark
        checker.grade = computeGrade(computedMark/totalMark)
        checker.subject_name = ansInstance.subject_name
        checker.student_name = ansInstance.student_name
        checker.roll_number = ansInstance.roll_number
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
        marksCalculated = getMarks(request, data.answer_sheet.url, data.id)
        if marksCalculated:
            messages.success(request, mark_safe(
                f'Successfully uploaded answer sheet of <b>roll number:{rollNumber}</b>'))
    else:
        checker.student_name = request.POST['student_name']
        checker.subject_name = request.POST['subject_name']
        checker.answer_sheet = request.FILES['answer_sheet']
        checker.save()
        marksCalculated = getMarks(request, checker.answer_sheet.url, checker.id)
        if marksCalculated:
            messages.success(request, mark_safe(
                f'Mark of <b>roll number:{rollNumber}</b> has been updated'))
    return

########################## Check HTR ###############################

from core.HandWriting_Recognition.src.utils import pdf_to_image
from core.HandWriting_Recognition.src.imageToText import photoToText
def pdfToText(path):
    images = pdf_to_image(path)
    answer = ""
    accuracyList = []
    wordList = []
    for img in images:
        temp1, temp2 = photoToText(img)
        wordList.append(temp1)
        accuracyList.extend(temp2)
    return wordList, accuracyList

def checkHTR(request):
    form = CheckHtrForm()
    if request.method == 'POST':
        form = CheckHtrForm(request.POST, request.FILES)
        if form.is_valid():
            pdffile = request.POST['answersheet_path']
            words, aa = pdfToText(pdffile)
            messages.success(request, mark_safe(str(words)))
            return redirect('check_htr')
    return render(request, 'check_htr.html', {'form': form})
