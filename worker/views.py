import json
import os

from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, FormView, CreateView

from professor.models import ExamSet
from speaker.models import SpeakerSubmission, ExamSetSubmission
from worker.forms import ExamSetSubmissionFilterForm
from worker.models import WorkerSubmission


def homepage(request):
    context = {}
    return render(request, 'worker/homepage.html', context)


class ExamListView(FormView):
    template_name = "worker/examList.html"
    form_class = ExamSetSubmissionFilterForm

    def get_context_data(self, **kwargs):
        context = super(ExamListView, self).get_context_data(**kwargs)
        return context


class ExamListViewAjax(ListView):
    template_name = "worker/examListAjax.html"
    difficulty_filters = {}
    task_type_filters = {}
    region_filters = {}

    def dispatch(self, request, *args, **kwargs):
        self.region_filters = {
            'speaker__nationality__in': self.request.GET.get('countries').split(',')
        }
        self.difficulty_filters = {
            'exam_set__difficulty_level__in': self.request.GET.getlist('difficulty_level'),
            'exam_set__difficulty_level': 0,
        }

        self.task_type_filters = {
            'status__in': self.request.GET.getlist('work_type'),
        }
        return super(ExamListViewAjax, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return ExamSetSubmission.objects.filter(**self.difficulty_filters, _connector=Q.OR).filter(
            **self.task_type_filters, _connector=Q.OR).filter(**self.region_filters, _connector=Q.OR)


class QuestionSetListView(ListView):
    template_name = "worker/questionSetList.html"
    model = SpeakerSubmission

    def get_queryset(self):
        return SpeakerSubmission.objects.all()


class AnnotationPage(TemplateView):
    template_name = 'worker/annotationTool.html'

    def get_context_data(self, **kwargs):
        context = super(AnnotationPage, self).get_context_data()
        speakerObj = get_object_or_404(SpeakerSubmission, pk=kwargs.get('id'))
        context['audio_obj'] = speakerObj
        context['question_set'] = speakerObj.exam_set.question_sets.filter(
            questions__in=[speakerObj.question, ]).first()
        context['stt_data'] = json.dumps(context['audio_obj'].stt_data)
        annotated_data = ""
        if WorkerSubmission.objects.filter(speaker_submission__pk=kwargs.get('id'),
                                           worker_task__worker=self.request.user.worker).exists():
            annotated_data = WorkerSubmission.objects.get(speaker_submission__pk=kwargs.get('id'),
                                                          worker_task__worker=self.request.user.worker).split_data
        context['annotated_data'] = annotated_data

        return context


class SaveAnnotation(View):
    def post(self, *args, **kwargs):
        if self.request.is_ajax and self.request.method == "POST":
            if SpeakerSubmission.objects.filter(pk=kwargs.get('id')).exists():
                print(self.request.user.worker)
                if WorkerSubmission.objects.filter(speaker_submission__pk=kwargs.get('id'),
                                                   worker_task__worker=self.request.user.worker).exists():
                    obj = WorkerSubmission.objects.get(speaker_submission__pk=kwargs.get('id'),
                                                       worker_task__worker=self.request.user.worker)
                    obj.split_data = self.request.POST.get('annotated_data')
                    obj.save()
                else:
                    WorkerSubmission.objects.create(
                        worker_task__worker=self.request.user.worker,
                        speaker_submission_id=int(kwargs.get('id')),
                        split_data=json.loads(self.request.POST.get('annotated_data'))
                    )
                return render(self.request, 'worker/alerts/annotationSaveSuccess.html')
        return JsonResponse({"error": ""}, status=400)


class ProfileView(TemplateView):
    template_name = "worker/profile.html"
