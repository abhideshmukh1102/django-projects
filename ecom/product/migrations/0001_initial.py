# Generated by Django 5.0.3 on 2024-05-05 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ProductTable",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("price", models.DecimalField(decimal_places=3, max_digits=10)),
                ("description", models.CharField(max_length=100)),
                ("quantity", models.PositiveIntegerField(default=0)),
                ("category", models.CharField(max_length=100)),
                ("image", models.ImageField(upload_to="image")),
                ("is_available", models.BooleanField()),
            ],
        ),
    ]