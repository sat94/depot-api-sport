# Generated by Django 4.0.6 on 2022-10-04 13:08

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('nom', models.CharField(max_length=20)),
                ('prenom', models.CharField(max_length=20)),
                ('slug', models.SlugField(max_length=20)),
                ('email', models.EmailField(max_length=30)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photo')),
                ('adresse', models.CharField(max_length=200)),
                ('CodePostal', models.IntegerField(blank=True, null=True)),
                ('commercial', models.BooleanField(default=False)),
                ('ville', models.CharField(max_length=20)),
                ('permission', models.CharField(choices=[('Commercial', 'Commercial'), ('Partenaire', 'Partenaire'), ('Responsable', 'Responsable')], max_length=15)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=20)),
                ('description', models.CharField(max_length=200)),
            ],
            options={
                'ordering': ['slug'],
            },
        ),
        migrations.CreateModel(
            name='partenaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=20)),
                ('actif', models.BooleanField(default=True)),
                ('ville', models.CharField(max_length=15)),
                ('description', models.CharField(max_length=70)),
                ('numberPhone', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')])),
                ('photo', models.ImageField(blank=True, null=True, upload_to='ville')),
                ('option', models.ManyToManyField(blank=True, to='accounts.option')),
                ('resp', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='structure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actif', models.BooleanField(default=True)),
                ('slug', models.SlugField(max_length=20)),
                ('nom', models.CharField(max_length=20)),
                ('adresse', models.CharField(max_length=100)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='salle')),
                ('numberPhone', models.CharField(max_length=10, unique=True, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{8,15}$')])),
                ('piscine', models.BooleanField(default=False)),
                ('haman', models.BooleanField(default=False)),
                ('sauna', models.BooleanField(default=False)),
                ('membre', models.IntegerField(default=0)),
                ('option', models.ManyToManyField(blank=True, to='accounts.option')),
                ('part', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.partenaire')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='partenaire',
            name='salle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.structure'),
        ),
    ]