# Generated by Django 5.0.6 on 2024-09-10 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_geolocation'),
    ]

    operations = [
        migrations.AddField(
            model_name='geolocation',
            name='location_type',
            field=models.CharField(choices=[('pickup', 'Pickup'), ('delivery', 'Deliver Dressing')], default='delivery', max_length=10),
        ),
    ]
