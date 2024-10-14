# Generated by Django 4.2.1 on 2023-06-08 17:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Asignatura",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nombre", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Asignacion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "tipo_evaluacion",
                    models.CharField(
                        choices=[
                            ("Examen", "Examen"),
                            ("Trabajo", "Trabajo"),
                            ("Parcial", "Parcial"),
                        ],
                        max_length=100,
                    ),
                ),
                ("descripcion", models.TextField()),
                (
                    "asignatura",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="student_dashboard_app.asignatura",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="asignacion",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("tipo_evaluacion__in", ["Examen", "Trabajo", "Parcial"])
                ),
                name="constraint_tipo_evaluacion",
            ),
        ),
    ]
