# Generated by Django 3.2.16 on 2023-03-28 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boilerplate_app', '0003_auto_20210907_0643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
