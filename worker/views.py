import json
import os

from django.conf import settings
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, FormView, CreateView

from orgadmin.forms import UserChangeForm
from orgadmin.models import Contract, ContractSign, VerificationRequest
from professor.models import Question

from speaker.models import SpeakerSubmission, ExamSetSubmission

from worker.forms import ExamSetSubmissionFilterForm, ProfileEditForm
from worker.models import WorkerSubmission, WorkerTask


def homepage(request):
    context = {}
    return render(request, 'worker/homepage.html', context)


class ProfileEditView(FormView):
    form_class = ProfileEditForm
    base_user_form_class = UserChangeForm
    template_name = 'worker/edit_profile.html'
    success_url = reverse_lazy('worker:profile')

    def get(self, request, *args, **kwargs):
        super(ProfileEditView, self).get(request, *args, **kwargs)
        form = self.form_class(instance=self.request.user.worker)
        userForm = self.base_user_form_class(instance=self.request.user)
        return self.render_to_response(self.get_context_data(form=form, userForm=userForm))

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.request.user.worker)
        userForm = self.base_user_form_class(request.POST, instance=self.request.user)

        if form.is_valid() and userForm.is_valid():
            obj = form.save(commit=False)
            userForm.save()

            # After profile edit, admin needs to re-verify the account
            obj.is_verified = False
            obj.save()

            return redirect(self.success_url)
        else:
            return self.render_to_response(
                self.get_context_data(form=form, form2=userForm))


class RequestVerification(FormView):
    success_url = reverse_lazy('worker:profile')

    def post(self, request, *args, **kwargs):
        # Create Verification Request if no pending requests.
        if not self.request.user.worker.is_pending_verification():
            VerificationRequest.objects.create(user=self.request.user)
        return redirect(self.success_url)


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


def task_choice_map(status):
    MAPPING = {
        'SA1': 'S1',
        'SA2': 'S2',
        'TA1': 'T1',
        'TA2': 'T2',
        'EA1': 'E1',
        'EA2': 'E2',
    }
    return MAPPING[status]


class WorkerTaskCreate(CreateView):
    def get(self, request, *args, **kwargs):
        context = {
            'examSetSubmission': request.GET.get('examSetSubmission')
        }
        return render(request, 'worker/alerts/confirmTaskApplication.html', context)

    def post(self, request, *args, **kwargs):
        type = task_choice_map(ExamSetSubmission.objects.get(pk=request.POST.get('examSetSubmission')).next_status()[0])
        ins = WorkerTask.objects.create(
            worker=self.request.user.worker,
            examset_submission_id=request.POST.get('examSetSubmission'),
            task_type=type
        )
        if ins:
            return JsonResponse({}, status=201)


class WorkerTaskListView(ListView):
    model = WorkerTask
    template_name = 'worker/workerTaskList.html'

    def get_template_names(self):
        return self.template_name

    def get_queryset(self):
        return super().get_queryset()


class MyTaskListView(ListView):
    model = WorkerTask
    template_name = 'worker/myTaskList.html'

    def get_template_names(self):
        return self.template_name

    def get_queryset(self):
        qs = super().get_queryset().filter(worker=self.request.user.worker, approved=True)
        if not 'type' in self.request.GET or self.request.GET.get('type') == 'slicing':
            qs = qs.filter(task_type__in=['S1', 'S2'])
        elif self.request.GET.get('type') == 'tagging':
            qs = qs.filter(task_type__in=['T1', 'T2'])
        elif self.request.GET.get('type') == 'evaluation':
            qs = qs.filter(task_type__in=['E1', 'E2'])
        return qs


class AnnotationPage(TemplateView):
    template_name = 'worker/annotationTool.html'

    def get_context_data(self, **kwargs):
        context = super(AnnotationPage, self).get_context_data()
        workerTaskObj = get_object_or_404(WorkerTask, pk=kwargs.get('workertask_id'))

        context['worker_task'] = workerTaskObj
        context['exam_set'] = workerTaskObj.examset_submission.exam_set
        context['question_sets'] = workerTaskObj.examset_submission.exam_set.question_sets.all()

        if self.request.GET.get('question'):
            question = Question.objects.get(pk=self.request.GET.get('question'))
        else:
            question = workerTaskObj.examset_submission.exam_set.question_sets.first().questions.first()
        speakerSubmissionObj = SpeakerSubmission.objects.get(speaker=workerTaskObj.examset_submission.speaker,
                                                             question=question)

        context['audio_obj'] = speakerSubmissionObj
        context['stt_data'] = json.dumps(speakerSubmissionObj.stt_data)
        annotated_data = ""
        workerSubmissionObj = None
        if WorkerSubmission.objects.filter(speaker_submission__pk=speakerSubmissionObj.id,
                                           worker_task__worker=self.request.user.worker).exists():
            workerSubmissionObj = WorkerSubmission.objects.get(speaker_submission__pk=speakerSubmissionObj.id,
                                                               worker_task__worker=self.request.user.worker)
            annotated_data = workerSubmissionObj.work_data
        context['annotated_data'] = annotated_data
        context['workerSubmissionObj'] = workerSubmissionObj

        return context


class WorkerTaskSubmit(View):
    def post(self, *args, **kwargs):
        if WorkerSubmission.objects.filter(speaker_submission__pk=kwargs.get('speakersubmission_id'),
                                           worker_task__worker=self.request.user.worker,
                                           worker_task_id=kwargs.get('task_id')).exists():
            obj = WorkerSubmission.objects.get(speaker_submission__pk=kwargs.get('speakersubmission_id'),
                                               worker_task__worker=self.request.user.worker,
                                               worker_task_id=kwargs.get('task_id'))
            obj.work_data = self.request.POST.get('annotated_data')
            obj.status = True
            obj.save()
        else:
            obj = WorkerSubmission.objects.create(
                worker_task_id=kwargs.get('task_id'),
                speaker_submission_id=int(kwargs.get('speakersubmission_id')),
                work_data=json.loads(self.request.POST.get('annotated_data')),
                status=True
            )

        # If worker task submission count of exam set is same as number of questions in exam set, then worker task is completed
        workerTask_complete = obj.worker_task.examset_submission.exam_set.get_question_count() == WorkerSubmission.objects.filter(
            status=True, worker_task=obj.worker_task).count()
        if workerTask_complete and not obj.worker_task.status:
            obj.worker_task.status = True
            examSet = obj.worker_task.examset_submission
            examSet.status = obj.worker_task.examset_submission.next_status()[0]
            examSet.save()
            obj.worker_task.save()
        return JsonResponse({"message": "success"}, status=200)


class SaveAnnotation(View):
    def post(self, *args, **kwargs):
        if self.request.is_ajax and self.request.method == "POST":
            if SpeakerSubmission.objects.filter(pk=kwargs.get('speakersubmission_id')).exists():
                if WorkerSubmission.objects.filter(speaker_submission__pk=kwargs.get('speakersubmission_id'),
                                                   worker_task__worker=self.request.user.worker,
                                                   worker_task_id=kwargs.get('task_id')).exists():
                    obj = WorkerSubmission.objects.get(speaker_submission__pk=kwargs.get('speakersubmission_id'),
                                                       worker_task__worker=self.request.user.worker,
                                                       worker_task_id=kwargs.get('task_id'))
                    obj.work_data = self.request.POST.get('annotated_data')
                    obj.save()
                else:
                    WorkerSubmission.objects.create(
                        worker_task_id=kwargs.get('task_id'),
                        speaker_submission_id=int(kwargs.get('speakersubmission_id')),
                        work_data=json.loads(self.request.POST.get('annotated_data'))
                    )
                return render(self.request, 'worker/alerts/annotationSaveSuccess.html')
        return JsonResponse({"error": ""}, status=400)


class ProfileView(TemplateView):
    template_name = "worker/profile.html"


class ContractView(View):
    def get(self, request, **kwargs):
        context = {}
        context['contract'] = Contract.objects.filter(user_type='WOR', is_active=True,
                                                      created_by__organization_code=self.request.user.worker.organization_code).first()
        context['has_contract'] = request.user.worker.has_contract()
        context['has_contract_submitted'] = request.user.worker.has_contract_submitted()
        context['has_contract_approved'] = request.user.worker.has_contract_approved()
        return render(request, 'worker/contract.html', context)

    def post(self, request, **kwargs):
        if ContractSign.objects.filter(user=self.request.user, contract_code__user_type='WOR', approved=False,
                                       contract_code__created_by__organization_code=self.request.user.worker.organization_code).exists():
            contract = ContractSign.objects.get(user=self.request.user, contract_code__user_type='WOR', approved=False,
                                                contract_code__created_by__organization_code=self.request.user.worker.organization_code)
        else:
            contract = ContractSign()
        contract.user = request.user
        contract.upload_file = request.FILES['contract-file']
        contract.approved = None
        contract.contract_code_id = request.POST.get('contract-id')
        contract.save()
        return redirect('worker:contract')
