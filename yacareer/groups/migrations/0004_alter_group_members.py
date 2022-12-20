# Generated by Django 3.2.16 on 2022-12-20 15:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groups', '0003_auto_20221220_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(limit_choices_to='участники', related_name='GroupMembers', related_query_name='members', to=settings.AUTH_USER_MODEL),
        ),
    ]
