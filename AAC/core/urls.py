# -*- coding: utf-8 -*-
from django.urls import path
from . views import home, delete, teachers, answerSheetUpload, answerKeyUpload

urlpatterns = [
    path('', home, name='home'),
    path('delete/<int:student_id>', delete, name='delete'),
    path('answer_sheet_upload', answerSheetUpload, name='answer_sheet_upload'),
    path('answer_key_upload', answerKeyUpload, name='answer_key_upload'),
    path('teachers', teachers, name='teachers'),
]

