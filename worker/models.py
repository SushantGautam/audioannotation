from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from orgadmin.models import BaseUserModel, Contract, ContractSign, VerificationRequest


class Worker(BaseUserModel):
    bank_name = models.CharField(max_length=256, null=True, blank=True)
    bank_account_number = models.CharField(max_length=256, null=True, blank=True)
    education_level = models.CharField(max_length=256, null=True, blank=True)
    education_field = models.CharField(max_length=256, null=True, blank=True)
    class Meta:
        verbose_name = _('Worker')
        verbose_name_plural = _('Workers')

    def has_request_verification(self):
        return VerificationRequest.objects.filter(user=self.user).exists()

    def has_contract(self):
        return Contract.objects.filter(user_type='WOR', created_by__organization_code=self.organization_code).exists()

    def has_contract_submitted(self):
        return ContractSign.objects.filter(user=self.user, approved=None).exists()

    def has_contract_approved(self):
        return ContractSign.objects.filter(user=self.user, approved=True).exists()

    def get_verification_status(self):
        if VerificationRequest.objects.filter(user=self.user).exists():
            latest = self.user.verificationrequest_set.latest('id')
            print(latest)
            if latest.approved == None:
                return "Pending"
            elif latest.approved:
                return "Approved"
            else:
                return "Rejected"
        return "Not Submitted"

class EvaluationTitle(models.Model):
    EVALUATION_TYPE_CHOICES = (
        ('AC', _('Accentedness')),
        ('FL', _('Fluency')),
        ('CN', _('Content')),
        ('DE', _('Delivery')),
        ('CO', _('Comprehensibility')),
        ('LU', _('Language Use')),
    )
    title = models.CharField(max_length=256)
    score = models.IntegerField(default=0)
    evaluation_code = models.CharField(max_length=128)
    evaluation_type = models.CharField(max_length=2, choices=EVALUATION_TYPE_CHOICES)
    subcategory_code = models.ForeignKey('professor.SubCategory', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class WorkerTask(models.Model):
    TASK_TYPE_CHOICES = (
        ('S1', _('Slicing Level 1')),
        ('S2', _('Slicing Level 2')),
        ('T1', _('Tagging Level 1')),
        ('T2', _('Tagging Level 2')),
        ('E1', _('Evaluation Level 1')),
        ('E2', _('Evaluation Level 2')),
    )
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    examset_submission = models.ForeignKey('speaker.ExamSetSubmission', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(null=True) # null = not yet approved
    approved_at = models.DateTimeField(null=True)
    task_type = models.CharField(max_length=2, choices=TASK_TYPE_CHOICES, default='S1')
    status = models.BooleanField(default=False) # True = completed, False = not completed

    def __str__(self):
        return '{} - {}'.format(self.examset_submission, self.task_type)

    def get_approved_display(self):
        if not self.approved:
            return "Pending"
        return "Approved" if self.approved else "Rejected"

    def get_task_url(self):
        if self.task_type in ['S1', 'S2']:
            return reverse('worker:annotation_page', args=(self.pk, ))
        elif self.task_type in ['E1', 'E2']:
            return reverse('worker:evaluation_page', args=(self.pk, ))


class WorkerSubmission(models.Model):
    speaker_submission = models.ForeignKey('speaker.SpeakerSubmission', on_delete=models.CASCADE)
    worker_task = models.ForeignKey(WorkerTask, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    work_data = models.JSONField(null=True, blank=True, default=dict)
    evaluation_data = models.ManyToManyField(EvaluationTitle, blank=True)
    status = models.BooleanField(default=False) # True = completed, False = not completed
