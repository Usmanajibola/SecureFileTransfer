# Generated by Django 4.0.1 on 2022-02-03 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0002_myuser_alter_file_user_alter_link_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='date_created',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='link',
            name='date_created',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
