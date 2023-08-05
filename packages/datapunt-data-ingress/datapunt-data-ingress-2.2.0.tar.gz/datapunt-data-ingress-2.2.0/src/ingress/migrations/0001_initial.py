# Generated by Django 2.2.16 on 2020-11-04 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="IngressQueue",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("endpoint", models.TextField()),
                ("raw_data", models.TextField()),
                ("parse_started", models.DateTimeField(null=True)),
                ("parse_succeeded", models.DateTimeField(null=True)),
                ("parse_failed", models.DateTimeField(null=True)),
                ("parse_fail_info", models.TextField(null=True)),
            ],
        ),
    ]
