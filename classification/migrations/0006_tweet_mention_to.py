# Generated by Django 4.0.3 on 2022-03-31 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classification', '0005_rename_f1_setting_f1_score_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='mention_to',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
