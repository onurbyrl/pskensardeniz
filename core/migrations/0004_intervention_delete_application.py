# Generated by Django 4.2 on 2025-04-14 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_application_description_en_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Intervention',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=124, null=True)),
                ('title_tr', models.CharField(blank=True, max_length=124, null=True)),
                ('title_en', models.CharField(blank=True, max_length=124, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('description_tr', models.TextField(blank=True, null=True)),
                ('description_en', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='intervention_images/')),
            ],
            options={
                'verbose_name': 'Intervention',
                'verbose_name_plural': 'Interventions',
            },
        ),
        migrations.DeleteModel(
            name='Application',
        ),
    ]
