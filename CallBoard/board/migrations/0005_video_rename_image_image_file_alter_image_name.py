# Generated by Django 5.0.6 on 2024-09-08 13:04

import embed_video.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0004_alter_image_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('url', embed_video.fields.EmbedVideoField()),
            ],
        ),
        migrations.RenameField(
            model_name='image',
            old_name='image',
            new_name='file',
        ),
        migrations.AlterField(
            model_name='image',
            name='name',
            field=models.CharField(max_length=150),
        ),
    ]
