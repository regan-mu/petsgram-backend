# Generated by Django 5.1.1 on 2024-09-17 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0003_alter_follow_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
