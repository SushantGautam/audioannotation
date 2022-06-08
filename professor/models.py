from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
import os
from orgadmin.models import BaseUserModel, Organization

class Professor(BaseUserModel):
    class Meta:
        verbose_name = _('Professor')
        verbose_name_plural = _('Professors')


class Category(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    category_code = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


def question_file_name(instance, filename):
    return 'question/{0}/{1}/{2}'.format(instance.subcategory_code, instance.id, filename)


class Question(models.Model):
    UPLOAD_TYPE_CHOICES = (
        ('NON', _('None')),
        ('IMG', _('Image Question')),
        ('AUD', _('Audio Question')),
    )
    question_title = models.TextField()
    unique_code = models.CharField(max_length=10, unique=True)
    description = models.TextField(null=True, blank=True)
    upload_file = models.FileField(upload_to=question_file_name, null=True, blank=True)
    upload_type = models.CharField(max_length=3, choices=UPLOAD_TYPE_CHOICES, default='NON')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    difficulty_level = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(2)], 
                                            help_text=_('0: both, 1: beginner, 2: advanced'))
    ready_time = models.IntegerField(default=2, help_text=_('Time in seconds'))
    speaking_time = models.IntegerField(default=3, help_text=_('Time in seconds'))
    evaluation_purpose = models.CharField(max_length=256, null=True, blank=True)
    question_keywords = models.CharField(max_length=256, null=True, blank=True,
                                         help_text=_('Comma separated keywords'))
    subcategory_code = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    organization_code = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.unique_code


    def filename(self):
        return os.path.basename(self.upload_file.name)


class QuestionSet(models.Model):
    # name = models.CharField(max_length=256)
    unique_code = models.CharField(max_length=10, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    questions = models.ManyToManyField(Question)
    difficulty_level = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(2)],
                                                help_text=_('0: both, 1: beginner, 2: advanced'))
    subcategory_code = models.ForeignKey(SubCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.unique_code

    @property
    def organization_code(self):
        return self.questions.first().organization_code if self.questions.count() > 0 else None

class ExamSet(models.Model):
    exam_name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    question_sets = models.ManyToManyField(QuestionSet)
    difficulty_level = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(2)],
                                                help_text=_('0: both, 1: beginner, 2: advanced'))
    organization_code = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.exam_name

    def get_difficulty_level(self):
        return ['Both', 'Beginner', 'Advanced'][self.difficulty_level]

    def get_questionset_count(self):
        return self.question_sets.all().count()

    def get_question_count(self):
        return self.question_sets.all().values_list('questions', flat=True).count()
