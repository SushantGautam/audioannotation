from telnetlib import STATUS
from django.db import models

from orgadmin.models import BaseUserModel

class Worker(BaseUserModel):
    bank_name = models.CharField(max_length=256, null=True, blank=True)
    bank_account_number = models.CharField(max_length=256, null=True, blank=True)
    education_level = models.CharField(max_length=256, null=True, blank=True)
    education_field = models.CharField(max_length=256, null=True, blank=True)
    class Meta:
        verbose_name = 'Worker'
        verbose_name_plural = 'Workers'

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
        ('S', 'Slicing'),
        ('T', 'Tagging'),
        ('E', 'Evaluation'),
    )
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    examset_submission = models.ForeignKey('speaker.ExamSetSubmission', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(null=True) # null = not yet approved
    approved_at = models.DateTimeField(null=True)
    task_type = models.CharField(max_length=1, choices=TASK_TYPE_CHOICES, default='S')
    status = models.BooleanField(default=False) # True = completed, False = not completed

    def __str__(self):
        return '{} - {} - {}'.format(self.speaker_submission, self.task_type)

class WorkerSubmission(models.Model):
    speaker_submission = models.ForeignKey('speaker.SpeakerSubmission', on_delete=models.CASCADE)
    worker_task = models.ForeignKey(WorkerTask, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    split_data = models.JSONField(null=True, blank=True, default=dict)
    tagging_data = models.JSONField(null=True, blank=True, default=dict)
    evaluation_data = models.ManyToManyField(EvaluationTitle, blank=True)
    status = models.BooleanField(default=False) # True = completed, False = not completed