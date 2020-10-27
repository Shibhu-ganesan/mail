from django.shortcuts import render, redirect
from .Forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group
from .models import *
from django.core.mail import send_mail
from django.conf import settings


def dashboard(request):
    context = {}
    return render(request, "joinwithmeapp/dashboard.html", context)


def startup_page(request):
    context = {}
    return render(request, "joinwithmeapp/startup.html", context)


def startup_user(request, pk):
    user = StartUp.objects.get(id=pk)
    context = {'user': user}
    return render(request, 'joinwithmeapp/startup_user.html', context)


def member_page(request):
    context = {}
    return render(request, "joinwithmeapp/member.html", context)


def member_user(request, pk):
    user = Member.objects.get(id=pk)
    context = {'user': user}
    return render(request, 'joinwithmeapp/member_user.html', context)


def investor_page(request):
    context = {}
    return render(request, "joinwithmeapp/investor.html", context)


def investor_user(request, pk):
    user = Investor.objects.get(id=pk)
    context = {'user': user}
    return render(request, 'joinwithmeapp/investor_user.html', context)


def startup_form(request):
    form = StartUpForm()
    if request.method == "POST":
        form = StartUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("sta_reg")

    context = {"form": form}
    return render(request, 'joinwithmeapp/startup_form.html', context)


def member_form(request):
    form = MemberForm()
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mem_reg')
    context = {"form": form}

    return render(request, 'joinwithmeapp/member_form.html', context)


def investor_form(request):
    form = InvestorForm()
    if request.method == "POST":
        form = InvestorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inv_reg')
    context = {"form": form}

    return render(request, 'joinwithmeapp/investor_form.html', context)


def l_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            group = request.user.groups.all()[0].name
            if group == 'member':
                return redirect('member_user')
            if group == 'investor':
                return redirect('investor_user')
            if group == 'startup_seeker':
                return redirect('startup_user')
            group = None
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'joinwithmeapp/login.html', context)


def member_register(request):
    group = None
    form = CreateUserForm()
    user = Member.objects.all()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            subject = 'Thank you......'
            message = 'Welcome da venna.'
            from_email = settings.EMAIL_HOST_USER
            to_list = [user.email, settings.EMAIL_HOST_USER]
            send_mail(subject, message, from_email, to_list, fail_silently=True)
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='member')
            user.groups.add(group)
            Member.objects.create(

                Name=user.username
            )
            messages.success(request, "Hell yeah Welcome" + username)
            return redirect("login")
    context = {"form": form}
    return render(request, 'joinwithmeapp/member_register.html', context)


def investor_register(request):
    group = None
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='investor')
            user.groups.add(group)
            Investor.objects.create(
                user=user,
                Name=user.username
            )

            messages.success(request, "Hell yeah Welcome" + username)
            return redirect("login")
    context = {"form": form}
    return render(request, 'joinwithmeapp/investor_register.html', context)


def startup_register(request):
    group = None
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='startup_seeker')
            user.groups.add(group)
            StartUp.objects.create(
                user=user,
                Name=user.username
            )

            messages.success(request, "Hell yeah Welcome" + username)
            return redirect("login")
    context = {"form": form}
    return render(request, 'joinwithmeapp/startup_register.html', context)


def reg_before(request):
    context = {}
    return render(request, 'joinwithmeapp/reg_before_page.html', context)


def logoutt(req):
    logout(req)
    return l_login(req)


def member_list(req):
    member = Member.objects.all()
    context = {'member': member}
    return render(req, 'joinwithmeapp/member_list.html', context)


def investor_list(req):
    investor = Investor.objects.all()
    context = {'investor': investor}
    return render(req, 'joinwithmeapp/investor_list.html', context)


def startup_list(req):
    startupseekers = Investor.objects.all()
    context = {'startupseekers': startupseekers}
    return render(req, 'joinwithmeapp/startup_list.html', context)
