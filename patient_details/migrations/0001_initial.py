# Generated by Django 5.0.3 on 2024-04-09 08:15

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='patient', max_length=100)),
                ('dob', models.DateField(default=django.utils.timezone.now)),
                ('phone_number', models.IntegerField(default='0')),
                ('age', models.IntegerField(default=0)),
                ('weight', models.IntegerField(default=0)),
                ('height', models.IntegerField(default=0)),
                ('sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=100)),
                ('hyper_tension_bp', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], default='no', max_length=100)),
                ('chest_pain', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], default='no', max_length=100)),
                ('palpitation', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], default='no', max_length=100)),
                ('surgery', models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], default='no', max_length=100)),
                ('any_other', models.TextField(default='', max_length=50)),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='recordings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record', models.FileField(upload_to='recordfile')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='patient_details.patient_details')),
            ],
        ),
    ]
