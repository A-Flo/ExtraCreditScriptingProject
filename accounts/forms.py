from django import forms
from .models import (
    DNSUser,
    Administrator,
    Permission,
)

class AdministratorForm(forms.ModelForm):
    class Meta:
        model = Administrator
        fields = (
        'user',
        )

class PermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = (
        'name',
        )
