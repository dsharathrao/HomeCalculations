# Generated by Django 4.1 on 2022-08-26 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='ProfilePic',
            field=models.ImageField(default='default.png', upload_to='UserProfilePics/'),
        ),
    ]
