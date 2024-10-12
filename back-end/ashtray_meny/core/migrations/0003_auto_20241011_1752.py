# Generated by Django 5.1.2 on 2024-10-11 17:52

from django.db import migrations, models
import uuid

def generate_unique_ids(apps, schema_editor):
    User = apps.get_model('core', 'User')
    for user in User.objects.all():
        if not user.unique_id:  # Only update if the field is empty
            user.unique_id = uuid.uuid4()
            user.save()

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_user_id_user_about_user_user_address_and_more'),
    ]

    operations = [
        migrations.RunPython(generate_unique_ids),
    ]