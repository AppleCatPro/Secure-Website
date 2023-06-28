import base64

from cryptography.fernet import Fernet
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import *


@login_required
def dashboard(request):
    # Получить конфиденциальные данные текущего пользователя
    user1 = request.user
    data = ConfidentialData.objects.filter(user=user1)
    user = User.objects.get(username=user1.username)

    # Журналирование доступа к панели управления
    log_entry = AuditLog(user=user, action='Доступ к dashboard', ip_address=request.META['REMOTE_ADDR'], success=True)
    log_entry.save()

    # Дешифруем и отображаем данные только для текущего пользователя
    user_key = user.encryption_key
    print(user_key)
    # f = Fernet(user_key)
    # decrypted_data = [f.decrypt(d.data.encode()).decode() for d in data]

    context = {
        # 'confidential_data': decrypted_data
        'confidential_data': data,
        'user': user
    }
    return render(request, 'dashboard.html', context)


def edit_data(request, data_id):
    # Получаем объект данных по его идентификатору
    user = request.user
    data = get_object_or_404(ConfidentialData, id=data_id)

    # Проверяем, является ли текущий пользователь владельцем данных
    if data.user != request.user:
        # Если пользователь не является владельцем данных, перенаправляем его на страницу с ошибкой доступа или другую необходимую страницу
        return redirect('access_denied')

    if request.method == 'POST':
        # Если запрос является POST-запросом, обрабатываем форму данных
        form = DataForm(request.POST, instance=data)
        if form.is_valid():
            # Если форма данных действительна, сохраняем обновленные данные
            form.save()
            # Перенаправляем пользователя на страницу с подтверждением обновления данных
            return redirect('data_updated')
    else:
        # Если запрос не является POST-запросом, создаем форму данных с исходными значениями
        form = DataForm(instance=data)

    # Журналирование доступа к панели управления
    log_entry = AuditLog(user=user, action='Доступ к редактируемым данным', ip_address=request.META['REMOTE_ADDR'],
                         success=True)
    log_entry.save()
    # Отображаем шаблон edit_data.html с формой данных
    return render(request, 'edit_data.html', {'form': form})


@login_required
def add_data(request):
    user = User.objects.get(username=request.user.username)

    if request.method == 'POST':
        form = DataForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user

            # Получаем ключ шифрования для пользователя
            user_key = user.encryption_key
            # f = Fernet(user_key)

            # Шифруем данные перед сохранением
            # encrypted_data = f.encrypt(form.cleaned_data['data'].encode())
            # data.data = encrypted_data

            data.save()

            data.save()

            # Перенаправляем пользователя на страницу с подтверждением добавления данных
            return redirect('dashboard')
    else:
        form = DataForm()

    return render(request, 'add_data.html', {'form': form})


@login_required
def delete_data(request, data_id):
    # Получаем объект данных по его идентификатору
    data = get_object_or_404(ConfidentialData, id=data_id)

    # Убеждаемся, что текущий пользователь является владельцем данных
    if data.user == request.user:
        # Проверяем, является ли запрос POST-запросом
        if request.method == 'POST':
            # Если запрос POST, удаляем данные
            data.delete()
            # Перенаправляем пользователя на страницу dashboard или на другую страницу по вашему выбору
            return redirect('dashboard')

        # Отображаем шаблон delete_data.html для подтверждения удаления
        return render(request, 'delete_data.html', {'data': data})

    # Если текущий пользователь не является владельцем данных, отображаем ошибку или перенаправляем на другую страницу
    return redirect('access_denied')


@login_required
def view_data(request, data_id):
    # Получаем объект данных по его идентификатору
    data = get_object_or_404(ConfidentialData, id=data_id)

    # Убеждаемся, что текущий пользователь является владельцем данных
    if data.user == request.user:
        # Отображаем шаблон view_data.html с данными
        return render(request, 'view_data.html', {'data': data})

    # Если текущий пользователь не является владельцем данных, отображаем ошибку или перенаправляем на другую страницу
    return redirect('access_denied')


from django.shortcuts import render


def data_updated(request):
    user = request.user
    # Журналирование доступа к панели управления
    log_entry = AuditLog(user=user, action='Данные обновлены', ip_address=request.META['REMOTE_ADDR'],
                         success=True)
    log_entry.save()
    return render(request, 'data_updated.html')


def access_denied(request):
    user = request.user
    # Журналирование доступа к панели управления
    log_entry = AuditLog(user=user, action='Доступ запрещен', ip_address=request.META['REMOTE_ADDR'],
                         success=True)
    log_entry.save()
    return render(request, 'access_denied.html')


# def register_view(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#
#             # Генерируем ключ шифрования
#             key = Fernet.generate_key()
#
#             # Сохраняем ключ шифрования для пользователя
#             user = form.instance
#             user.encryption_key = key
#             user.save()
#
#             messages.success(request, 'Registration successful. You can now log in.')
#             return redirect('login')
#     else:
#         form = CustomUserCreationForm()
#
#     return render(request, 'register.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Создаем пользователя
            user = form.save()

            # Генерируем ключ шифрования
            key = Fernet.generate_key()

            # Преобразуем ключ в base64-формат
            encoded_key = base64.urlsafe_b64encode(key)

            # Сохраняем ключ в поле encryption_key модели User
            user.encryption_key = encoded_key
            user.save()

            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    # Отображаем форму регистрации
    return render(request, 'register.html', {'form': form})


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        # 'confidential_data': decrypted_data
        'form': form,
        'user': request.user
    }
    return render(request, 'lk.html', context)


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})


@login_required
def delete_account_view(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Your account has been deleted.')
        return redirect('home')

    user = request.user
    # Журналирование доступа к панели управления
    log_entry = AuditLog(user=user, action='Successfully Deleted User', ip_address=request.META['REMOTE_ADDR'],
                         success=True)
    log_entry.save()
    return render(request, 'delete_account.html')


def home_view(request):
    return render(request, 'home.html', {'user': request.user})
