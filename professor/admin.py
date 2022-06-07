from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import *

admin.site.register(Professor)
admin.site.register(Category)
admin.site.register(SubCategory)

class QuestionResource(resources.ModelResource):
    class Meta:
        model = Question

class QuestionAdmin(ImportExportModelAdmin):
    resource_class = QuestionResource

class QuestionSetResource(resources.ModelResource):
    class Meta:
        model = QuestionSet

class QuestionSetAdmin(ImportExportModelAdmin):
    resource_class = QuestionSetResource

class ExamSetResource(resources.ModelResource):
    class Meta:
        model = ExamSet

class ExamSetAdmin(ImportExportModelAdmin):
    resource_class = ExamSetResource

admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionSet, QuestionSetAdmin)
admin.site.register(ExamSet, ExamSetAdmin)
