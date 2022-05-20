from django.db import models
from django.utils.translation import gettext_lazy as _

from orgadmin.models import BaseUserModel
from professor.models import Question
from speaker.choices import GENDER_CHOICES, COUNTRY_CHOICES, LANGUAGE_CHOICES, PROFICIENCY_CHOICES


class Speaker(BaseUserModel):
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='F')
    nationality = models.CharField(max_length=2, choices=COUNTRY_CHOICES, default='KR')
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='KO')
    proficiency = models.CharField(max_length=1, choices=PROFICIENCY_CHOICES, default='B')
    topic_score = models.IntegerField(default=0)
    education_level = models.CharField(max_length=256, null=True, blank=True)
    learning_period = models.IntegerField(default=0)
    korea_residency = models.IntegerField(default=0)
    study_purpose = models.CharField(max_length=256, null=True, blank=True)
    learning_method = models.CharField(max_length=256, null=True, blank=True)
    class Meta:
        verbose_name = _('Speaker')
        verbose_name_plural = _('Speakers')


def audio_filename(instance, filename):
    return 'speaker/audio/{0}/{1}'.format(instance.speaker, str(instance.id) + filename)


class SpeakerSubmission(models.Model):
    STATUS_CHOICES = (
        ('IS', _('Initial State')),
        ('SS', _('STT Submitted')),
        ('SP', _('STT Processing')),
        ('SC', _('STT Completed')),
        ('SF', _('STT Failed')),
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



