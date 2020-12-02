from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    teacher_id = models.ForeignKey(User, on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=256)

    def __str__(self):
        return self.subject_name
    class Meta:
        verbose_name_plural = "Subject"

class AnswerKeys(models.Model):
    subject_name = models.CharField(max_length=256, unique = True)
    answer_key = models.JSONField()

    def __str__(self):
        return self.subject_name
    class Meta:
        verbose_name_plural = "Answer Key"

class AnswerSheets(models.Model):
    roll_number = models.IntegerField(unique = True)
    student_name = models.CharField(max_length=256)
    subject_name = models.CharField(max_length=256)
    answer_sheet = models.FileField(upload_to='documents/%Y/%m/%d')

    def __str__(self):
        return self.student_name
    class Meta:
        verbose_name_plural = "Answer Sheet"

class Grade(models.Model):
    answersheet_id = models.IntegerField(unique = True)
    total_mark = models.IntegerField()
    computed_mark = models.IntegerField()
    grade = models.CharField(max_length=32)
    student_name = models.CharField(max_length=256)
    subject_name = models.CharField(max_length=256)

    def __str__(self):
        return self.subject_name
    class Meta:
        verbose_name_plural = "Grade"
