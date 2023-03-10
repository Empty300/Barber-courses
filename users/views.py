from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView

from store.models import Lessons
from users.forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from users.models import EmailVerification, User


class EmailVerificationView(TemplateView):
    title = 'Store - Подтверждение электронной почты'
    template_name = 'store/index.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('store:store'))


class UserRegistrationView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зарегестрировались! ' \
                      'На вашу почту было отправлено письмо для ' \
                      'подтверждения вашего email адресса'


class UserLoginView(LoginView):
    model = User
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.request.user.pk,))


class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Store - Профиль'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        context['lessons'] = Lessons.objects.all()

        return context

    def get(self, request, *args, **kwargs):
        if self.request.user.pk != self.kwargs['pk']:
            return HttpResponseRedirect(reverse('store:store'))
        else:
            return super().get(request, *args, **kwargs)


