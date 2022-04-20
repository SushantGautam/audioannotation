from django import forms
from django.contrib import admin
from django.shortcuts import redirect
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

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
    def response_add(self, request, obj, post_url_continue=None):
        return redirect(request.path)

    def response_change(self, request, obj):
        return redirect(request.path)

    def _getSplittedAudio(self, instance):
        return format_html_join(
            mark_safe('<br/>'),
            '<audio controls> <source src="/{}"> </audio>',
            ((line,) for line in instance.getSplittedAudio),
        ) or mark_safe(
            "<span class='errors'>No Audio Splits Found</span>")

    def play_main_audio(self, instance):
        return mark_safe('<br/><audio controls> <source src="' + instance.sound_file.url + '"> </audio> <br> ' + ''' 
        <a href='javascript:window.open("/record/{}","record", "width=400,height=400")'>Record Audio</a> 
        '''.format(instance.id)) or mark_safe(
            "<span class='errors'>No Audio Uploaded</span>" +
            '''<a href='javascript:window.open("/record/{}","record", "width=600,height=300")'>Record Audio</a>'''
            .format(instance.id))

    def splitted_audio(self, instance):
        return mark_safe(
            '''<a href='javascript:window.open("/splitAudio/{}","example", "width=600,height=300")'>Split Audio</a> |
            <a href="/admin/constance/config/" target="_blank">(Settings)</a>'''.format(instance.id))

    form = SubmissionsAdminForm
    list_display = [
        "last_updated",
        "created",
    ]

    readonly_fields = [
        "last_updated",
        "created", "playMainAduio",
        "_getSplittedAudio", "splitAudio"
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
