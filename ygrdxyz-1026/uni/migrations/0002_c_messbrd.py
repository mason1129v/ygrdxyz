# Generated by Django 4.0 on 2023-10-25 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uni', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='c_messbrd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MID', models.CharField(max_length=100, verbose_name='使用者編號')),
                ('MCont', models.CharField(max_length=1000, verbose_name='內容')),
                ('MDATE', models.DateTimeField()),
            ],
        ),
    ]