from django.db.models.signals import post_save
from django.dispatch import receiver

from professor.models import ExamSet
from speaker.models import ExamSetSubmission
from speaker.models import SpeakerSubmission

def checkIfExamSetComplete(speaker, exam_set):
    exam_set = ExamSet.objects.get(pk=exam_set.pk)
    examQuesCount = exam_set.get_question_count()
    speakerCount = SpeakerSubmission.objects.filter(exam_set_id=exam_set.id, speaker=speaker).count()
    return examQuesCount == speakerCount

@receiver(post_save, sender=SpeakerSubmission)
def examSetSubmissionCreate(sender, instance, created, **kwargs):
    # when worker task is created, change the related examsetsubmission's status to next.
    if created and checkIfExamSetComplete(instance.speaker, instance.exam_set):
        ExamSetSubmission.objects.create(
            speaker=instance.speaker,
            exam_set=instance.exam_set
        )


