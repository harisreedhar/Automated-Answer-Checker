from django import forms
from core.models import AnswerKeys

class AnswerSheetForm(forms.Form):
    roll_number = forms.IntegerField(
    label='Roll Number',
    )

    student_name = forms.CharField(
    label='Student Name',
    )

    # subject_name = forms.ChoiceField(
    #     #queryset = AnswerKeys.objects.all(),
    #     choices = [(obj.subject_name, obj.subject_name) for i, obj in enumerate(AnswerKeys.objects.all())],
    #     label = 'Subject'
    # )

    answer_sheet = forms.FileField(
    label='Answer Sheet',
    help_text='file should be in pdf format',
    )

class AnswerKeyForm(forms.Form):
    subject_name = forms.CharField(
    label='Subject',
    )

    answer_1 = forms.CharField(
        widget=forms.Textarea,
        label='Qn1 Answer',
    )
    mark_1 = forms.IntegerField(
        label='Qn1 Mark',
    )
    answer_2 = forms.CharField(
        widget=forms.Textarea,
        label='Qn2 Answer',
    )
    mark_2 = forms.IntegerField(
        label='Qn2 Mark',
    )
    answer_3 = forms.CharField(
        widget=forms.Textarea,
        label='Qn3 Answer',
    )
    mark_3 = forms.IntegerField(
        label='Qn3 Mark',
    )


