from django import forms
from professor.models import Question, QuestionSet
from django.utils.translation import ugettext_lazy as _


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ['updated_at', 'organization_code']

    # def __init__(self, *args, **kwargs):
    #     # self.request = kwargs.pop("request")
    #     super().__init__(*args, **kwargs)
        # self.fields['upload_file']= forms.FileField(
        #         label='Select a file',
        #         help_text='max. 2 MB'
        #     )
    #     self.fields['organization_code'].widget = forms.HiddenInput()
    #     self.fields['organization_code'].initial = self.request.user.professor.organization_code




class QuestionSetForm(forms.ModelForm):
    class Meta:
        model = QuestionSet
        exclude = ['updated_at']

