from rest_framework import viewsets, permissions

from . import models
from . import serializers


class MemberViewSet(viewsets.ModelViewSet):
    """ViewSet for the Member class"""

    queryset = models.Member.objects.all()
    serializer_class = serializers.MemberSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuestionViewSet(viewsets.ModelViewSet):
    """ViewSet for the Question class"""

    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]


class SubmissionsViewSet(viewsets.ModelViewSet):
    """ViewSet for the Submissions class"""

    queryset = models.Submissions.objects.all()
    serializer_class = serializers.SubmissionsSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProjectViewSet(viewsets.ModelViewSet):
    """ViewSet for the Project class"""

    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
