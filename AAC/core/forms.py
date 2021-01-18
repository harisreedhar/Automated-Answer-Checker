from django import forms
from core.models import AnswerKeys
from django.utils.safestring import mark_safe
from django.core.validators import FileExtensionValidator

class AnswerSheetForm(forms.Form):
    roll_number = forms.IntegerField(
    label='Roll Number',
    )

    student_name = forms.CharField(
    label='Student Name',
    )

    answer_sheet = forms.FileField(
    label='Answer Sheet',
    validators=[ FileExtensionValidator(['pdf'])]
    )
class AnswerKeyForm(forms.Form):
    subject_name = forms.CharField(
    label='Subject',
    )

    answer_key = forms.CharField(
        widget=forms.Textarea,
        label='Answer Key',
    )

    marks = forms.CharField(
    label='Marks',
    )

    # using clean_ prefix to custom validate fields

    def clean_marks(self):
        mrks = self.data.get('marks')
        checker = False
        try:
            mrks = [int(s) for s in mrks.split(',')]
            checker = True
        except:
            checker = False
        if not checker:
            raise forms.ValidationError('Marks should be comma separated integer values')
        return

    def clean_answer_key(self):
        anskey = self.data.get('answer_key')
        checker = False
        try:
            exec(anskey)
            checker = True
        except:
            checker = False
        if not checker:
            raise forms.ValidationError(mark_safe("Answer key should be in the form: <br/> Q1 = 'hint 1', 'hint 2', ... 'hint n'<br/>Q2 = 'hint 1', 'hint 2', ... 'hint n'<br/>"))
        return

########################## Check HTR ###############################

class CheckHtrForm(forms.Form):
    answersheet_path = forms.CharField(label='Answersheet Path',)
