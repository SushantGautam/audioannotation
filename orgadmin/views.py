import requests
from django.http import JsonResponse
from django.shortcuts import HttpResponse, render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, FormView

from orgadmin.models import User
from speaker.models import Speaker


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

class SpeakerListView(ListView):
    template_name = "orgadmin/speaker/speaker_list.html"
    model = Speaker


class UserVerification(FormView):
    def post(self, *args, **kwargs):
        if self.request.is_ajax:
            speaker = get_object_or_404(Speaker, pk=kwargs.get('user_id'))
            speaker.is_verified = True
            speaker.save()

            return JsonResponse({'message': 'success'}, status=200)
        return JsonResponse({'message': 'Bad Request.'}, status=400)


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