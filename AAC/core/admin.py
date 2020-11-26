from django.contrib import admin
from . models import AnswerKeys, AnswerSheets, Grade

# Register your models here.

admin.site.register(AnswerKeys)
admin.site.register(AnswerSheets)
admin.site.register(Grade)
