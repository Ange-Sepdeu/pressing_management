# Generated by Django 5.0.6 on 2024-09-08 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_rename_description_contact_message_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='message',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='name',
        ),
        migrations.AddField(
            model_name='contact',
            name='service_rate',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
