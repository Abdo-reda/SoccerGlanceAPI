# Generated by Django 4.1.7 on 2023-05-08 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_user_first_name_remove_user_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='target_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
