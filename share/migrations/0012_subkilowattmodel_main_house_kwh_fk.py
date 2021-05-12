# Generated by Django 3.1.7 on 2021-05-11 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0011_subhousenamemodel_subkilowattmodel_subtenantmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='subkilowattmodel',
            name='main_house_kwh_FK',
            field=models.OneToOneField(max_length=255, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_house_kilowatt_related', to='share.subhousenamemodel', verbose_name='House Name'),
        ),
    ]
