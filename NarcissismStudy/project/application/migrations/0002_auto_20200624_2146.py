# Generated by Django 2.2.13 on 2020-06-24 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='selfie',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
