from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserCreationForm


def user_register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('index')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки ниже.')
    else:
        form = UserCreationForm()

    return render(
        request=request,
        template_name='register.html',
        context={'form': form}
    )


def user_login_view(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        remember_me = request.POST.get('remember_me')  # получение значения чекбокса

        user = authenticate(request=request, username=phone_number, password=password)

        if user:
            login(request, user)
            messages.success(request, 'Вы успешно вошли в аккаунт')

            # время жизни сессии для запоминания авторизованного пользователя
            if remember_me:
                request.session.set_expiry(1209600)  # 2 недели в секундах
            else:
                request.session.set_expiry(0)  # удаление сессии после закрытия браузера

            return redirect('index')

        messages.error(request, 'Неверный логин или пароль.')

    return redirect('index')


def user_logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из аккаунта.')

    return redirect('index')
