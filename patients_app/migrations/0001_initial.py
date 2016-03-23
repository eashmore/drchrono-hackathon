# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-23 01:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Allergies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=200)),
                ('notes', models.TextField(blank=True)),
                ('reaction', models.CharField(blank=True, max_length=200)),
                ('status', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField()),
                ('payer_name', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Medication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('daw', models.BooleanField()),
                ('name', models.CharField(max_length=200)),
                ('prn', models.BooleanField()),
                ('date_prescribed', models.DateField(blank=True, null=True)),
                ('date_started_taking', models.DateField(blank=True, null=True)),
                ('date_stopped_taking', models.DateField(blank=True, null=True)),
                ('dispense_quantity', models.FloatField(blank=True, null=True)),
                ('dosage_quantity', models.FloatField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
                ('frequency', models.CharField(blank=True, max_length=200)),
                ('number_refills', models.IntegerField(blank=True, null=True)),
                ('order_status', models.CharField(blank=True, max_length=200)),
                ('status', models.CharField(blank=True, max_length=200)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=200)),
                ('middle_name', models.CharField(blank=True, max_length=200)),
                ('last_name', models.CharField(blank=True, max_length=200)),
                ('address', models.CharField(blank=True, max_length=200)),
                ('email', models.CharField(blank=True, max_length=200)),
                ('home_phone', models.CharField(blank=True, max_length=14)),
                ('cell_phone', models.CharField(blank=True, max_length=14)),
                ('city', models.CharField(blank=True, max_length=200)),
                ('emergency_contact_name', models.CharField(blank=True, max_length=200)),
                ('emergency_contact_phone', models.CharField(blank=True, max_length=200)),
                ('emergency_contact_relation', models.CharField(blank=True, max_length=200)),
                ('employer', models.CharField(blank=True, max_length=200)),
                ('employer_city', models.CharField(blank=True, max_length=200)),
                ('employer_address', models.CharField(blank=True, max_length=200)),
                ('employer_state', models.CharField(blank=True, max_length=200)),
                ('employer_zip_code', models.CharField(blank=True, max_length=200)),
                ('primary_care_physician', models.CharField(blank=True, max_length=200)),
                ('zip_code', models.CharField(blank=True, max_length=5)),
                ('state', models.CharField(blank=True, max_length=2)),
                ('social_security_number', models.CharField(blank=True, max_length=20)),
                ('responsible_party_name', models.CharField(blank=True, max_length=200)),
                ('responsible_party_phone', models.CharField(blank=True, max_length=14)),
                ('responsible_party_relation', models.CharField(blank=True, max_length=200)),
                ('responsible_party_email', models.CharField(blank=True, max_length=200)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_changed', models.DateField(blank=True, null=True)),
                ('date_diagnosis', models.DateField(blank=True, null=True)),
                ('date_onset', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True)),
                ('name', models.CharField(blank=True, max_length=200)),
                ('notes', models.TextField(blank=True)),
                ('status', models.CharField(blank=True, max_length=200)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients_app.Patient')),
            ],
        ),
        migrations.AddField(
            model_name='medication',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients_app.Patient'),
        ),
        migrations.AddField(
            model_name='insurance',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients_app.Patient'),
        ),
    ]