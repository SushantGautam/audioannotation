from django import forms
from . import models


class QuestionForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = []



class SubmissionsForm(forms.ModelForm):
    class Meta:
        model = models.Submissions
        fields = []



class ProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = []

