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
        exclude = ['extras']


class MemberAdmin(admin.ModelAdmin):
    form = MemberAdminForm
    list_display = [
        "username", 'first_name', 'last_name', 'email',
    ]


class QuestionAdminForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = "__all__"
        exclude = ['extras']


class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm
    list_display = [
        "short_question_text",
        "id",
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
        exclude = ['extras']


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
        if instance.sound_file:
            return mark_safe('<br/><audio controls> <source src="' + instance.sound_file.url + '"> </audio> <br> ' + ''' 
        <a href='javascript:window.open("/record/{}","record", "width=400,height=400")'><b>🎤 Record New Audio</b></a> | 
        <a href='javascript:window.open("/annotate/{}","record", "")'> <b>✂ Annotate Current Audio</b></a> 
        '''.format(instance.id, instance.id))
        elif instance.id:
            return mark_safe(
                "<span class='errors'>No Audio Uploaded</span>" +
                '''<a href='javascript:window.open("/record/{}","record", "width=400,height=300")'>🎤 Record Audio</a>'''
                .format(instance.id))
        else:
            return mark_safe(
                "<span class='errors'>You will record option here to 🎤 record audio after saving.</span>")

    def split_audio(self, instance):
        return mark_safe(
            '''<a href='javascript:window.open("/splitAudio/{}","example", "width=400,height=300")'>Split Audio</a> |
            <a href="/admin/constance/config/" target="_blank">(Settings)</a>'''.format(instance.id))

    form = SubmissionsAdminForm
    list_display = [
        "created",
        'id',
        "question", 'short_comment',
        "sound_file",
        "last_updated",
    ]

    readonly_fields = [
        "last_updated",
        "created", "play_main_audio",
        # "get_splitted_chunks",
        "split_audio",
        'extras',
    ]


class ProjectAdminForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = "__all__"
        exclude = ['groups', 'user_permissions', 'extras']


class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm
    list_display = [
        "name",
        "id",
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
