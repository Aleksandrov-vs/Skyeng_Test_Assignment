from functools import wraps

from django.http import Http404
from code_monitoring.models import Script, ScriptCheck


def user_has_script_access(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        try:
            script_id = kwargs['script_id']
            script = Script.objects.get(id=script_id)
            if script.user != user:
                raise Http404("You don't have access to this page.")

        except Script.DoesNotExist:
            raise Http404("You don't have access to this page.")

        return view_func(request, *args, **kwargs)

    return _wrapped_view


def user_has_script_check_access(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user
        try:
            script_id = kwargs['script_id']
            script = Script.objects.get(id=script_id)
            if script.user != user:
                raise Http404("You don't have access to this page.")

        except ScriptCheck.DoesNotExist:
            raise Http404("You don't have access to this page.")

        return view_func(request, *args, **kwargs)

    return _wrapped_view
