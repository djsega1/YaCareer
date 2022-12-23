# Generated by Django 3.2.16 on 2022-12-23 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='сервис')),
                ('bootstrap_icon', models.CharField(help_text='https://icons.bootstrap-5.ru/icons/Найдите на данном сайте нужную картинку и впишите название(например: bi bi-telegram)', max_length=150, verbose_name='иконка')),
                ('is_contact', models.BooleanField(default=False, verbose_name='контакт')),
            ],
            options={
                'verbose_name': 'сервис',
                'verbose_name_plural': 'сервисы',
                'default_related_name': 'service',
            },
        ),
    ]
