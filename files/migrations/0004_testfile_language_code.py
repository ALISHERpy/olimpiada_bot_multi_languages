# Generated by Django 3.2.9 on 2023-10-11 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0003_auto_20230911_1804'),
    ]

    operations = [
        migrations.AddField(
            model_name='testfile',
            name='language_code',
            field=models.CharField(default='', max_length=4),
            preserve_default=False,
        ),
    ]
