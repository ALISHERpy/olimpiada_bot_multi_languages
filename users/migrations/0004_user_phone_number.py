# Generated by Django 3.2.9 on 2023-09-12 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_rm_unused_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=13),
        ),
    ]
