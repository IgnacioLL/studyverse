# Generated by Django 4.2.1 on 2023-06-18 17:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("student_dashboard_app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="asignatura",
            name="usuario",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
