# Generated by Django 4.1.7 on 2023-03-14 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hospital_api', '0003_remove_treatment_end_date_remove_treatment_patient_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TreatmentApplied',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_applied', models.DateTimeField(auto_now_add=True)),
                ('drug', models.CharField(max_length=255)),
                ('dosage', models.FloatField()),
                ('assistant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_api.assistant')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_api.patient')),
                ('treatment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital_api.treatment')),
            ],
        ),
    ]
