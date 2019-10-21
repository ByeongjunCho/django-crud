from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login  # login함수
from django.contrib.auth import logout as auth_logout
from .forms import CustomUserChangeForm
# Create your views here.

def signup(request):
    if request.user.is_authenticated:  # 로그인 상태 확인
        return redirect('articles:index')  # 로그인이 된 경우 index로 redirect
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            auth_login(request, user)
            return redirect('articles:index')
    else:
        form = UserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST) # cookie와 session을 request를 통해 넘겨준다.
        if form.is_valid():
            # 로그인
            # from IPython import embed
            # embed()
            user = form.get_user() # user를 가지고 와서
            auth_login(request, user) # login함수에 입력
            return redirect(request.GET.get('next') or 'articles:index') # 단축평가
            # return redirect('articles:index')
    else:
        form = AuthenticationForm()
        print(form)
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    return redirect('articles:index')

@login_required
def update(request):
    if request.method == 'POST':
        # 1. 사용자가 보낸 내용을 담아서
        form = CustomUserChangeForm(request.POST, instance=request.user)
        # 2. 검증
        if form.is_valid():
            form.save()
            return redirect('articles:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'accounts/form.html', {'form': form})

def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)  # 반드시 첫번째
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('articles:index')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/password_change.html', {'form': form})