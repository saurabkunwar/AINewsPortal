# Generated by Django 4.0.5 on 2022-06-21 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backendservice', '0002_alter_article_published_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='published_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]