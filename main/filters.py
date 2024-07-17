import django_filters
from django.db.models import Q
from django.forms.widgets import TextInput
from django.utils.html import format_html
from main.models import Child, Test


class LabeledTextInput(TextInput):
    def __init__(self, attrs=None, label_attrs=None):
        super().__init__(attrs)
        self.label_attrs = label_attrs or {}

    def render(self, name, value, attrs=None, renderer=None):
        input_html = super().render(name, value, attrs, renderer)
        return format_html('{input_html}', input_html=input_html)


class TestFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method='filter_by_tests',
        label='',
        widget=LabeledTextInput(
            attrs={'placeholder': 'Поиск', 'class': 'form-control'}
        )
    )

    def filter_by_tests(self, queryset, name, value):
        return queryset.filter(
            Q(test_code__icontains=value) |
            Q(user__user_code__icontains=value) |
            Q(child__child_code__icontains=value) |
            Q(result_test__icontains=value)
        )

    class Meta:
        model = Test
        fields = ['search']




class LabeledTextInput1(TextInput):
    def __init__(self, attrs=None, label_attrs=None):
        super().__init__(attrs)
        self.label_attrs = label_attrs or {}

    def render(self, name, value, attrs=None, renderer=None):
        input_html = super().render(name, value, attrs, renderer)
        return format_html('{input_html}', input_html=input_html)


class ChildFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        method='filter_by_childs',
        label='',
        widget=LabeledTextInput1(
            attrs={'placeholder': 'Поиск', 'class': 'form-control'}
        )
    )

    def filter_by_childs(self, queryset, name, value):
        return queryset.filter(
            Q(user__user_code__icontains=value) |
            Q(child_code__icontains=value) |
            Q(child_gender__icontains=value)
        )


    class Meta:
        model = Child
        fields = ['search']
