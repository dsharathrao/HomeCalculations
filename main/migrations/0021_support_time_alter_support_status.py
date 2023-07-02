# Generated by Django 4.1 on 2022-08-26 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_rename_message_support_description_support_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='support',
            name='Time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='support',
            name='Status',
            field=models.CharField(choices=[('new', 'NEW'), ('resolved', 'RESOLVED'), ('inprogress', 'INPROGRESS'), ('cancelled', 'CANCELLED'), ('closed', 'CLOSED')], default='new', max_length=100),
        ),
    ]
