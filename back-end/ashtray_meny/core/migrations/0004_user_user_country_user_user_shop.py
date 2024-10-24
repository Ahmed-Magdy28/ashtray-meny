# Generated by Django 5.1.2 on 2024-10-22 19:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_shop_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='user_shop',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.shop'),
        ),
    ]
