# Generated by Django 3.2.19 on 2024-09-08 10:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_customuser_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='pressing_photos/')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_file', models.FileField(upload_to='pressing_videos/')),
            ],
        ),
        migrations.CreateModel(
            name='PressingProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('services_offered', models.TextField()),
                ('pricing', models.TextField()),
                ('about_us', models.TextField()),
                ('approved', models.BooleanField(default=False)),
                ('photos', models.ManyToManyField(blank=True, to='orders.Photo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('videos', models.ManyToManyField(blank=True, to='orders.Video')),
            ],
        ),
    ]
