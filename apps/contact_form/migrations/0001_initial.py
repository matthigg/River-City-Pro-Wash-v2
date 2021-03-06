# Generated by Django 2.1.11 on 2019-09-07 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('address', models.CharField(max_length=200, null=True)),
                ('email', models.CharField(max_length=64)),
                ('phone', models.CharField(max_length=24)),
                ('message', models.TextField(max_length=500)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('ip_address', models.GenericIPAddressField(null=True)),
            ],
            options={
                'verbose_name_plural': 'Contact Form',
            },
        ),
    ]
