# Generated by Django 4.2.3 on 2023-07-23 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0002_chat_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
