from distutils.command.upload import upload
import os
from django.db import models
from orgadmin.models import BaseUserModel

class Speaker(BaseUserModel):
    class Meta:
        verbose_name = 'Speaker'
        verbose_name_plural = 'Speakers'


def audio_filename(instance, filename):
    return 'speaker/audio/{0}/{1}'.format(instance.speaker, str(instance.id) + filename)

class AudioFile(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    audio_file = models.FileField(upload_to=audio_filename)
    speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE)

    def __str__(self):
        return self.audio_file.name


