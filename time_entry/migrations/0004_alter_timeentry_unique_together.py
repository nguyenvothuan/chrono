# Generated by Django 3.2.16 on 2023-04-02 02:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_alter_account_startdate'),
        ('time_entry', '0003_alter_timeentry_account'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='timeentry',
            unique_together={('account', 'date')},
        ),
    ]
