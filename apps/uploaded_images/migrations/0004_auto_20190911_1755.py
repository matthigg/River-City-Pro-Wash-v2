# Generated by Django 2.1.11 on 2019-09-11 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploaded_images', '0003_auto_20190911_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedimages',
            name='After_Picture_Size_kB',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='uploadedimages',
            name='Before_Picture_Dimension',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='uploadedimages',
            name='Before_Picture_Size_kB',
            field=models.IntegerField(null=True),
        ),
    ]
