from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

from .models import User
from board.models import Board
from django.http import HttpResponseRedirect
from django.urls import reverse
from accounts.email_auth import EmailAuthView
from .forms import AuthenticationForm, AgencyRegistrationForm, CompanyRegistrationForm
from django.contrib.auth.hashers import check_password


def is_Agency(user):
    return user.serializable_value('user_type') == 'Agency'


def is_Company(user):
    return user.serializable_value('user_type') == 'Company'


def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'signup.html')


@csrf_exempt
def signup_company(request):
    # user가 로그인 상태시 main으로 리다이렉트
    if request.user.is_authenticated:
        return redirect('index')

    context = {}
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user_type = 'Company'
            form.save()
            EmailAuthView.post(request, form)
            messages.info(request, '이메일 인증 후 로그인해주세요.')
            return redirect('login')
        else:
            context['form'] = form

    return render(request, 'signup_company.html', context)


@csrf_exempt
def signup_official(request):
    # user가 로그인 상태시 main으로 리다이렉트
    if request.user.is_authenticated:
        return redirect('index')

    context = {}
    if request.method == 'POST':
        form = AgencyRegistrationForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user_type = 'Agency'
            form.save()
            EmailAuthView.post(request, form)
            messages.info(request, '이메일 인증 후 로그인해주세요.')
            return redirect('login')
        else:
            context['form'] = form

    return render(request, 'signup_official.html', context)


@csrf_exempt
def login_accounts(request):
    if request.user.is_authenticated:
        return redirect('index')

    context = {}
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            user_id = request.POST['user_id']
            password = request.POST['password']
            user = authenticate(user_id=user_id, password=password)

            if user:
                if not user.email_auth:
                    messages.info(request, '　　　　　이메일 인증 후 로그인해주세요.')
                    return redirect('login')
                else:
                    login(request, user)
                    next_url = request.GET.get('next')
                    if next_url:
                        return redirect(next_url)
                    return redirect('index')
        else:
            context['form'] = form
    return render(request, 'login.html', context)


def pwchange(request):
    if request.method == 'POST':
        user_id = request.session.get('_auth_user_id')
        user_pw = request.POST.get('password1')
        user_pw_check = request.POST.get('password2')

        if user_pw_check != user_pw:
            messages.info(request, '비밀번호가 일치하지 않습니다.')
            return HttpResponseRedirect(reverse('pwchange'))
        else:
            user = User.objects.get(id=user_id)
            user.set_password(user_pw)
            user.save()
            messages.info(request, '　　　　　　비밀번호가 변경되었습니다. 　　　　　　　다시 로그인 해주세요.')
            return HttpResponseRedirect(reverse('login'))
    return render(request, 'pwchange.html')


def withdraw(request):
    if request.method == 'POST':
        user = request.user
        password = request.POST.get('password1', '')
        confirm_password = request.POST.get('password2', '')

        if password != confirm_password:
            messages.info(request, '두 비밀번호가 일치하지 않습니다.')
            return HttpResponseRedirect(reverse('delete'))

        if check_password(password, user.password):
            user.delete()
            logout(request)
            messages.info(request, '회원탈퇴가 완료되었습니다.')
            return redirect('index')

        else:
            messages.info(request, '비밀번호가 일치하지 않습니다.')
            return HttpResponseRedirect(reverse('delete'))

    return render(request, 'delete.html')


def logout_accounts(request):
    logout(request)
    return redirect('index')


def edit_company(request):
    # user_id = request.session.get('_auth_user_id')
    # user = User.objects.get(id = user_id)
    # if request.method == 'POST':
    #     if user.user_type == 'Company':
    #         userrequest.POST.get('compName')
    return render(request, 'edit_company.html')


def edit_official(request):
    return render(request, 'edit_official.html')


def my_business(request):
    board_list = Board.objects.filter(user_id=request.user)
    context = {'board_list': board_list}
    return render(request, 'my_business.html', context)


def my_qna(request):
    return render(request, 'my_qna.html')


def signup_agreement(request):
    return render(request, 'signup_agreement.html')
