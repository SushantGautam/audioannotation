from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth import REDIRECT_FIELD_NAME

def authorize(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)

            raise PermissionDenied
            
        return _wrapped_view
    return decorator