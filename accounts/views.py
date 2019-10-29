from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login  # login함수
from django.contrib.auth import logout as auth_logout
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User
from django.contrib.auth import get_user_model
from IPython import embed
# Create your views here.

def signup(request):
    if request.user.is_authenticated:  # 로그인 상태 확인
        return redirect('articles:index')  # 로그인이 된 경우 index로 redirect
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('articles:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)

def login(request):
    # embed()
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
            update_session_auth_hash(request, form.user)  # 비밀번호 변경 후 로그아웃되지 않도록 session을 업데이트한다.
            return redirect('articles:index')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/password_change.html', {'form': form})

def profile(request, account_pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=account_pk)
    context = {
        'user_profile' : user
    }
    from IPython import embed
    # embed()
    return render(request, 'accounts/profile.html', context)

from .models import User as customUser
def follow(request, account_pk):
    User = get_user_model()
    obama = get_object_or_404(User, pk=account_pk)

    if obama != request.user:
        # obama를 팔로우한 적이 있다면
        if request.user in obama.followers.all():
            # 취소
            obama.followers.remove(request.user)
        # 아니면
        else:
            # 팔로우
            obama.followers.add(request.user)

    return redirect('accounts:profile', account_pk)


    