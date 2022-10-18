# Generated by Django 4.0.6 on 2022-10-04 14:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='photo',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=True, null=True, quality=75, scale=0.5, size=[300, 500], upload_to='photo'),
        ),
        migrations.AlterField(
            model_name='partenaire',
            name='photo',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=True, null=True, quality=75, scale=0.5, size=[500, 300], upload_to='ville'),
        ),
        migrations.AlterField(
            model_name='partenaire',
            name='resp',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='responsable', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='structure',
            name='photo',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=True, null=True, quality=75, scale=0.5, size=[500, 300], upload_to='salle'),
        ),
    ]