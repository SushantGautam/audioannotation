from django.db import models
from orgadmin.models import BaseUserModel
from professor.models import Question

class Speaker(BaseUserModel):
    class Meta:
        verbose_name = 'Speaker'
        verbose_name_plural = 'Speakers'


def audio_filename(instance, filename):
    return 'speaker/audio/{0}/{1}'.format(instance.speaker, str(instance.id) + filename)


class AudioFile(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    audio_file = models.FileField(upload_to=audio_filename)
    speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.audio_file.name


class SpeakerSubmission(models.Model):
    STATUS_CHOICES = (
        ('IS', 'Initial State'),
        ('SS', 'STT Submitted'),
        ('SP', 'STT Processing'),
        ('SC', 'STT Completed'),
        ('SF', 'STT Failed'),
    )

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to=audio_filename)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    stt_data = models.JSONField(null=True, blank=True, default=dict)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='IN')

    def __str__(self):
        return self.question.title



