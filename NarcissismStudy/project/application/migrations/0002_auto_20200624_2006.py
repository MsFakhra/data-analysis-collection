# Generated by Django 2.2.12 on 2020-06-24 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.BigIntegerField(verbose_name='post_id')),
                ('posted_on', models.DateTimeField(verbose_name='posted_on')),
                ('owner', models.CharField(max_length=200)),
                ('is_comment', models.BooleanField(verbose_name='is_comment')),
                ('sentiment', models.CharField(max_length=200, verbose_name='sentiment')),
                ('sscore', models.FloatField(verbose_name='sscore')),
                ('tag_used', models.BooleanField(default=False, verbose_name='tag_used')),
                ('likes', models.IntegerField(verbose_name='likes')),
                ('caption', models.TextField(verbose_name='caption')),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.BigIntegerField(verbose_name='post_id')),
                ('posted_on', models.DateTimeField(verbose_name='posted_on')),
                ('selfie', models.BooleanField(default=False, verbose_name='selfie')),
                ('person', models.TextField(verbose_name='person')),
                ('image_path', models.TextField(verbose_name='image_path')),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(verbose_name='user_id')),
                ('instagram', models.CharField(max_length=200, verbose_name='instagram')),
                ('posted_on', models.DateTimeField(verbose_name='posted_on')),
                ('post_url', models.TextField(verbose_name='post_url')),
                ('hashtags', models.TextField(verbose_name='hashtags')),
                ('mentions', models.TextField(verbose_name='mentions')),
                ('tagged_users', models.TextField(verbose_name='tagged_users')),
                ('is_video', models.BooleanField(default=False, verbose_name='is_video')),
                ('likes', models.BigIntegerField(verbose_name='likes')),
                ('caption', models.TextField(verbose_name='caption')),
            ],
        ),
        migrations.AddField(
            model_name='users',
            name='state',
            field=models.TextField(default='pending', verbose_name='state'),
        ),
    ]