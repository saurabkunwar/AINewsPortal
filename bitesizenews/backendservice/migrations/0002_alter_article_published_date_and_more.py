# Generated by Django 4.0.5 on 2022-06-21 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendservice', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='published_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='summarization',
            field=models.TextField(blank=True, null=True),
        ),
    ]
