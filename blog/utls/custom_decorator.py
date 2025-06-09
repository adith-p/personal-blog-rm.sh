from django.conf import settings
from django.shortcuts import redirect


def only_me(view_func):
    def _inner_function(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.username == settings.USERNAME:
            return view_func(request, *args, **kwargs)
        return redirect("blog:bloglist")

    return _inner_function
