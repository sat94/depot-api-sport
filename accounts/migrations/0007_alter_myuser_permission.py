# Generated by Django 4.0.6 on 2022-10-10 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_option_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='permission',
            field=models.CharField(blank=True, choices=[('Commercial', 'Commercial'), ('Partenaire', 'Partenaire'), ('Responsable', 'Responsable')], max_length=15, null=True),
        ),
    ]