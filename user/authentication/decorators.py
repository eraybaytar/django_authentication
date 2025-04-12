from django.http import HttpResponseForbidden

def role_required(required_roles):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Yetkisiz erişim.")
            if request.user.role not in required_roles:
                return HttpResponseForbidden("Bu sayfaya erişim yetkiniz yok.")
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
