# Generated by Django 2.2.12 on 2020-06-25 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0006_auto_20200625_0854'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='instagram',
            field=models.CharField(max_length=200, null=True, verbose_name='instagram'),
        ),
    ]
