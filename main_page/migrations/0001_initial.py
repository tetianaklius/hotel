# Generated by Django 4.1.7 on 2023-03-26 23:43

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import main_page.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('sup_desc', models.TextField(blank=True, max_length=2000)),
                ('point_text_1', models.TextField(max_length=200)),
                ('point_text_2', models.TextField(max_length=200)),
                ('point_text_3', models.TextField(max_length=200)),
                ('point_text_4', models.TextField(blank=True, max_length=200)),
                ('point_text_5', models.TextField(blank=True, max_length=200)),
                ('inf_desc', models.TextField(blank=True, max_length=2000)),
                ('is_visible', models.BooleanField(default=True)),
                ('photo', models.ImageField(upload_to='about')),
            ],
        ),
        migrations.CreateModel(
            name='CategoryRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=100, unique=True)),
                ('position', models.SmallIntegerField(unique=True)),
                ('is_visible', models.BooleanField(default=True)),
                ('persons', models.SmallIntegerField(default=1)),
            ],
            options={
                'ordering': ('position',),
            },
        ),
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, max_length=100)),
                ('sub_title', models.TextField(blank=True, max_length=500)),
                ('phone_title', models.TextField(blank=True, max_length=20)),
                ('phone', models.TextField(max_length=20)),
                ('phone_add', models.TextField(blank=True, max_length=20)),
                ('address_title', models.TextField(blank=True, max_length=50)),
                ('address', models.TextField(max_length=200)),
                ('email_title', models.TextField(blank=True, max_length=10)),
                ('email', models.TextField(blank=True, max_length=50)),
                ('email_add', models.TextField(blank=True, max_length=50)),
                ('socials', models.TextField(blank=True, max_length=100)),
                ('add_information', models.TextField(blank=True, max_length=500)),
                ('open_hours_title', models.TextField(blank=True, max_length=20)),
                ('open_days_1', models.TextField(max_length=150)),
                ('open_hours_1', models.TextField(max_length=50)),
                ('open_days_2', models.TextField(blank=True, max_length=150)),
                ('open_hours_2', models.TextField(blank=True, max_length=50)),
                ('day_off_title', models.TextField(blank=True, max_length=15)),
                ('day_off', models.TextField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='gallery')),
                ('desc', models.TextField(blank=True, max_length=250)),
                ('inn_short_desc', models.CharField(max_length=30)),
                ('season', models.SmallIntegerField()),
                ('is_visible', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('last_name', models.CharField(blank=True, max_length=50)),
                ('phone', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message='Помилка в номері телефону', regex='^\\+?3?8?0\\d{2}[- ]?(\\d[- ]?){7}$')])),
                ('user_email', models.CharField(blank=True, max_length=100, null=True)),
                ('persons', models.IntegerField(blank=True, default=2, null=True)),
                ('message', models.TextField(blank=True, max_length=250)),
                ('room_id', models.IntegerField(blank=True, null=True)),
                ('room_price', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('user_id', models.IntegerField(blank=True, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('date_processing', models.DateField(auto_now=True)),
                ('is_processed', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=100, unique=True)),
                ('desc', models.TextField(blank=True, max_length=3000)),
                ('position', models.SmallIntegerField(unique=True)),
                ('is_visible', models.BooleanField(default=True)),
                ('persons', models.SmallIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('price_comment', models.TextField(blank=True, max_length=100)),
                ('price_1person', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('price_2person', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('price_3person', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('price_pets', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('special_offer', models.BooleanField(default=False)),
                ('title_photo', models.ImageField(upload_to='title_photo')),
                ('inn_number', models.SmallIntegerField(blank=True, default=1)),
                ('for_single', models.BooleanField(default=False)),
                ('with_pets', models.BooleanField(default=False)),
                ('first_floor', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='main_page.categoryroom')),
            ],
            options={
                'ordering': ('position',),
            },
        ),
        migrations.CreateModel(
            name='RoomPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to=main_page.models.RoomPhoto.get_file_name)),
                ('position', models.SmallIntegerField(unique=True)),
                ('desc', models.TextField(blank=True, max_length=250)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_photo', to='main_page.room')),
            ],
            options={
                'ordering': ('room', 'position'),
            },
        ),
    ]
