# Generated by Django 4.0.6 on 2022-10-14 22:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_alter_myuser_permission'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='partenaires',
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='structures',
        ),
    ]
