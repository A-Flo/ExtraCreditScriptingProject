from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import PermissionForm, AdministratorForm
from .models import Permission, DNSUser, Administrator
from django.core.urlresolvers import reverse
from register.forms import RegisterationForm

def main(request):
    return render(request, "base.html")

def render_permission_form(request):
    data = dict()
    return render(request, "accounts/permission_form.html", data)

def create_permission(request):
    form = PermissionForm(request.POST)
    print form
    if form.is_valid():
        print 'valid'
        form.save()
    data = dict()
    data["permissions"] = Permission.objects.all()
    return render(request, "accounts/permission_form.html", data)

def render_default_users(request):
    u = request.user.id
    data = dict()
    admin = Administrator.objects.filter(user_id = u)
    print admin
    if admin:
        data["default_users"] = DNSUser.objects.all()
        data["form"] = RegisterationForm
        data["admin_users"] = Administrator.objects.all()
        return render(request, "accounts/default_users.html", data)
    else:
        data["not_admin"] = 1
        return render(request, "accounts/error_page.html", data)

def delete_dnsusers(request):
    objectid = request.POST["objectid"]
    DNSUser.objects.get(id = objectid).delete()
    return redirect(reverse("default_users"))

def confirm_delete(request):
    if request.method == "POST":
        objectid = request.POST["objectid"]
        user = DNSUser.objects.get(id = objectid)
        return render(request, "accounts/confirm_delete.html", {"user": user})

def render_administrator_form(request):
    form = RegisterationForm
    data = dict()
    data["form"] = form
    return render(request, "accounts/administrator_registeration.html", data)

def user_to_admin(request):
    user_id = request.POST.get("user_id")
    dnsuser = DNSUser.objects.get(user_id = user_id)
    user = User.objects.get(username = dnsuser.user.username)
    dnsuser.delete()
    admin_user = Administrator.objects.create(user = user)
    return redirect(reverse("default_users"))
