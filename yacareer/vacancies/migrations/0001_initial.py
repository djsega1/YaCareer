# Generated by Django 3.2.16 on 2022-12-23 05:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('groups', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupVacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('v_name', models.CharField(max_length=70, verbose_name='название')),
                ('text', models.CharField(max_length=1024, verbose_name='текст к посту')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_vacancy', to='groups.group', verbose_name='группа')),
            ],
            options={
                'verbose_name': 'вакансия',
                'verbose_name_plural': 'вакансии',
                'ordering': ['id'],
                'default_related_name': 'group_vacancy',
            },
        ),
    ]