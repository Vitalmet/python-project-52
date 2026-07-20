from django import forms
from django_filters import FilterSet, ChoiceFilter, BooleanFilter, ModelMultipleChoiceFilter
from django_filters.filters import ModelChoiceFilter
from django.utils.translation import gettext_lazy as _
from .models import Task, Status, Label
from django.contrib.auth.models import User


class TaskFilter(FilterSet):
    status = ModelChoiceFilter(
        field_name='status',
        label=_('Status'),
        queryset=Status.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    executor = ModelChoiceFilter(
        field_name='executor',
        label=_('Executor'),
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    labels = ModelMultipleChoiceFilter(
        field_name='labels',
        label=_('Label'),
        queryset=Label.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'})
    )
    self_tasks = BooleanFilter(
        field_name='author',
        label=_('Only my tasks'),
        method='filter_self_tasks',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def filter_self_tasks(self, queryset, name, value):
        if value:
            user = self.request.user
            if user.is_authenticated:
                return queryset.filter(author=user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'self_tasks']
