# Generated by Django 3.1.7 on 2021-05-04 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0004_auto_20210503_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='housekilowattmodel',
            name='kwh',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]