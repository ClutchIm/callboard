from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.shortcuts import redirect


class AuthorRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_verified:
            return self.handle_no_permission()

        if request.user != self.get_object().author or request.user.is_staff:
            messages.info(request, 'Вы не являетесь автором')
            return redirect('PostList')
        return super().dispatch(request, *args, **kwargs)


class IsVerifiedMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not request.user.is_verified:
            messages.info(request, 'Доступно только верифицированным пользователям')
            return redirect('PostList')
        return super().dispatch(request, *args, **kwargs)

