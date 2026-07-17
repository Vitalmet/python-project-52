from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Status, Task


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=150,
        required=False,
        label=_('First name'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        label=_('Last name'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        max_length=150,
        label=_('Username'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label=_('Confirm Password'),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError(_('User with this username already exists.'))
        return username


class CustomUserChangeForm(UserChangeForm):
    password = None

    first_name = forms.CharField(
        max_length=150,
        required=False,
        label=_('First name'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        label=_('Last name'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        max_length=150,
        label=_('Username'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise ValidationError(_('User with this username already exists.'))
        return username


class StatusForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        label=_('Name'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Status
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Status.objects.filter(name=name).exists():
            raise ValidationError(_('Status with this name already exists.'))
        return name


class TaskForm(forms.ModelForm):
    name = forms.CharField(
        max_length=150,
        label=_('Name'),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        label=_('Description'),
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
    )
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        label=_('Status'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label=_('Executor'),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Task.objects.filter(name=name).exists():
            raise ValidationError(_('Task with this name already exists.'))
        return name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['name'].validators = []
