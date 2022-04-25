from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.template.defaultfilters import truncatechars
from django.urls import reverse


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

    def __str__(self):
        return str(self.username)

    def get_absolute_url(self):
        return reverse("User_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("User_update", args=(self.pk,))


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
    question_text = models.TextField(max_length=4000, blank=False, null=False)
    created_by = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="question_created_by")
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    extras = models.JSONField(blank=True, null=True, default=dict)

    class Meta:
        pass

    @property
    def short_question_text(self):
        return str(truncatechars(self.question_text, 50))

    def __str__(self):
        return self.short_question_text

    def get_absolute_url(self):
        return reverse("Question_detail", args=(self.pk,))

    def get_update_url(self):
        return reverse("Question_update", args=(self.pk,))


class Submissions(models.Model):
    # Fields
    TTL_STATUS_CHOICES = (
        (0, 'Idle'),
        (1, 'Submitted To STT Queue'),
        (2, 'Processing by STT Queue'),
        (3, 'Calling STT API'),
        (4, 'STT Output Received & Processing'),
        (5, 'STT TaskCompleted | AnnotationSaved '),
    )

    id = models.AutoField(primary_key=True, auto_created=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    submitted_by = models.ForeignKey(Member, on_delete=models.CASCADE)
    sound_file = models.FileField(upload_to='media/question_audio/', blank=True, null=True,
                                  help_text="Upload audio file now or you will get to record your voice after you save.")
    comment = models.TextField(max_length=4000, blank=True, null=True, help_text="Optional! Write your comment here", )
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    tts_status = models.SmallIntegerField(choices=TTL_STATUS_CHOICES, default=0, help_text="For Future Purpose.")
    extras = models.JSONField(blank=True, null=True, default=dict)

    def set_tts_status(self, status):
        self.tts_status = status  # STT TaskCompleted | AnnotationSaved
        self.no_post_save = True
        self.save()

    @property
    def short_comment(self):
        return str(truncatechars(self.comment, 40))

    @property
    def getSplittedAudio(self):
        pathToSave = 'media/audio-splits/' + str(self.id) + "/"
        if self.extras.get("audio_segments"):
            return sorted(self.extras.get("audio_segments"))
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


@receiver(pre_save, sender=Submissions)
def addrequest(sender, instance, **kwargs):
    if instance.sound_file:
        instance.pv_sound_file = instance.sound_file.url
    else:
        instance.pv_sound_file = None


from .utils.audio import segmentaudio


@receiver(post_save, sender=Submissions)
def addrequest(sender, instance, **kwargs):
    if hasattr(instance, 'no_post_save'):
        return
    try:
        pv = Submissions.objects.get(id=instance.id)
    except:
        if instance.sound_file:  # first time is sound is added
            instance.extras['annotations'] = []
            instance.no_post_save = True
            instance.status = 0
            instance.save()
            segmentaudio.delay(sID=instance.id)
            print(" new file and audio file changed")
        return  # exit and ignore for the first time

    if instance.sound_file:
        if instance.sound_file.url != instance.pv_sound_file:  # on sound update
            instance.extras['annotations'] = []
            instance.no_post_save = True
            instance.save()
            segmentaudio.delay(sID=instance.id)
            print("audio file changed")
