# Generated by Django 3.1.7 on 2021-07-01 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0045_auto_20210701_0142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subhousenamemodel',
            name='sub_house_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Sub House Name'),
        ),
    ]