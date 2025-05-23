# Generated by Django 4.2 on 2025-04-16 21:23

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_article_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='text_en',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='text_tr',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='title_en',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='title_tr',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
