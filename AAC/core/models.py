from django.db import models

class AnswerTable(models.Model):
    student_name = models.CharField(max_length=256)
    answer = models.FileField(upload_to='documents/%Y/%m/%d')
    answer_key = models.FileField(upload_to='documents/%Y/%m/%d')
    marks = models.FloatField()
