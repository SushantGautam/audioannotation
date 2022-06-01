from django.forms import ModelForm
from django import forms

from speaker.models import ExamSetSubmission
from worker.models import WorkerTask


class ExamSetSubmissionFilterForm(ModelForm):
    class Meta:
        model = ExamSetSubmission
        fields = []

    def __init__(self, *args, **kwargs):
        super(ExamSetSubmissionFilterForm, self).__init__(*args, **kwargs)

        # Refer to professor/models.py
        DIFFICULTY_CHOICES = (
            ("1", "Beginner"),
            ("2", "Advanced"),
        )
        MAPPED_TASK_TYPE_Choices = (
            ('STC', 'Slicing Level 1'),
            ('SC1', 'Slicing Level 2'),
            ('SC2', 'Tagging Level 1'),
            ('TC1', 'Tagging Level 2'),
            ('TC2', 'Evaluation Level 1'),
            ('EC1', 'Evaluation Level 2'),
        )
        self.fields['difficulty_level'] = forms.MultipleChoiceField(choices=DIFFICULTY_CHOICES,
                                                                    widget=forms.CheckboxSelectMultiple(),
                                                                    required=False)

        self.fields['work_type'] = forms.MultipleChoiceField(choices=MAPPED_TASK_TYPE_Choices,
                                                             widget=forms.CheckboxSelectMultiple(), required=False)
        self.fields['tags'] = forms.CharField(
            widget=forms.Textarea(attrs={'placeholder': 'Seperate tags by comma( , )', 'rows': '3', 'cols': '15'}),
            required=False)
