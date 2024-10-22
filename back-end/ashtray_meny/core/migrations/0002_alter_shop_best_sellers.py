# Generated by Django 5.1.2 on 2024-10-22 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='best_sellers',
            field=models.ManyToManyField(blank=True, related_name='shop_best_sellers', to='core.product'),
        ),
    ]
