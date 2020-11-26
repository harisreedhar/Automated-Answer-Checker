from django.db import models
from django.contrib.auth.models import User

# class AnswerTable(models.Model):
#     student_name = models.CharField(max_length=256)
#     subject_name = models.CharField(max_length=256)
#     answer = models.FileField(upload_to='documents/%Y/%m/%d')
#     answer_key = models.FileField(upload_to='documents/%Y/%m/%d')
#     marks = models.FloatField()

class Subject(models.Model):
    teacher_id = models.ForeignKey(User, on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

# class Student(models.Model):
#     roll_number = models.IntegerField()
#     student_name = models.CharField(max_length=256)
#     class_name = models.CharField(max_length=256)

class AnswerKeys(models.Model):
    subject_name = models.CharField(max_length=256)
    answer_key = models.JSONField()

    def __str__(self):
        return self.subject_name
    class Meta:
        verbose_name_plural = "Answer Key"

class AnswerSheets(models.Model):
    roll_number = models.IntegerField()
    student_name = models.CharField(max_length=256)
    subject_name = models.CharField(max_length=256)
    answer_sheet = models.FileField(upload_to='documents/%Y/%m/%d')

    def __str__(self):
        return self.student_name
    class Meta:
        verbose_name_plural = "Answer Sheet"

class Grade(models.Model):
    answersheet_id = models.ForeignKey(AnswerSheets, on_delete=models.CASCADE)
    grade = models.CharField(max_length=32)

    def __str__(self):
        return self.name
