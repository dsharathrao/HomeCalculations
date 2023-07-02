# Generated by Django 4.1 on 2022-08-21 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_shopping_proof'),
    ]

    operations = [
        migrations.CreateModel(
            name='Medical',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('HospitalName', models.CharField(max_length=100)),
                ('DiseaseName', models.CharField(blank=True, max_length=100, null=True)),
                ('Prescription', models.FileField(blank=True, null=True, upload_to='Medical/Prescription/')),
                ('Time', models.DateField(blank=True, null=True)),
                ('Amount', models.IntegerField()),
                ('Proof', models.FileField(blank=True, null=True, upload_to='Medical/Bills/')),
            ],
            options={
                'verbose_name_plural': 'Medical',
            },
        ),
    ]