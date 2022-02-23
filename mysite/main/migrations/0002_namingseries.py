# Generated by Django 4.0.2 on 2022-02-20 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NamingSeries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serie', models.CharField(max_length=10)),
                ('type', models.CharField(choices=[('default', 'Default'), ('in', 'In'), ('out', 'Out')], default='default', max_length=10, null=True)),
                ('number', models.IntegerField(default=1, max_length=10)),
                ('fill', models.IntegerField(default=4, max_length=1)),
            ],
        ),
    ]