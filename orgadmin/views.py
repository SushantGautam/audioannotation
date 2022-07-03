import os
from datetime import datetime

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, FormView, CreateView, DetailView, UpdateView, DeleteView

from orgadmin.forms import ContractForm, UserRegistrationForm
from orgadmin.models import User, ContractSign, Contract, Organization
from professor.forms import QuestionForm, QuestionSetForm
from professor.models import SubCategory, Category, Question, QuestionSet, Professor, ExamSet
from speaker.models import Speaker, ExamSetSubmission, SpeakerSubmission
from worker.models import Worker, WorkerTask, EvaluationTitle


def homepage(request):
    if hasattr(request.user, 'orgadmin'):
        all_task = WorkerTask.objects.all()
        context = {
            'user_count': User.objects.all().count(),
            'speaker_count': Speaker.objects.all().count(),
            'worker_count': Worker.objects.all().count(),
            'professor_count': Professor.objects.all().count(),
            'latest_tasks': all_task.order_by('-pk')[:5],
            'pending_task': all_task.filter(status=False).count(),
            'completed_task': all_task.filter(status=True).count(),
        }

        return render(request, 'orgadmin/homepage.html', context=context)
    elif hasattr(request.user, 'speaker'):
        return redirect('speaker:homepage')
    elif hasattr(request.user, 'professor'):
        return redirect('professor:homepage')
    elif hasattr(request.user, 'worker'):
        return redirect('worker:homepage')
    else:
        return JsonResponse({'error': 'User not assigned to any role'})


def user_register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("account_login")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = UserRegistrationForm()
    return render(request=request, template_name="account/register.html", context={"register_form": form})


# For development phase only
def gitpull(request):
    import subprocess
    # process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
    # output = process.communicate()[0]
    command = "git pull"
    ret = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
    return HttpResponse(ret.stdout.decode())


def migratedb(request):
    import subprocess
    command = ". venv/bin/activate; python manage.py makemigrations; python manage.py migrate;"
    ret = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
    return HttpResponse(ret.stdout.decode())


def deployserver(request):
    import subprocess
    command = "sh deploy.sh;"
    ret = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
    return HttpResponse(ret.stdout.decode())


class ProfileView(TemplateView):
    template_name = "orgadmin/profile.html"


class UserListView(ListView):
    template_name = "orgadmin/userList.html"
    model = User


class ContractListView(ListView):
    template_name = "orgadmin/contract/contractList.html"
    model = Contract

    def get_context_data(self, **kwargs):
        context = super(ContractListView, self).get_context_data(**kwargs)
        existing_choices = Contract.objects.all().values_list('user_type', flat=True)
        choices = list(Contract.USER_TYPE_CHOICES)
        new_choices = []
        for value, display in choices:
            if value not in existing_choices:
                new_choices.append((value, display))
        context['can_create'] = True if len(new_choices) > 0 else False
        return context


class ContractCreateView(CreateView):
    model = Contract
    form_class = ContractForm
    template_name = 'orgadmin/contract/contractForm.html'
    success_url = reverse_lazy('contract_list')

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = self.request.user.orgadmin
            obj.save()
        return super().form_valid(form)


class ContractEditView(UpdateView):
    model = Contract
    form_class = ContractForm
    template_name = 'orgadmin/contract/contractForm.html'
    success_url = reverse_lazy('contract_list')

    def form_valid(self, form):
        return super().form_valid(form)


class ContractDeleteView(DeleteView):
    model = Contract
    success_url = reverse_lazy('contract_list')


class ContractDetailView(DetailView):
    model = Contract
    template_name = 'orgadmin/contract/contractDetail.html'


class UserChangeBlock(FormView):
    def post(self, *args, **kwargs):
        if self.request.is_ajax:
            user = get_object_or_404(User, pk=kwargs.get('user_id'))
            if '/block' in self.request.path:
                user.is_active = False
            else:
                user.is_active = True
            user.save()

            return JsonResponse({'message': 'success'}, status=200)
        return JsonResponse({'message': 'Bad Request.'}, status=400)


class SpeakerListView(ListView):
    template_name = "orgadmin/speaker/speaker_list.html"
    model = Speaker

    def get_queryset(self):
        qs = super().get_queryset().filter(organization_code=self.request.user.orgadmin.organization_code)
        query_param = self.request.GET.get('status', None)
        if query_param and query_param.lower() == 'pending':
            listOfIds = [x.id for x in qs if x.get_verification_status().lower() == query_param]
            qs = qs.filter(pk__in=listOfIds)
        elif query_param and query_param.lower() == 'verified':
            qs = qs.filter(is_verified=True)
        elif query_param and query_param.lower() == 'rejected':
            listOfIds = [x.id for x in qs if x.get_verification_status().lower() == query_param]
            qs = qs.filter(pk__in=listOfIds)
        elif query_param and query_param.lower() == 'inactive':
            qs = qs.filter(user__is_active=False)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(SpeakerListView, self).get_context_data(*args, **kwargs)
        qs = super().get_queryset().filter(organization_code=self.request.user.orgadmin.organization_code)
        context['total'] = qs.count()
        listOfIds = [x.id for x in qs if x.get_verification_status().lower() == 'pending']
        context['pending'] = qs.filter(pk__in=listOfIds).count()
        context['verified'] = qs.filter(is_verified=True).count()
        listOfIds = [x.id for x in qs if x.get_verification_status().lower() == 'rejected']
        context['rejected'] = qs.filter(pk__in=listOfIds).count()
        context['inactive'] = qs.filter(user__is_active=False).count()
        context['on_recording'] = qs.exclude(
            pk__in=ExamSetSubmission.objects.all().values_list("speaker_id", flat=True)).distinct().count()
        context['recording_completed'] = qs.filter(
            pk__in=ExamSetSubmission.objects.all().values_list("speaker_id", flat=True)).distinct().count()
        context['stt_submitted'] = qs.filter(
            pk__in=ExamSetSubmission.objects.exclude(status__in=['INS', 'STI', 'STF']).values_list("speaker_id",
                                                                                                   flat=True)).distinct().count()
        return context


class SpeakerDetailView(DetailView):
    template_name = "orgadmin/speaker/speaker_detail.html"
    model = Speaker

    def get_context_data(self, *args, **kwargs):
        context = super(SpeakerDetailView, self).get_context_data(*args, **kwargs)
        return context


class SpeakerResultView(DetailView):
    model = Speaker
    template_name = "orgadmin/speaker/speaker_result.html"

    def get_context_data(self, *args, **kwargs):
        context = super(SpeakerResultView, self).get_context_data(*args, **kwargs)

        # exam_sets = ExamSet.objects.filter(
        #     pk__in=self.object.speakersubmission_set.values_list('exam_set', flat=True).distinct())
        #
        # solved_exam_sets = ExamSet.objects.filter(
        #     pk__in=self.object.examsetsubmission_set.values_list('exam_set', flat=True).distinct())
        #
        # question_sets = QuestionSet.objects.filter(examset__in=exam_sets).distinct()
        # solved_question_sets = QuestionSet.objects.filter(examset__in=solved_exam_sets).distinct()
        #
        # total_question = Question.objects.filter(questionset__in=question_sets).distinct()
        # solved_question = Question.objects.filter(questionset__in=solved_question_sets).distinct()
        #
        # context['tq_count'] = len(total_question)
        # context['sq_count'] = len(solved_question)
        # context['uq_count'] = context['tq_count'] - context['sq_count']
        # context['total_question'] = total_question
        # context['solved_question'] = solved_question

        status = self.request.GET.get('status', None)
        total_questions = Question.objects.filter(questionset__in=QuestionSet.objects.filter(is_active=True)).distinct()
        solved_question_ids = self.object.speakersubmission_set.values_list('question', flat=True).distinct()
        solved_question = Question.objects.filter(pk__in=solved_question_ids).distinct()
        unsolved_question = total_questions.exclude(pk__in=solved_question).distinct()
        if status == 'solved':
            context['questions'] = solved_question
        elif status == 'unsolved':
            context['questions'] = unsolved_question
        else:
            context['questions'] = total_questions

        context['tq_count'] = total_questions.count()
        context['sq_count'] = solved_question.count()
        context['uq_count'] = unsolved_question.count()

        for question in context['questions']:
            if question in solved_question:
                question.solved = True
                ss = SpeakerSubmission.objects.filter(speaker=self.object, question=question).first()

                # question.audio_url = '/media/' + question.speakersubmission_set.values_list('audio_file', flat=True).first()
                question.audio_url = ss.audio_file.url
                # question.audio_recorded_date = question.speakersubmission_set.first().created_at
                question.audio_recorded_date = ss.created_at
                # question.audio_recording_size = round(os.path.getsize(os.path.join(settings.MEDIA_ROOT, question.speakersubmission_set.values_list('audio_file', flat=True).first())) / (1024 * 1024),2)
                question.audio_recording_size = round(
                    os.path.getsize(os.path.join(settings.MEDIA_ROOT, str(ss.audio_file))) / (1024 * 1024), 2)

                # print('url', ss.audio_file.url)
                # print('audio_recorded_date', ss.created_at)
                # print('audio_recording_size', round(os.path.getsize(os.path.join(settings.MEDIA_ROOT,ss.audio_file )),2))

        return context


class SpeakerVerification(FormView):
    def post(self, *args, **kwargs):
        if self.request.is_ajax:
            speaker = get_object_or_404(Speaker, pk=kwargs.get('user_id'))
            speaker.is_verified = True if self.request.POST.get('is_approved') == str(1) else False

            if speaker.user.verificationrequest_set.filter(approved=None).exists():
                vr = speaker.user.verificationrequest_set.filter(approved=None).last()
                vr.approved = True if self.request.POST.get('is_approved') == str(1) else False
                vr.approved_at = datetime.utcnow()
                vr.save()
            speaker.save()

            return JsonResponse({'message': 'success', 'status': speaker.is_verified}, status=200)
        return JsonResponse({'message': 'Bad Request.'}, status=400)


class SpeakerContractSignList(ListView):
    model = ContractSign
    template_name = 'orgadmin/speaker/contract_list.html'

    def get_queryset(self):
        qs = super().get_queryset().filter(
            user__speaker__organization_code=self.request.user.orgadmin.organization_code,
            contract_code__user_type="SPE")
        query_param = self.request.GET.get('status', None)
        if query_param and query_param.lower() == 'pending':
            qs = qs.filter(approved=None)
        elif query_param and query_param.lower() == 'verified':
            qs = qs.filter(approved=True)
        elif query_param and query_param.lower() == 'rejected':
            qs = qs.filter(approved=False)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(SpeakerContractSignList, self).get_context_data(*args, **kwargs)
        qs = super().get_queryset().filter(
            user__speaker__organization_code=self.request.user.orgadmin.organization_code,
            contract_code__user_type="SPE")
        context['total'] = qs.count()
        context['pending'] = qs.filter(approved=None).count()
        context['verified'] = qs.filter(approved=True).count()
        context['rejected'] = qs.filter(approved=False).count()
        return context


class SpeakerContractSignVerify(FormView):
    def post(self, *args, **kwargs):
        if self.request.is_ajax:
            contract = get_object_or_404(ContractSign, pk=kwargs.get('contract_id'))
            contract.approved = True if self.request.POST.get('is_approved') == str(1) else False
            contract.approved_at = datetime.utcnow()
            contract.save()

            return JsonResponse(
                {'message': 'success', 'status': contract.approved, 'approved_date': contract.approved_at}, status=200)
        return JsonResponse({'message': 'Bad Request.'}, status=400)


class WorkerListView(ListView):
    template_name = "orgadmin/worker/worker_list.html"
    model = Worker

    def get_queryset(self):
        qs = super().get_queryset().filter(organization_code=self.request.user.orgadmin.organization_code)
        query_param = self.request.GET.get('status', None)
        if query_param and query_param.lower() == 'pending':
            listOfIds = [x.id for x in qs if x.get_verification_status().lower() == query_param]
            qs = qs.filter(pk__in=listOfIds)
        elif query_param and query_param.lower() == 'verified':
            qs = qs.filter(is_verified=True)
        elif query_param and query_param.lower() == 'rejected':
            listOfIds = [x.id for x in qs if x.get_verification_status().lower() == query_param]
            qs = qs.filter(pk__in=listOfIds)
        elif query_param and query_param.lower() == 'inactive':
            qs = qs.filter(user__is_active=False)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(WorkerListView, self).get_context_data(*args, **kwargs)
        qs = super().get_queryset().filter(organization_code=self.request.user.orgadmin.organization_code)
        context['total'] = qs.count()
        listOfIds = [x.id for x in qs if x.get_verification_status().lower() == 'pending']
        context['pending'] = qs.filter(pk__in=listOfIds).count()
        context['verified'] = qs.filter(is_verified=True).count()
        listOfIds = [x.id for x in qs if x.get_verification_status().lower() == 'rejected']
        context['rejected'] = qs.filter(pk__in=listOfIds).count()
        context['inactive'] = qs.filter(user__is_active=False).count()
        return context


class WorkerDetailView(DetailView):
    template_name = "orgadmin/worker/worker_detail.html"
    model = Worker

    def get_context_data(self, *args, **kwargs):
        context = super(WorkerDetailView, self).get_context_data(*args, **kwargs)
        return context


class WorkerVerification(FormView):
    def post(self, *args, **kwargs):
        if self.request.is_ajax:
            worker = get_object_or_404(Worker, pk=kwargs.get('user_id'))
            worker.is_verified = True if self.request.POST.get('is_approved') == str(1) else False
            if worker.user.verificationrequest_set.filter(approved=None).exists():
                vr = worker.user.verificationrequest_set.filter(approved=None).last()
                vr.approved = True if self.request.POST.get('is_approved') == str(1) else False
                vr.approved_at = datetime.utcnow()
                vr.save()
            worker.save()
            return JsonResponse({'message': 'success', 'status': worker.is_verified, }, status=200)
        return JsonResponse({'message': 'Bad Request.'}, status=400)


class WorkerContractSignList(ListView):
    model = ContractSign
    template_name = 'orgadmin/worker/contract_list.html'

    def get_queryset(self):
        qs = super().get_queryset().filter(
            user__speaker__organization_code=self.request.user.orgadmin.organization_code,
            contract_code__user_type="WOR")
        query_param = self.request.GET.get('status', None)
        if query_param and query_param.lower() == 'pending':
            qs = qs.filter(approved=None)
        elif query_param and query_param.lower() == 'verified':
            qs = qs.filter(approved=True)
        elif query_param and query_param.lower() == 'rejected':
            qs = qs.filter(approved=False)
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(WorkerContractSignList, self).get_context_data(*args, **kwargs)
        qs = super().get_queryset().filter(
            user__speaker__organization_code=self.request.user.orgadmin.organization_code,
            contract_code__user_type="WOR")
        context['total'] = qs.count()
        context['pending'] = qs.filter(approved=None).count()
        context['verified'] = qs.filter(approved=True).count()
        context['rejected'] = qs.filter(approved=False).count()
        return context


class WorkerContractSignVerify(FormView):
    def post(self, *args, **kwargs):
        if self.request.is_ajax:
            contract = get_object_or_404(ContractSign, pk=kwargs.get('contract_id'))
            contract.approved = True if self.request.POST.get('is_approved') == str(1) else False
            contract.approved_at = datetime.utcnow()
            contract.save()

            return JsonResponse(
                {'message': 'success', 'status': contract.approved, 'approved_date': contract.approved_at}, status=200)
        return JsonResponse({'message': 'Bad Request.'}, status=400)


class WorkerTaskList(ListView):
    model = WorkerTask
    template_name = 'orgadmin/worker/task_list.html'

    def get_queryset(self):
        qs = super().get_queryset().filter(worker__organization_code=self.request.user.orgadmin.organization_code, )
        query_param = self.request.GET.get('type', None)
        if query_param and query_param.lower() == 'slicing':
            qs = qs.filter(task_type__in=['S1', 'S2'])
        if query_param and query_param.lower() == 'tagging':
            qs = qs.filter(task_type__in=['T1', 'T2'])
        if query_param and query_param.lower() == 'evaluation':
            qs = qs.filter(task_type__in=['E1', 'E2'])
        return qs


class WorkerTaskVerify(FormView):
    def post(self, *args, **kwargs):
        if self.request.is_ajax:
            task = get_object_or_404(WorkerTask, pk=kwargs.get('task_id'))
            task.approved = True if self.request.POST.get('is_approved') == str(1) else False
            task.approved_at = datetime.utcnow()
            if not task.approved:
                task.examset_submission.status = task.examset_submission.prev_status()[0]
                task.examset_submission.save()
            task.save()

            return JsonResponse(
                {'message': 'success', 'status': task.approved, 'approved_date': task.approved_at}, status=200)
        return JsonResponse({'message': 'Bad Request.'}, status=400)


class CategoryManagementListView(ListView):
    model = SubCategory
    template_name = 'orgadmin/categoryManagement/categoryManagement.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryManagementListView, self).get_context_data(*args, **kwargs)
        context['categories'] = Category.objects.filter().distinct()
        return context


class EvaluationManagementListView(ListView):
    model = EvaluationTitle
    template_name = 'orgadmin/evaluation/evaluationList.html'

    def get_context_data(self, *args, **kwargs):
        context = super(EvaluationManagementListView, self).get_context_data(*args, **kwargs)
        return context


class QuestionListPage(ListView):
    template_name = 'orgadmin/question/questionListPage.html'
    model = Question

    def get_queryset(self):
        return super(QuestionListPage, self).get_queryset().filter(
            organization_code=self.request.user.orgadmin.organization_code)


class QuestionsCreateView(CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'orgadmin/question/ajax/questionsCreateAjax.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['subcat'] = SubCategory.objects.all()
        return context

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.organization_code = self.request.user.orgadmin.organization_code
            self.object.save()
        return redirect('question_list')

    def form_invalid(self, form):
        print('form_error', form.errors)

    # def get_form_kwargs(self, *args, **kwargs):
    #     kwargs =  super().get_form_kwargs(*args, **kwargs)
    #     kwargs['request'] = self.request
    #     return kwargs


class QuestionsUpdateView(UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'orgadmin/question/ajax/questionsCreateAjax.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['subcat'] = SubCategory.objects.all()
        context['organization_codes'] = Organization.objects.all()
        return context

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.save()
        return redirect('question_list')


class QuestionDetailView(DetailView):
    model = Question
    template_name = 'orgadmin/question/questionsDetailPage.html'


def MultipleQuestionDeleteView(request):
    if request.method == 'POST':
        try:
            Obj = Question.objects.filter(pk__in=request.POST.getlist('question_ids[]'))
            Obj.delete()
            return redirect('question_list')

        except:
            messages.error(request,
                           "Cannot delete Questions")
            return JsonResponse({}, status=500)


def QuestionDeleteView(request, pk):
    if request.method == "POST":
        Question.objects.filter(pk=pk).delete()
        return redirect("question_list")


class QuestionSetListView(ListView):
    model = QuestionSet
    template_name = 'orgadmin/questionSet/QuestionSetPage.html'

    def get_queryset(self):
        qs = super(QuestionSetListView, self).get_queryset()
        print([x.organization_code for x in qs if x.organization_code == self.request.user.orgadmin.organization_code])
        pk_list = [x.pk for x in qs if x.organization_code == self.request.user.orgadmin.organization_code]
        return qs.filter(pk__in=pk_list)

    def get_context_data(self, *args, **kwargs):
        context = super(QuestionSetListView, self).get_context_data(*args, **kwargs)
        return context


class QuestionSetCreateView(CreateView):
    model = QuestionSet
    form_class = QuestionSetForm
    template_name = 'orgadmin/questionSet/ajax/QuestionSetCreateAjax.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['subcat'] = SubCategory.objects.all()
        context['qn_list'] = Question.objects.filter(organization_code=self.request.user.orgadmin.organization_code)
        # context['sel_qn_list'] = [int(x) for x in self.request.GET['qn_list'].split(",") if x]
        # context['qn_list'] = context['qn_list'].exclude(pk__in=context['sel_qn_list'])
        return context

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save(commit=False)
            try:
                selected_questions = self.request.POST.get("selected_questions").split(',')
                self.object.save()
                for q in selected_questions:
                    self.object.questions.add(Question.objects.get(pk=int(q)))
                return redirect('question_set_list')
            except Exception as e:
                print(e)
                self.object.delete()
                return redirect('question_set_list')


class QuestionsSetUpdateView(UpdateView):
    model = QuestionSet
    form_class = QuestionSetForm
    template_name = 'orgadmin/questionSet/ajax/QuestionSetCreateAjax.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['subcat'] = SubCategory.objects.all()
        context['qn_list'] = Question.objects.filter(organization_code=self.request.user.orgadmin.organization_code)
        sel_qn_list = self.object.questions.values_list("id", flat=True)
        context['sel_qn_list'] = sel_qn_list
        # context['qn_list'] = context['qn_list'].exclude(pk__in=sel_qn_list)
        return context

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save(commit=False)
            try:
                selected_questions = self.request.POST.get("selected_questions").split(',')
                self.object.save()
                for q in selected_questions:
                    self.object.questions.add(Question.objects.get(pk=int(q)))
                return redirect('question_set_list')
            except:
                print('except')
                self.object.delete()
                return redirect('question_set_list')


def MultipleQuestionSetDeleteView(request):
    if request.method == 'POST':
        try:
            Obj = QuestionSet.objects.filter(pk__in=request.POST.getlist('questionset_ids[]'))
            Obj.delete()
            return redirect('question_set_list')

        except:
            messages.error(request,
                           "Cannot delete QuestionSet")
            return JsonResponse({}, status=500)


def QuestionSetDeleteView(request, pk):
    if request.method == "POST":
        QuestionSet.objects.filter(pk=pk).delete()
        return redirect("question_set_list")


class ExamSetSubmissionList(ListView):
    model = ExamSetSubmission
    template_name = 'orgadmin/examSetSubmission/examSetSubmissionList.html'

    def get_queryset(self):
        qs = super(ExamSetSubmissionList, self).get_queryset()
        qs = qs.filter(speaker__organization_code=self.request.user.orgadmin.organization_code)
        return qs


class ExamSetGenerateStt(FormView):
    success_url = reverse_lazy('examset_submission_list')

    def post(self, request, *args, **kwargs):
        from speaker.tasks import run_STTClova
        run_STTClova.delay(exam_set_id=int(kwargs.get('examsetsubmission_id')))
        return redirect(self.success_url)


class ExamsList(ListView):
    model = ExamSet
    template_name = "orgadmin/examset/examList.html"

    def get_queryset(self):
        qs = super(ExamsList, self).get_queryset().filter(
            organization_code=self.request.user.orgadmin.organization_code)
        return qs


class ExamsDetail(DetailView):
    model = ExamSet
    template_name = "orgadmin/examset/examDetail.html"

    def get_context_data(self, **kwargs):
        context = super(ExamsDetail, self).get_context_data(**kwargs)
        speakers = Speaker.objects.filter(
            pk__in=self.object.speakersubmission_set.values_list('speaker', flat=True)).distinct()
        for speaker in speakers:
            speaker.progress = self.object.completed_question_count(speaker.id)
            speaker.exam_status = self.object.get_exam_status(speaker.id)
            speaker.submit_status = self.object.get_submit_status(speaker.id)
        context['speakers'] = speakers
        return context


def submitExam(request, exam_id):
    if request.method == 'POST':
        speaker_id, exam_id = request.POST.get('speaker_id'), exam_id
        from speaker.views import createExamSubmission
        ins = createExamSubmission(int(speaker_id), exam_id)
        if ins:
            return redirect('examset_detail', pk=exam_id)
        else:
            return redirect('examset_detail', pk=exam_id)
