# Generated by Django 3.2.16 on 2023-03-27 22:45

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('positionTitle', models.CharField(blank=True, default='', max_length=100)),
                ('startDate', models.DateField(default=datetime.datetime(2023, 3, 27, 18, 45, 48, 76685))),
                ('isManager', models.BooleanField(default=False)),
                ('manager', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='account.account')),
                ('user', models.ForeignKey(blank=True, default=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
