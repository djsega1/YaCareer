# Generated by Django 3.2.16 on 2022-12-18 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='upload',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/%Y/%m', verbose_name='фото'),
        ),
    ]
