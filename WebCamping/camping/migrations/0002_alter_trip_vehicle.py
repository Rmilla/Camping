# Generated by Django 5.0.6 on 2024-05-17 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('camping', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='vehicle',
            field=models.CharField(max_length=200),
        ),
    ]
