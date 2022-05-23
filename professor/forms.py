from django import forms
from professor.models import Question
from django.utils.translation import ugettext_lazy as _


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ['updated_at', 'organization_code']

    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop("request")
    #     super().__init__(*args, **kwargs)
    #     self.fields['organization_code'].widget = forms.HiddenInput()
    #     self.fields['organization_code'].initial = self.request.user.professor.organization_code






