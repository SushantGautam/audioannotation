from django.contrib import admin
from django import forms

from . import models


class QuestionAdminForm(forms.ModelForm):

    class Meta:
        model = models.Question
        fields = "__all__"


class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm
    list_display = [
        "last_updated",
        "created",
    ]
    readonly_fields = [
        "last_updated",
        "created",
    ]


class SubmissionsAdminForm(forms.ModelForm):

    class Meta:
        model = models.Submissions
        fields = "__all__"


class SubmissionsAdmin(admin.ModelAdmin):
    form = SubmissionsAdminForm
    list_display = [
        "last_updated",
        "created",
    ]
    readonly_fields = [
        "last_updated",
        "created",
    ]


class ProjectAdminForm(forms.ModelForm):

    class Meta:
        model = models.Project
        fields = "__all__"


class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm
    list_display = [
        "created",
        "last_updated",
    ]
    readonly_fields = [
        "created",
        "last_updated",
    ]


admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Submissions, SubmissionsAdmin)
admin.site.register(models.Project, ProjectAdmin)
