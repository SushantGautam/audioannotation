from rest_framework import serializers

from . import models


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Question
        fields = [
            "last_updated",
            "created",
        ]

class SubmissionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Submissions
        fields = [
            "last_updated",
            "created",
        ]

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Project
        fields = [
            "created",
            "last_updated",
        ]
