# Generated by Django 2.1.11 on 2019-09-12 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploaded_images', '0009_auto_20190912_1436'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedimages',
            name='Category',
            field=models.CharField(choices=[('None', 'Select a Category'), ('Concrete_&_Brick', 'Concrete & Brick'), ('Decks', 'Decks'), ('Deck_Staining', 'Deck Staining'), ('Driveways', 'Driveways'), ('Fences', 'Fences'), ('Graffiti_Removal', 'Graffiti Removal'), ('Houses', 'Houses'), ('Sidewalks', 'Sidewalks')], default='None', max_length=64, null=True),
        ),
    ]
