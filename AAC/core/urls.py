# -*- coding: utf-8 -*-
from django.urls import path
from . views import home, delete

urlpatterns = [
    path('', home, name='home'),
    path('delete/<int:student_id>', delete, name='delete'),
]

