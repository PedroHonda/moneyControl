# Generated by Django 3.0.2 on 2020-01-20 03:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Taxes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('tax_name', models.CharField(max_length=50)),
                ('value', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='StockSelling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('broker', models.CharField(max_length=30)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('asset_name', models.CharField(max_length=50)),
                ('quantity', models.FloatField()),
                ('value', models.FloatField()),
                ('total_value', models.FloatField()),
                ('total_value_received', models.FloatField()),
                ('comment', models.TextField(default='')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StockBuying',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('broker', models.CharField(max_length=30)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('asset_name', models.CharField(max_length=50)),
                ('quantity', models.FloatField()),
                ('value', models.FloatField()),
                ('total_value', models.FloatField()),
                ('total_value_paid', models.FloatField()),
                ('comment', models.TextField(default='')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='REIFSelling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('broker', models.CharField(max_length=30)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('asset_name', models.CharField(max_length=50)),
                ('quantity', models.FloatField()),
                ('value', models.FloatField()),
                ('total_value', models.FloatField()),
                ('total_value_received', models.FloatField()),
                ('comment', models.TextField(default='')),
                ('profit', models.FloatField(default=0.0)),
                ('darf', models.FloatField(default=0.0)),
                ('darf_paid', models.CharField(default='', max_length=5)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='REIFBuying',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('broker', models.CharField(max_length=30)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('asset_name', models.CharField(max_length=50)),
                ('quantity', models.FloatField()),
                ('value', models.FloatField()),
                ('total_value', models.FloatField()),
                ('total_value_paid', models.FloatField()),
                ('comment', models.TextField(default='')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FixedSelling',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('broker', models.CharField(max_length=30)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('asset_name', models.CharField(max_length=50)),
                ('quantity', models.FloatField()),
                ('value', models.FloatField()),
                ('total_value', models.FloatField()),
                ('total_value_received', models.FloatField()),
                ('comment', models.TextField(default='')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FixedBuying',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('broker', models.CharField(max_length=30)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('asset_name', models.CharField(max_length=50)),
                ('quantity', models.FloatField()),
                ('value', models.FloatField()),
                ('total_value', models.FloatField()),
                ('total_value_paid', models.FloatField()),
                ('comment', models.TextField(default='')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Current',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset_name', models.CharField(max_length=50)),
                ('quantity', models.FloatField()),
                ('mean_value', models.FloatField()),
                ('total', models.FloatField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
