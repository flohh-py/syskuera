# Generated by Django 4.0.2 on 2022-02-24 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_stockentryline_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stockentry',
            options={'ordering': ['-code']},
        ),
    ]
