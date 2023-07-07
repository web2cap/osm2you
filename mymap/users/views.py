from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, UpdateView

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("markers:index")
    template_name = "users/signup.html"


class EditProfile(UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = "users/editprofile.html"
    success_url = reverse_lazy("markers:myprofile")

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.request.user.pk)

    def get(self, request, *args, **kwargs):
        self.referer = request.META.get("HTTP_REFERER", "")
        request.session["login_referer"] = self.referer
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.referer = request.session.get("login_referer", "")
        return super().post(request, *args, **kwargs)
