import django_filters
from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter, SearchFilter

from . import models
from . import serializers


class MemberViewSet(viewsets.ModelViewSet):
    """ViewSet for the Member class"""

    queryset = models.Member.objects.all()
    serializer_class = serializers.MemberSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['id',]



class QuestionViewSet(viewsets.ModelViewSet):
    """ViewSet for the Question class"""

    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['id', 'project']


class SubmissionsViewSet(viewsets.ModelViewSet):
    """ViewSet for the Submissions class"""

    queryset = models.Submissions.objects.all()
    serializer_class = serializers.SubmissionsSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['id', 'question']


class ProjectViewSet(viewsets.ModelViewSet):
    """ViewSet for the Project class"""

    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['id', 'created_by']
