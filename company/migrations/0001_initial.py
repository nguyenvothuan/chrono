# Generated by Django 3.2.16 on 2023-03-27 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=50)),
            ],
        ),
    ]
