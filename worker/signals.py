from django.db.models.signals import post_save
from django.dispatch import receiver

from speaker.models import ExamSetSubmission
from worker.models import WorkerTask

@receiver(post_save, sender=WorkerTask)
def examSetSubmissionStatusChange(sender, instance, created, **kwargs):
    # when worker task is created, change the related examsetsubmission's status to next.
    if created:
        examSet = instance.examset_submission
        examSet.status = instance.examset_submission.next_status()[0]
        examSet.save()


