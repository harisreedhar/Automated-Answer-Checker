# -*- coding: utf-8 -*-
from django.urls import path
from . views import home, answerSheetUpload, answerKeyUpload, checkHTR, generateMarkList

urlpatterns = [
    path('', home, name='home'),
    path('answer_sheet_upload', answerSheetUpload, name='answer_sheet_upload'),
    path('answer_key_upload', answerKeyUpload, name='answer_key_upload'),
    path('check_htr', checkHTR, name='check_htr'),
    path('marklist_generate', generateMarkList, name='marklist_generate'),
]
