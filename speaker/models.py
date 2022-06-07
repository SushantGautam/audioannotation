import os
from django.db import models
from django.utils.translation import gettext_lazy as _

from orgadmin.models import BaseUserModel, Contract, ContractSign, VerificationRequest
from professor.models import Question, ExamSet
from speaker.choices import GENDER_CHOICES, COUNTRY_CHOICES, LANGUAGE_CHOICES, PROFICIENCY_CHOICES


class Speaker(BaseUserModel):
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='F')
    nationality = models.CharField(max_length=2, choices=COUNTRY_CHOICES, default='KR')
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='ko')
    proficiency = models.CharField(max_length=1, choices=PROFICIENCY_CHOICES, default='B')
    topic_score = models.IntegerField(default=0)
    education_level = models.CharField(max_length=256, null=True, blank=True)
    learning_period = models.IntegerField(default=0)
    korea_residency = models.IntegerField(default=0)
    study_purpose = models.CharField(max_length=256, null=True, blank=True)
    learning_method = models.CharField(max_length=256, null=True, blank=True)
    bank_name = models.CharField(max_length=256, null=True, blank=True)
    bank_account_number = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        verbose_name = _('Speaker')
        verbose_name_plural = _('Speakers')

    def __str__(self):
        return self.user.username
    
    def has_request_verification(self):
        return VerificationRequest.objects.filter(user=self.user).exists()
    
    def has_profile_rejected(self):
        return VerificationRequest.objects.filter(user=self.user, approved=False).exists()

    def has_contract(self):
        return Contract.objects.filter(user_type='SPE', created_by__organization_code=self.organization_code).exists()
    
    def has_contract_submitted(self): #submitted and pending approval
        return ContractSign.objects.filter(user=self.user, approved=None).exists()
    
    def has_contract_rejected(self): #submitted and rejected
        return ContractSign.objects.filter(user=self.user, approved=False).exists()
    
    def has_contract_approved(self): #submitted and approved
        return ContractSign.objects.filter(user=self.user, approved=True).exists()


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
    exam_set = models.ForeignKey(ExamSet, on_delete=models.CASCADE)

    audio_file = models.FileField(upload_to=audio_filename)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    stt_data = models.JSONField(null=True, blank=True, default=dict)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='IS')

    def __str__(self):
        return self.question.question_title

    def filename(self):
        return os.path.basename(self.audio_file.name)

class ExamSetSubmission(models.Model):
    STATUS_CHOICES = (
        ('INS', _('Initial State')),
        ('STC', _('STT Completed')),
        ('SA1', _('Slicing Assigned level 1')),
        ('SC1', _('Slicing Completed level 1')),
        ('SA2', _('Slicing Assigned level 2')),
        ('SC2', _('Slicing Completed level 2')),
        ('TA1', _('Tagging Assigned level 1')),
        ('TC1', _('Tagging Completed level 1')),
        ('TA2', _('Tagging Assigned level 2')),
        ('TC2', _('Tagging Completed level 2')),
        ('EA1', _('Evaluation Assigned level 1')),
        ('EC1', _('Evaluation Completed level 1')),
        ('EA2', _('Evaluation Assigned level 2')),
        ('EC2', _('Evaluation Completed level 2')),
        ('STF', _('STT Failed')),
    )
    speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE)
    exam_set = models.ForeignKey(ExamSet, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='INS')

    def __str__(self):
        return self.exam_set.exam_name

    def complete(self):
        return self.status == 'EC2'

    def next_status(self):
        current = list(filter(lambda x: self.status in x, self.STATUS_CHOICES))[0]
        if self.STATUS_CHOICES.index(current) != self.STATUS_CHOICES.__len__() - 1:
            return self.STATUS_CHOICES[self.STATUS_CHOICES.index(current)+1]
        return None

    def prev_status(self):
        current = list(filter(lambda x: self.status in x, self.STATUS_CHOICES))[0]
        if self.STATUS_CHOICES.index(current) != 0:
            return self.STATUS_CHOICES[self.STATUS_CHOICES.index(current)-1]
        return None

