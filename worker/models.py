from telnetlib import STATUS
from django.db import models

from orgadmin.models import BaseUserModel, Contract, ContractSign


class Worker(BaseUserModel):
    bank_name = models.CharField(max_length=256, null=True, blank=True)
    bank_account_number = models.CharField(max_length=256, null=True, blank=True)
    education_level = models.CharField(max_length=256, null=True, blank=True)
    education_field = models.CharField(max_length=256, null=True, blank=True)
    class Meta:
        verbose_name = 'Worker'
        verbose_name_plural = 'Workers'

    def has_contract(self):
        return Contract.objects.filter(user_type='WOR', is_active=True,
                                       created_by__organization_code=self.organization_code).exists()

    def has_submitted_contract(self):
        return ContractSign.objects.filter(user=self, contract_code__user_type='WOR', approved=None,
                                           contract_code__created_by__organization_code=self.organization_code).exists()

    def has_contract_approved(self):
        return ContractSign.objects.filter(user=self, contract_code__user_type='WOR', approved=True,
                                           contract_code__created_by__organization_code=self.organization_code).exists()


class EvaluationTitle(models.Model):
    EVALUATION_TYPE_CHOICES = (
        ('P', 'Proficiency'),
        ('F', 'Fluency'),
        ('C', 'Content'),
        ('D', 'Delivery'),
        ('A', 'Accuracy'),
    )
    title = models.CharField(max_length=256)
    score = models.IntegerField(default=0)
    evaluation_type = models.CharField(max_length=1, choices=EVALUATION_TYPE_CHOICES)
    subcategory_code = models.ForeignKey('professor.SubCategory', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class WorkerTask(models.Model):
    TASK_TYPE_CHOICES = (
        ('S1', 'Slicing Level 1'),
        ('S2', 'Slicing Level 2'),
        ('T1', 'Tagging Level 1'),
        ('T2', 'Tagging Level 2'),
        ('E1', 'Evaluation Level 1'),
        ('E2', 'Evaluation Level 2'),
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
            return "Not Approved"
        return "Approved" if self.approved else "Rejected"


class WorkerSubmission(models.Model):
    speaker_submission = models.ForeignKey('speaker.SpeakerSubmission', on_delete=models.CASCADE)
    worker_task = models.ForeignKey(WorkerTask, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    work_data = models.JSONField(null=True, blank=True, default=dict)
    evaluation_data = models.ManyToManyField(EvaluationTitle, blank=True)
    status = models.BooleanField(default=False) # True = completed, False = not completed