# Generated by Django 4.0.3 on 2022-03-25 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classification', '0002_rename_threshold_setting_threshold_max_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='is_active',
            field=models.BooleanField(default=0, null=True),
        ),
    ]
