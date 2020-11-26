# -*- coding: utf-8 -*-
from django.urls import path, include
from . views import register_view, logout

urlpatterns = [
    path('register/', register_view, name='register'),
    path('logout/', logout, name='logout')
]

