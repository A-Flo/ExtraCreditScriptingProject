from django.shortcuts import render
from .forms import PermissionForm
from .models import Permission

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
