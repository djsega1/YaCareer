# Generated by Django 3.2.16 on 2022-12-18 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(blank=True, default='static_dev/img/user.png', null=True, upload_to='images/%Y/%m', verbose_name='фото'),
        ),
    ]
