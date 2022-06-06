from django.forms import ModelForm, DateTimeField, DateTimeInput

from speaker.models import SpeakerSubmission, Speaker


class SpeakerSubmissionForm(ModelForm):
    class Meta:
        model = SpeakerSubmission
        fields = ["question", "speaker", "audio_file"]


class ProfileEditForm(ModelForm):
    birth_date = DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1',
            'type': 'date'
        })
    )

    class Meta:
        model = Speaker
        exclude = ('organization_code', 'user', 'verified')
