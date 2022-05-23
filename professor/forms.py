from django import forms
from professor.models import Question
from django.utils.translation import ugettext_lazy as _


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ['updated_at']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['question_title'].widget.attrs['placeholder'] = _("Enter question title")
    #     self.fields['question_title'].widget.attrs['placeholder'] = _("Enter question title")
    #     # self.fields['Question_Name'].label = ""
    #     # self.fields['Question_Type'].widget = forms.HiddenInput()

