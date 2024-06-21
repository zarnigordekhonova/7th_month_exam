from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser
from Users.forms import RegisterForm, ProfileUpdateForm
from django.views import View
from django.contrib import messages
# Create your views here.

class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }
        return render(request, 'Users/register.html', context=context)

    def post(self, request):
        register_form = RegisterForm(data=request.POST, files=request.FILES)
        if register_form.is_valid():
            register_form.save()
            messages.success(request, 'Ro\'yxatdan o\'tish muvaffaqiyatli yakunlandi!')
            return redirect('users:login')
        else:
            context = {
                'register_form': register_form
            }
            return render(request, 'Users/register.html', context=context)


class LoginView(View):
    def get(self, request):
        forms = AuthenticationForm()
        messages_to_display = messages.get_messages(request)
        context = {
            'forms': forms,
            'messages_to_display': messages_to_display
        }
        return render(request, 'Users/login.html', context=context)

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, 'Siz saytga muvaffaqiyatli kirdingiz!')
            return redirect('chat:homepage')
        else:
            context = {
                'login_form': login_form
            }
            messages.error(request, 'Login yoki parol xato kiritilgan!')
        return render(request, 'Users/login.html', context=context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Siz saytdan muvaffaqiyatli chiqdingiz!')
        return redirect('chat:homepage')

class ProfileView(View):
    def get(self, request):
        context = {
            'user': request.user
        }

        return render(request, 'Users/profile.html', context=context)

class ProfileUpdateView(View):
    def get(self, request):
        update_form = ProfileUpdateForm(instance=request.user)
        context = {
            'form': update_form
        }
        return render(request, 'Users/profile_update.html', context=context)

    def post(self, request):
        update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if update_form.is_valid():
            update_form.save()
            messages.success(request, 'Profil muvaffaqiyatli o\'zgartirildi!')
            return redirect('users:profile')
        else:
            context = {
                'form': update_form
            }
            return render(request, 'Users/profile_update.html', context=context)
