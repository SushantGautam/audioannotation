from django.contrib.auth import logout
from django.http import HttpResponse
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from . import api
from . import views

router = routers.DefaultRouter()
router.register("Member", api.MemberViewSet)
router.register("Question", api.QuestionViewSet)
router.register("Submissions", api.SubmissionsViewSet)
router.register("Project", api.ProjectViewSet)


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key,
                         'id': token.user_id,
                         'FullName': token.user.first_name + " " + token.user.last_name,
                         })


def logout_request(request):
    logout(request)
    return HttpResponse("LoggedOut", status=200)


urlpatterns = (
    path("api/", include(router.urls)),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path("Question/", views.QuestionListView.as_view(), name="Question_list"),
    path("Question/create/", views.QuestionCreateView.as_view(), name="Question_create"),
    path("Question/detail/<int:pk>/", views.QuestionDetailView.as_view(), name="Question_detail"),
    path("Question/update/<int:pk>/", views.QuestionUpdateView.as_view(), name="Question_update"),
    path("Question/delete/<int:pk>/", views.QuestionDeleteView.as_view(), name="Question_delete"),
    path("Submissions/", views.SubmissionsListView.as_view(), name="Submissions_list"),
    path("Submissions/create/", views.SubmissionsCreateView.as_view(), name="Submissions_create"),
    path("Submissions/detail/<int:pk>/", views.SubmissionsDetailView.as_view(), name="Submissions_detail"),
    path("Submissions/update/<int:pk>/", views.SubmissionsUpdateView.as_view(), name="Submissions_update"),
    path("Submissions/delete/<int:pk>/", views.SubmissionsDeleteView.as_view(), name="Submissions_delete"),
    path("Project/", views.ProjectListView.as_view(), name="Project_list"),
    path("Project/create/", views.ProjectCreateView.as_view(), name="Project_create"),
    path("Project/detail/<int:pk>/", views.ProjectDetailView.as_view(), name="Project_detail"),
    path("Project/update/<int:pk>/", views.ProjectUpdateView.as_view(), name="Project_update"),
    path("Project/delete/<int:pk>/", views.ProjectDeleteView.as_view(), name="Project_delete"),
    path("splitAudio/<int:qid>/", views.splitAudio, name="splitAudio"),
    path("record/<int:qid>/", views.Record, name="record"),
    path("annotate/<int:qid>/", views.Annotate, name="annotate"),

    # frontend login
    path("api/token-auth", CustomObtainAuthToken.as_view()),
    path("logout", logout_request, name="logout"),

)
