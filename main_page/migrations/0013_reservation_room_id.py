# Generated by Django 4.1.7 on 2023-03-19 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_page', '0012_gallery_is_visible_alter_reservation_phone_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='room_id',
            field=models.IntegerField(default=1),
        ),
    ]
