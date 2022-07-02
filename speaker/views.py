import datetime
import base64
import json
from multiprocessing import context
from random import randint

from django.core.files.base import ContentFile
from django.db.models import Q
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, FormView, TemplateView, UpdateView

from orgadmin.forms import UserChangeForm
from orgadmin.models import Contract, ContractSign, VerificationRequest
from speaker.forms import SpeakerSubmissionForm, ProfileEditForm
from speaker.models import Speaker, SpeakerSubmission, ExamSetSubmission

from professor.models import Question, QuestionSet, ExamSet


def homepage(request):
    verification_request = VerificationRequest.objects.filter(user=request.user)
    contract_sign = ContractSign.objects.filter(user=request.user)
    profile_register_date, profile_approved_date = '', ''
    contract_sign_date, contract_approved_date = '', ''
    if verification_request:
        verification_request = verification_request.latest('id')
        profile_register_date = verification_request.created_at.strftime('%Y-%m-%d (%H:%M %p)')
        profile_approved_date = verification_request.approved_at.strftime(
            '%Y-%m-%d (%H:%M %p)') if verification_request.approved_at else ''
    if contract_sign:
        contract_sign = contract_sign.latest('id')
        contract_sign_date = contract_sign.created_at.strftime('%Y-%m-%d (%H:%M %p)')
        contract_approved_date = contract_sign.approved_at.strftime(
            '%Y-%m-%d (%H:%M %p)') if contract_sign.approved_at else ''

    context = {
        'profile_register_date': profile_register_date,
        'profile_approved_date': profile_approved_date,
        'contract_sign_date': contract_sign_date,
        'contract_approved_date': contract_approved_date,
    }

    return render(request, 'speaker/homepage.html', context)


class ProfileView(TemplateView):
    template_name = "speaker/profile.html"


class ProfileEditView(FormView):
    # model = Speaker
    form_class = ProfileEditForm
    base_user_form_class = UserChangeForm
    template_name = 'speaker/edit_profile.html'
    success_url = reverse_lazy('speaker:profile')

    def get(self, request, *args, **kwargs):
        super(ProfileEditView, self).get(request, *args, **kwargs)
        form = self.form_class(instance=self.request.user.speaker)
        userForm = self.base_user_form_class(instance=self.request.user)
        return self.render_to_response(self.get_context_data(form=form, userForm=userForm))

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.request.user.speaker)
        userForm = self.base_user_form_class(request.POST, instance=self.request.user)

        if form.is_valid() and userForm.is_valid():
            obj = form.save(commit=False)
            userForm.save()

            # After profile edit, admin needs to re-verify the account
            obj.verified = False
            obj.save()

            return redirect(self.success_url)
        else:
            return self.render_to_response(
                self.get_context_data(form=form, form2=userForm), status=400)


class RequestVerification(FormView):
    success_url = reverse_lazy('speaker:profile')

    def post(self, request, *args, **kwargs):
        # Create Verification Request if no pending requests.
        if not self.request.user.speaker.is_pending_verification():
            VerificationRequest.objects.create(user=self.request.user)
        return redirect(self.success_url)


class ContractView(View):
    def get(self, request, **kwargs):
        context = {}
        context['contract'] = Contract.objects.filter(user_type='SPE', is_active=True,
                                                      created_by__organization_code=self.request.user.speaker.organization_code).first()
        context['has_contract'] = request.user.speaker.has_contract()
        context['has_contract_submitted'] = request.user.speaker.has_contract_submitted()
        context['has_contract_approved'] = request.user.speaker.has_contract_approved()
        context['approved_contract_file'] = ''
        if context['has_contract_approved']:
            upload_file = ContractSign.objects.filter(user=self.request.user,
                                                      contract_code=context['contract'],
                                                      approved=True).first().upload_file
            if upload_file:
                context['approved_contract_file'] = upload_file.url
        return render(request, 'speaker/contract.html', context)

    def post(self, request, **kwargs):
        contract_code_id = request.POST.get('contract-id')
        if contract_code_id:
            contract_code = Contract.objects.filter(id=int(contract_code_id)).first()
            # contract_type = contract_code.contract_type
            if ContractSign.objects.filter(user=self.request.user, contract_code__user_type='SPE', approved=False,
                                           contract_code=contract_code).exists():
                contract = ContractSign.objects.get(user=self.request.user, contract_code__user_type='SPE',
                                                    approved=False,
                                                    contract_code=contract_code)
            else:
                contract = ContractSign()
            contract.user = request.user
            contract.contract_code = contract_code
            contract.approved = True
            contract.approved_at = timezone.now()
            upload_file = request.POST.get('contract-file')
            format, imgstr = upload_file.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=str(randint(1, 100)) + 'contract-sign' + '.' + ext)
            contract.upload_file = data
            # if contract_type == 'F':
            #     contract.upload_file = request.FILES['contract-file']
            #     contract.approved = None
            # elif contract_type == 'T':
            #     contract.approved = True
            #     contract.approved_at = datetime.datetime.now()
            contract.save()
        return redirect('speaker:contract')


class QuestionSetList(ListView):
    template_name = 'speaker/question_set_list.html'
    model = QuestionSet

    def get_queryset(self):
        qs = super(QuestionSetList, self).get_queryset().filter(examset=self.kwargs.get('exam_id'))
        if self.request.GET.get('status') == 'incomplete':
            qs = qs.filter(pk__in=[o.pk for o in qs if not o.is_complete(speaker=self.request.user.speaker)])
        # elif self.request.GET.get('status') == 'recorded':
        #     qs = qs.filter(pk__in=[o.pk for o in qs if o.is_complete(speaker=self.request.user.speaker)])
        for x in qs:
            x.complete = x.is_complete(speaker=self.request.user.speaker)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['examObj'] = get_object_or_404(ExamSet, id=self.kwargs.get('exam_id'))
        return context


class ExamSetList(ListView):
    template_name = 'speaker/exam_set_list.html'
    model = ExamSet

    def get_queryset(self):
        datetime_now = datetime.datetime.utcnow()
        qs = super(ExamSetList, self).get_queryset().filter(
            is_active=True, organization_code=self.request.user.speaker.organization_code,
            difficulty_level__in=[0, self.request.user.speaker.level_mapping()]).filter(
            Q(start_date__lte=datetime_now) | Q(start_date=None))
        for q in qs:
            q.exam_status = q.get_exam_status(self.request.user.speaker)
            q.submit_status = q.get_submit_status(self.request.user.speaker)
        return qs


class ExamPopupView(FormView):
    form_class = SpeakerSubmissionForm
    template_name = 'speaker/test_popup.html'
    qn_num = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        exam_set = get_object_or_404(ExamSet, id=self.kwargs.get('exam_id'))
        qn_set = self.request.GET['qn_set']

        qn_set = QuestionSet.objects.get(pk=qn_set)

        questions = qn_set.questions.all()
        speaker = self.request.user.speaker
        unanswered_list = qn_set.questions.exclude(
            pk__in=SpeakerSubmission.objects.filter(speaker=speaker, exam_set=exam_set).values_list('question__pk',
                                                                                                    flat=True))

        self.qn_num = list(questions.values_list('id', flat=True)).index(
            unanswered_list.first().id) if unanswered_list.count() > 0 else 0

        qn_num = int(self.request.GET.get('qn_num', self.qn_num))
        context['qn'] = questions[qn_num]

        # que_set = context['qn'].questionset_set.first()
        context['qn'].can_submit = not SpeakerSubmission.objects.filter(question=context['qn'],
                                                                        speaker=speaker,
                                                                        exam_set=exam_set).exists()

        for ques in questions:
            ques.can_submit = not SpeakerSubmission.objects.filter(question=ques,
                                                                   speaker=speaker,
                                                                   exam_set=exam_set).exists()

        context['speakerSubObj'] = SpeakerSubmission.objects.filter(question=context['qn'],
                                                                    speaker=speaker,
                                                                    exam_set=exam_set).first()
        print(context['speakerSubObj'])
        context['examObj'] = exam_set
        context['speaker'] = speaker
        context['qn_set'] = qn_set
        context['questions'] = questions
        context['qn_num'] = qn_num
        context['qn_num1'] = qn_num + 1
        context['prev_qn'] = None if qn_num == 0 else qn_num - 1
        context['next_qn'] = None if questions.count() == (qn_num + 1) else qn_num + 1
        return context

    def get_form(self, form_class=None):
        if 'id' in self.request.POST:
            form_class = self.form_class(self.request.POST, self.request.FILES,
                                         instance=SpeakerSubmission.objects.get(pk=self.request.POST.get('id')))
        else:
            form_class = self.form_class(self.request.POST, self.request.FILES)
        return form_class

    def form_valid(self, form):
        res_dict = {}
        if form.is_valid():
            print("File saved")
            obj = form.save(commit=False)
            obj.exam_set = get_object_or_404(ExamSet, id=self.kwargs.get('exam_id'))
            obj.save()
            res_dict = {
                'success': 'true',
            }
            res_dict.update(json.loads(serializers.serialize('json', [obj, ]))[0])
        else:
            print("form invalid: ", form.errors)
            res_dict = {
                'success': 'false',
            }
        return JsonResponse(res_dict)

    def form_invalid(self, form):
        print("Error: ", form.errors)
        res_dict = {
            'success': 'false',
            'error': str(form.errors),
        }
        return JsonResponse(res_dict)


def createExamSubmission(speaker_id, exam_set_id):
    if not ExamSetSubmission.objects.filter(speaker_id=speaker_id, exam_set_id=exam_set_id).exists():
        ExamSetSubmission.objects.create(speaker_id=speaker_id, exam_set_id=exam_set_id)
        return True
    return False

def submitExam(request, exam_id):
    if request.method == 'POST':
        speaker_id, exam_id = request.user.speaker.pk, exam_id
        ins = createExamSubmission(speaker_id, exam_id)
        if ins:
            return redirect('speaker:exam_set_list')
        else:
            return redirect('speaker:exam_set_list')
