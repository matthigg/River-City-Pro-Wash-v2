# Generated by Django 2.1.11 on 2019-09-06 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact_form', '0005_contactform_ip_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactform',
            name='ip_address_string',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
