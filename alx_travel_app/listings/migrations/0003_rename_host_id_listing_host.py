# Generated by Django 5.1.5 on 2025-02-06 17:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0002_alter_booking_table_alter_listing_table_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='host_id',
            new_name='host',
        ),
    ]
