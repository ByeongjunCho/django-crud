from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
# Create your views here.

def signup(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('articles:index')
    else:
        user_form = UserCreationForm()
    context = {
        'user_form': user_form
    }
    return render(request, 'accounts/signup.html', context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST) # cookie와 session을 request를 통해 넘겨준다.
        if form.is_valid():
            # 로그인
            user = form.get_user() # user를 가지고 와서
            auth_login(request, user) # login함수에 입력
            return redirect('articles:index')
    else:
        form = AuthenticationForm()
        print(form)
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)