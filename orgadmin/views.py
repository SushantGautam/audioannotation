from datetime import datetime

import requests
from django.http import JsonResponse
from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, FormView

from orgadmin.models import User, ContractSign
from speaker.models import Speaker
from worker.models import Worker


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
        return super().get_queryset().filter(organization_code=self.request.user.orgadmin.organization_code)


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
        return super().get_queryset().filter(
            user__speaker__organization_code=self.request.user.orgadmin.organization_code,
            contract_code__user_type="SPE")


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
        return super().get_queryset().filter(organization_code=self.request.user.orgadmin.organization_code)


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
            return JsonResponse({'message': 'success', 'status': worker.is_verified,}, status=200)
        return JsonResponse({'message': 'Bad Request.'}, status=400)


class WorkerContractSignList(ListView):
    model = ContractSign
    template_name = 'orgadmin/worker/contract_list.html'

    def get_queryset(self):
        return super().get_queryset().filter(
            user__speaker__organization_code=self.request.user.orgadmin.organization_code,
            contract_code__user_type="WOR")


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
