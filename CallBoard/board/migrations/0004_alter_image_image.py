# Generated by Django 5.0.6 on 2024-09-08 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0003_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='board/files/images/'),
        ),
    ]
