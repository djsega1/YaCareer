# Generated by Django 3.2.16 on 2022-12-21 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_followsu2u_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermedia',
            name='file',
            field=models.FileField(unique=True, upload_to='files/', verbose_name='файл'),
        ),
    ]
