# Generated by Django 3.2.16 on 2022-12-19 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_profilelinks_is_contact'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profilelinks',
            name='is_contact',
        ),
    ]