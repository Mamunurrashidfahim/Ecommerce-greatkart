# Generated by Django 3.2.8 on 2021-11-30 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_alter_homeslider_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homeslider',
            name='images',
            field=models.ImageField(upload_to='homeslider'),
        ),
    ]