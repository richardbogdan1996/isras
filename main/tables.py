from datetime import timedelta
from django_tables2 import Table, Column, paginators
from main.models import Test, Child
from django.utils.formats import date_format
from django.urls import reverse
from django.utils.html import format_html


class ResultTestTable(Table):

    user_code = Column(accessor='user.user_code', verbose_name='Код пользователя')
    child = Column(accessor='child.child_code', verbose_name='Код ребенка')
    test_code = Column(accessor='test_code', verbose_name='Код теста')
    child_birthday = Column(accessor='child_birthday', verbose_name='Дата рождения ребенка')
    result_test = Column(accessor='result_test', verbose_name='Результат теста')
    test_date = Column(accessor='test_date', verbose_name='Дата создания')

    class Meta:
        model = Test
        fields = ('test_code', 'user_code', 'child', 'child_birthday', 'result_test','test_date')
        per_page = 7
        paginator = paginators.LazyPaginator
        page_kwarg = 'page'  # Установка имени параметра страницы
        attrs = {"class": "table table-bordered table-auto table-sm", "id": "blacklist-table"}

    def render_test_date(self, value, record):
        value_with_offset = value + timedelta(hours=3)
        return date_format(value_with_offset, "d.m.Y H:i")

    def render_child_birthday(self, value, record):
        return date_format(value, "d.m.Y")




class ResultChildTable(Table):
    child_code = Column(accessor='child_code', verbose_name='Код ребенка')
    user_code = Column(accessor='user.user_code', verbose_name='Код родителя')
    child_birthday_date = Column(accessor='child_birthday_date', verbose_name='Дата рождения')
    child_gender = Column(accessor='child_gender', verbose_name='Пол')
    test_1 = Column(accessor='child_code', verbose_name='Тест-1', orderable=False)
    test_2 = Column(accessor='child_code', verbose_name='Тест-2', orderable=False)
    test_3 = Column(accessor='child_code', verbose_name='Тест-3', orderable=False)
    child_view = Column(accessor='child_code', verbose_name='', orderable=False)
    created_at = Column(accessor='created_at', verbose_name='Дата создания')

    class Meta:
        model = Child
        fields = ('child_code', 'user_code', 'child_birthday_date', 'child_gender', 'test_1', 'test_2', 'test_3', 'child_view', 'created_at',)
        per_page = 7
        paginator = paginators.LazyPaginator
        page_kwarg = 'page'  # Установка имени параметра страницы
        attrs = {"class": "table table-bordered table-auto table-sm", "id": "blacklist-table"}

    def render_test_1(self, value, record):
        url = reverse('test1', args=[record.child_code])
        return format_html('<a href="{}">{}</a>', url, 'Начать тест')

    def render_test_2(self, value, record):
        url = reverse('test2', args=[record.child_code])
        return format_html('<a href="{}">{}</a>', url, 'Начать тест')

    def render_test_3(self, value, record):
        url = reverse('test3', args=[record.child_code])
        return format_html('<a href="{}">{}</a>', url, 'Начать тест')


    def render_child_view(self, value, record):
        url = reverse('child_view', args=[record.child_code])
        return format_html('<a href="{}">{}</a>', url, 'Просмотр >')



    def render_child_birthday_date(self, value, record):
        return date_format(value, "d.m.Y")


    def render_created_at(self, value, record):
        value_with_offset = value + timedelta(hours=3)
        return date_format(value_with_offset, "d.m.Y H:i")