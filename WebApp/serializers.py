from rest_framework import serializers

from . import models


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Member
        # fields = '__all__'
        exclude = ['user_permissions', 'groups',]


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Question
        fields = '__all__'


class SubmissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Submissions
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = '__all__'
