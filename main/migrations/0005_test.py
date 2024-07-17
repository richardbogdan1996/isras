# Generated by Django 5.0.4 on 2024-05-18 08:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_child'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_identifier', models.CharField(max_length=254)),
                ('test_code', models.CharField(max_length=254, null=True)),
                ('child_birthday', models.DateField(blank=True, null=True)),
                ('test_date', models.DateTimeField(auto_now_add=True)),
                ('result_test', models.TextField(blank=True, null=True)),
                ('child', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='child_tests', to='main.child')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_tests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
