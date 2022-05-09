from distutils.command.upload import upload
from django.db import models

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
    # question_set = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    upload_file = models.FileField(upload_to=question_file_name, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    level = models.IntegerField(default=1)
    subcategory_code = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class QuestionSet(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    questions = models.ManyToManyField(Question)
    def __str__(self):
        return self.name
