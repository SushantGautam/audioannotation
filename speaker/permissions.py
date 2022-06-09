from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.utils import timezone

from professor.models import ExamSet

def OrgMxnCls(obj, request):
    if obj.organization_code == request.user.organization_code:
        return True
    else:
        raise PermissionDenied()

def ExamMxnCls(obj, request):
    datetime_now = timezone.now().replace(microsecond=0)
    if obj.difficulty_level == 0 or obj.difficulty_level == request.user.level:
        if obj.start_date <= datetime_now <= obj.end_date:
            return True
    else:
        raise PermissionDenied()

class SpeakerExamMxnCls:
    def get(self, request, *args, **kwargs):
        exam_set = get_object_or_404(ExamSet, pk=kwargs.get('pk'))
        OrgMxnCls(exam_set, request)
        ExamMxnCls(exam_set, request)
        return super().get(request, *args, **kwargs)