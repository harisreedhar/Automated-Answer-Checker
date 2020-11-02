from django import forms
from core.models import AnswerTable

class AnswerForm(forms.Form):
    student_name = forms.CharField(
    label='Student Name',
    )

    subject_name = forms.CharField(
    label='Subject',
    )

    answer = forms.FileField(
    label='Answer Sheet',
    help_text='pdf, jpeg, png are supported',
    )

    answer_key = forms.FileField(
    label='Answer Key',
    help_text='pdf, jpeg, png are supported'
    )
