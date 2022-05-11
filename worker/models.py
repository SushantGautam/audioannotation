from django.db import models

from orgadmin.models import BaseUserModel

class Worker(BaseUserModel):
    class Meta:
        verbose_name = 'Worker'
        verbose_name_plural = 'Workers'

class WorkerSubmission(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    speaker_submission = models.ForeignKey('speaker.SpeakerSubmission', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    split_data = models.JSONField(null=True, blank=True, default=dict)
