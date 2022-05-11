import os

from django.db import models
from orgadmin.models import BaseUserModel


class Speaker(BaseUserModel):
    class Meta:
        verbose_name = 'Speaker'
        verbose_name_plural = 'Speakers'


def update_filename(instance, filename):
    path = "upload/path/"
    format = str(instance.pk) + "_new_audio.wav"
    return os.path.join(path, format)


class AudioFile(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    audio_file = models.FileField(upload_to=update_filename)

    class Meta:
        verbose_name = 'AudioFile'
        verbose_name_plural = 'AudioFiles'


