from functools import wraps
from django.utils import six
from django.utils.decorators import available_attrs
from work_system.models import Check_In
from work_system.Josn import Json

json = Json()


def user_passes_test(test_func, what_error):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)
            else:
                return json.what_error(what_error)

        return _wrapped_view

    return decorator


def login_required(function=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """

    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        what_error='no landings'
    )
    return actual_decorator


def permission_required(perm):
    """
    Decorator for views that checks whether a user has a particular permission
    enabled, redirecting to the log-in page if necessary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """

    def check_perms(user):
        if isinstance(perm, six.string_types):
            perms = (perm,)
        else:
            perms = perm
        if user.has_perms(perms):
            return True
        return False

    return user_passes_test(check_perms, what_error='No permission')


def check_in_required(function=None):
    def is_check_in(user):
        try:
            if Check_In.objects.filter(work_number=user.username).reverse()[0].check == 0:
                return True
            return False
        except:
            return True

    return user_passes_test(is_check_in,  what_error='NO checked in')


def check_out_required(function=None):
    def is_check_in(user):
        try:
            if Check_In.objects.filter(work_number=user.username).reverse()[0].check == 0:
                return False
            return True
        except:
            return False

    return user_passes_test(is_check_in, what_error='Has been checked in')


def work_order_required(perm):
    def check(user):
        if isinstance(perm, six.string_types):
            perms = (perm,)
        else:
            perms = perm
        if user.has_perms(perms) or Check_In.objects.filter(work_number=user.username).reverse()[0].check  == 1:
            return True
        return False

    return user_passes_test(check, what_error='NO checked in')
