from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, UpdateView, View, TemplateView, ListView

from users.models import User

from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string

from users.forms import UserRegisterForm, UserProfileForm, PasswordResetForm, UserLoginForm
from users.services import send_verification_email, send_password


class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def form_invalid(self, form):
        if not form.user_cache or not form.user_cache.is_active:
            messages.error(self.request, 'Ваш аккаунт не активен!')
            return redirect(reverse_lazy('users:ban'))

        return super().form_invalid(form)


class BanView(TemplateView):
    model = User
    template_name = 'users/ban.html'


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        verification_token = get_random_string(length=15)
        form.instance.verification_token = verification_token
        send_verification_email(form.instance.email, verification_token)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('users:verify_email')


class VerifyEmailView(View):
    template_name = 'users/verify_email.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        verification_code = request.POST.get('verification_code')
        User = get_user_model()
        try:
            user = User.objects.get(verification_token=verification_code)
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return redirect('users:confirmation_success')
        except User.DoesNotExist:
            pass
        return redirect('users:confirmation_error')


class ConfirmationSuccessView(TemplateView):
    template_name = 'users/confirmation_success.html'


class ConfirmationErrorView(TemplateView):
    template_name = 'users/confirmation_error.html'


class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class ConfirmEmailView(View):

    def get(self, request, token):
        User = get_user_model()

        try:
            user = User.objects.get(verification_token=token)
            if not user.is_verified:
                user.is_verified = True
                user.save()
                return render(request, 'confirmation_success.html')

        except User.DoesNotExist:
            return render(request, 'confirmation_error.html')


class GenerateAndSendNewPasswordView(LoginRequiredMixin, View):
    template_name = 'users/generate_and_send_password.html'
    form = PasswordResetForm()

    def get(self, request):
        return render(request, self.template_name, {'form': self.form})

    def post(self, request):
        self.form = PasswordResetForm(request.POST)
        if self.form.is_valid():
            email = self.form.cleaned_data['email']
            if send_password(email):
                return render(request, 'users/password_reset_success.html', {'email': email})
        return render(request, 'users/password_reset_error.html')


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'users/user_list.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        queryset = User.objects.filter(is_staff=False)
        return queryset


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:user_list')
    permission_required = 'users.set_active'
    fields = ['is_active', ]



