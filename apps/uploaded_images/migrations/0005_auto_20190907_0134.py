# Generated by Django 2.1.11 on 2019-09-07 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploaded_images', '0004_uploadedimages_img_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uploadedimages',
            old_name='img_file',
            new_name='img_after',
        ),
        migrations.RemoveField(
            model_name='uploadedimages',
            name='img_name',
        ),
        migrations.AddField(
            model_name='uploadedimages',
            name='img_before',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
