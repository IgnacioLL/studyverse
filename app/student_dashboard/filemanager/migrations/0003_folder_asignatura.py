# Generated by Django 4.2.1 on 2023-06-18 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("student_dashboard_app", "0002_asignatura_usuario"),
        ("filemanager", "0002_remove_folder_asignatura"),
    ]

    operations = [
        migrations.AddField(
            model_name="folder",
            name="asignatura",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="asignatura",
                to="student_dashboard_app.asignatura",
            ),
            preserve_default=False,
        ),
    ]
