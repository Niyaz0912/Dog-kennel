import random
import string

from django.http import HttpResponseRedirect, HttpResponse

from django.contrib import messages
from django.shortcuts import render, reverse, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy


from users.forms import UserRegisterForm, UserLoginForm, UserUpdateForm, UserPasswordChangeForm
from users.services import send_register_email, send_new_password


def user_register_view(request):
    form = UserRegisterForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            new_user = form.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            try:
                send_register_email(new_user.email)
            except Exception:
                print('Не удалось отправить письмо!')
            return HttpResponseRedirect(reverse('users:login_user'))
    context = {
        'form': form
    }
    return render(request, 'user/register_user.html', context)


def user_login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(email=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('dogs:index'))
                else:
                    return HttpResponse('Аккаунт неактивен!')

    form = UserLoginForm()
    context = {
        'form': form
    }

    return render(request, 'user/login_user.html', context)


@login_required
def user_profile_view(request):
    user_object = request.user
    context = {
        # 'user_object': user_object,
        'title': f'Ваш профиль {user_object.first_name}',
        # 'form': UserForm(instance=user_object),
    }
    return render(request, 'user/user_profile_read_only.html', context)


@login_required
def user_update_view(request):
    user_object = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user_object)
        if form.is_valid():
            user_object = form.save()
            user_object.save()
            return HttpResponseRedirect(reverse('users:profile_user'))
    user_name = user_object.first_name
    context = {
        'user_object': user_object,
        'title': f'Изменить профиль {user_name}',
        'form': UserUpdateForm(instance=user_object)
    }
    return render(request, 'user/update_user.html', context)
    # return render(request, 'user/update_user.html', {
    #     'object': user_object,
    #     'title': f'Изменить профиль{user_object.first_name}',
    #     'form'; UserUpdateForm(isinstance=user_object)
    # })


@login_required
def user_change_password_view(request):
    user_object = request.user
    form = UserPasswordChangeForm(user_object, request.POST)
    if request.method == "POST":
        if form.is_valid():
            user_object = form.save()
            update_session_auth_hash(request, user_object)
            messages.success(request, "Пароль был успешно изменен!")
            return HttpResponseRedirect(reverse('users:profile_user'))
        else:
            messages.error(request, "Не удалось изменить пароль!")

    context = {
        'form': form
    }
    return render(request, 'user/change_password_user.html', context)


# class UserPasswordChangeView(PasswordChangeView):
#     form_class = UserPasswordChangeForm
#     success_url = reverse_lazy('user:profile_user')
#     template_name = 'user/change_password_user.html'


def user_logout_view(request):
    logout(request)
    return redirect('dogs:index')


@login_required
def user_generate_new_password(request):
    new_password = ''.join(random.sample((string.ascii_letters + string.digits), 12))
    request.user.set_password(new_password)
    request.user.save()
    send_new_password(request.user.email, new_password)
    return redirect(reverse('dogs:index'))
