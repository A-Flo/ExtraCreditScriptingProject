from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login
from accounts.models import DNSUser, Administrator, Permission
from django.contrib.auth.models import User

from .forms import (
    RegisterationForm,
    LoginForm
)


class Login(View):

    def get(self, request, *a, **kw):
        context = dict()
        context["form"] = LoginForm
        return render(request, "accounts/login.html", context)

    def post(self, request, *a, **kw):
        form = LoginForm(request.POST)
        data = dict()
        u = User.objects.filter(username = request.POST["username"])
        if not u:
            data["not_user"] = 1
            return render(request, "accounts/error_page.html", data)
        if form.is_valid:
            user = authenticate(
                username=request.POST.get('username', None),
                password=request.POST.get('password', None))
            if user is not None:
                if user.is_active:
                    login(request, user)
                    user.is_authenticated = True
                    return redirect(reverse_lazy("default_users"))
            else:
                data["invalid"] = True
                return render(request, "accounts/error_page.html")
        else:
            data["invalid"] = True

        data["form"] = LoginForm
        return render(request, 'accounts/login.html', data)


class Registeration(View):

    def get(self, request, *a, **kw):
        context = dict()
        context["form"] = RegisterationForm
        return render(request, "accounts/registeration.html", context)

    def post(self, request, *a, **kw):
        form = RegisterationForm(request.POST)
        context = dict()
        if form.is_valid:
            form.save()
            if request.POST.get("admin", None):
                print "admin create"
                dnsuser = {
                    "user": User.objects.get(username = request.POST["username"])
                }
                a = Administrator.objects.get_or_create(**dnsuser)
                a[0].permissions.add(Permission.objects.get(id = 1).id)
            else:
                dnsuser = {
                    "user": User.objects.get(username = request.POST["username"])
                }
                a = DNSUser.objects.get_or_create(**dnsuser)
            if not request.POST.get("dont_login"):
                user = authenticate(
                    username=request.POST.get('username', None),
                    password=request.POST.get('password', None))
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        user.is_authenticated = True
                        return redirect(reverse_lazy("default_users"))
            return redirect(reverse_lazy("default_users"))
        else:
            context["invalid"] = True
            return render(request, "accounts/login.html", context)
