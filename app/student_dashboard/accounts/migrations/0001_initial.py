# Generated by Django 4.2.1 on 2023-06-08 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        help_text="Ex: example@example.com",
                        max_length=255,
                        unique=True,
                        verbose_name="Email Address",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(default=False, verbose_name="Staff status"),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="Active")),
                (
                    "date_joined",
                    models.DateTimeField(auto_now_add=True, verbose_name="Date Joined"),
                ),
                (
                    "last_updated",
                    models.DateTimeField(auto_now=True, verbose_name="Last Updated"),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        related_name="custom_user_set",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        related_name="custom_user_set",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
