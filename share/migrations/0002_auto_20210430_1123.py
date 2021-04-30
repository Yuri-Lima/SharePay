# Generated by Django 3.1.7 on 2021-04-30 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='housebillmodel',
            options={'ordering': ['-last_updated_bill']},
        ),
        migrations.AlterModelOptions(
            name='housenamemodel',
            options={'ordering': ['-last_updated_house']},
        ),
        migrations.AlterModelOptions(
            name='housetenantmodel',
            options={'ordering': ['-last_updated_tenant']},
        ),
        migrations.AddField(
            model_name='housebillmodel',
            name='last_updated_bill',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='housenamemodel',
            name='last_updated_house',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='housetenantmodel',
            name='last_updated_tenant',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
