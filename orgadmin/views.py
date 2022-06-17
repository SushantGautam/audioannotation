from datetime import datetime

import requests
from django.http import JsonResponse
from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, FormView

from orgadmin.models import User, ContractSign
from speaker.models import Speaker
from worker.models import Worker, WorkerTask


def homepage(request):
    if hasattr(request.user, 'orgadmin'):
        return render(request, 'orgadmin/homepage.html')
    elif hasattr(request.user, 'speaker'):
        return redirect('speaker:homepage')
    elif hasattr(request.user, 'professor'):
        return redirect('professor:homepage')
    elif hasattr(request.user, 'worker'):
        return redirect('worker:homepage')
    else:
        return JsonResponse({'error': 'User not assigned to any role'})


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
            print('here')
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
