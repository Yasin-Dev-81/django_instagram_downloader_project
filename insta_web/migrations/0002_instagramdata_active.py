# Generated by Django 4.0.2 on 2022-08-21 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insta_web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='instagramdata',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
