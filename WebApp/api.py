from rest_framework import viewsets, permissions

from . import serializers
from . import models


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
