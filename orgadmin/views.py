from django.shortcuts import HttpResponse, render


def homepage(request):
    return render(request, 'orgadmin/homepage.html')

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
    command = "sudo sh deploy.sh;"
    ret = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
    return HttpResponse(ret.stdout.decode())
