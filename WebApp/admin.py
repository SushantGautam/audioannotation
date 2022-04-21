from django import forms
from django.contrib import admin
from django.shortcuts import redirect
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

from . import models
from .models import Question


class MemberAdminForm(forms.ModelForm):
    class Meta:
        model = models.Member
        fields = "__all__"


class MemberAdmin(admin.ModelAdmin):
    form = MemberAdminForm
    list_display = [
        "username", 'first_name', 'last_name', 'email',
    ]


class QuestionAdminForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = "__all__"


class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm
    list_display = [
        "id",
        "question_text",
        "project",
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

    def get_form(self, request, obj=None, **kwargs):
        form = super(SubmissionsAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['submitted_by'].initial = request.user
        form.base_fields['question'].initial = Question.objects.all().last()
        return form

    def response_change(self, request, obj):
        return redirect(request.path)

    def get_splitted_chunks(self, instance):
        return format_html_join(
            mark_safe('<br/>'),
            '<audio controls> <source src="/{}"> </audio>',
            ((line,) for line in instance.getSplittedAudio),
        ) or mark_safe(
            "<span class='errors'>No Audio Splits Found</span>")

    def play_main_audio(self, instance):
        return mark_safe('<br/><audio controls> <source src="' + instance.sound_file.url + '"> </audio> <br> ' + ''' 
        <a href='javascript:window.open("/record/{}","record", "width=400,height=400")'><b>🎤 Record New Audio</b></a> | 
        <a href='javascript:window.open("/annotate/{}","record", "")'> <b>✂ Annotate Current Audio</b></a> 
        '''.format(instance.id, instance.id)) or mark_safe(
            "<span class='errors'>No Audio Uploaded</span>" +
            '''<a href='javascript:window.open("/record/{}","record", "width=600,height=300")'>🎤 Record Audio</a>'''
            .format(instance.id))

    def split_audio(self, instance):
        return mark_safe(
            '''<a href='javascript:window.open("/splitAudio/{}","example", "width=600,height=300")'>Split Audio</a> |
            <a href="/admin/constance/config/" target="_blank">(Settings)</a>'''.format(instance.id))

    form = SubmissionsAdminForm
    list_display = [
        "created",
        'id',
        "question",
        "sound_file",
        "last_updated",
    ]

    readonly_fields = [
        "last_updated",
        "created", "play_main_audio",
        "get_splitted_chunks", "split_audio", 'extras',
    ]


class ProjectAdminForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = "__all__"
        exclude = ['groups', 'user_permissions']


class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm
    list_display = [
        "id",
        "name",
        "created",
        "last_updated",
    ]
    readonly_fields = [
        "created",
        "last_updated",
    ]


# hide group from admin
from django.contrib.auth.models import Group

admin.site.unregister(Group)

admin.site.register(models.Member, MemberAdmin)

admin.site.register(models.Question, QuestionAdmin)
admin.site.register(models.Submissions, SubmissionsAdmin)
admin.site.register(models.Project, ProjectAdmin)
