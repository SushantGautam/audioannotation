from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from WebApp.utils.audio import segmentaudio


class Member(AbstractUser):
    TTL_GENDER = (
        (0, 'Unknown'),  # needs verification after member submits
        (1, 'Female'),  # when admin verifies
        (1, 'Male'),  # when admin verifies
    )
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    extras = models.JSONField(blank=True, null=True, default=dict)
    DOB = models.DateField(null=True, blank=True)
    position = models.CharField(max_length=100, null=True, blank=True)
    gender = models.SmallIntegerField(choices=TTL_GENDER, default=0)
    study_purpose = models.CharField(max_length=100, null=True, blank=True)
    study_period = models.DurationField(null=True, blank=True)


class Project(models.Model):
    # Fields
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="project_created_by")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    extras = models.JSONField(blank=True, null=True, default=dict)

    class Meta:
        pass

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("Project_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("Project_update", args=(self.pk,))


class Question(models.Model):
    # Fields
    id = models.AutoField(primary_key=True, auto_created=True)
    question_text = models.CharField(max_length=200, blank=False, null=False)
    created_by = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="question_created_by")
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    extras = models.JSONField(blank=True, null=True, default=dict)

    class Meta:
        pass

    def __str__(self):
        return str(self.question_text)

    def get_absolute_url(self):
        return reverse("Question_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("Question_update", args=(self.pk,))


class Submissions(models.Model):
    # Fields
    TTL_STATUS_CHOICES = (
        (0, 'Submitted'),  # needs verification after member submits
        (1, 'AdminVerifiedRequest'),  # when admin verifies
        (2, 'AdminRejectedRequest'),  # admin rejects; may be member can resubmit after correction later
        (3, 'PaymentMade'),  # After admin verifies; member pays money
        (4, 'Hold'),  # after member pays money, talent can accept/reject
        (5, 'TalentRejected'),  # if talent is unable to serve
        (6, 'TalentCompleted'),  # automatically marked completed when talent does a submission
        (7, 'AdminVerifySubmission'),
        (8, 'AdminRejectSubmission'),
    )

    id = models.AutoField(primary_key=True, auto_created=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    submitted_by = models.ForeignKey(Member, on_delete=models.CASCADE)
    sound_file = models.FileField(upload_to='media/question_audio/')
    comment = models.CharField(max_length=200, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    tts_status = models.SmallIntegerField(choices=TTL_STATUS_CHOICES, default=0)
    extras = models.JSONField(blank=True, null=True, default=dict)

    @property
    def getSplittedAudio(self):
        pathToSave = 'media/audio-splits/' + str(self.id) + "/"
        if self.extras.get("audio_segments"):
            return self.extras.get("audio_segments")
        else:
            print('No sudio splits found')
            return []

    class Meta:
        pass

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("Submissions_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("Submissions_update", args=(self.pk,))


@receiver(post_save, sender=Submissions)
def addrequest(sender, instance, **kwargs):
    try:
        pv = Submissions.objects.get(id=instance.id)
    except:
        if instance.sound_file:  # first time is sound is added
            segmentaudio(sID=instance.id, audiofile=instance.sound_file)
            print(" new file and audio file changed")
        return  # exit and ignore for the first time

    if instance.sound_file != pv.sound_file:  # on sound update
        segmentaudio(sID=instance.id, audiofile=instance.sound_file)
        print("audio file changed")
