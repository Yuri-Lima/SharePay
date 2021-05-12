# Generated by Django 3.1.7 on 2021-05-12 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0017_auto_20210511_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subkilowattmodel',
            name='main_house_kwh_FK',
            field=models.ForeignKey(max_length=255, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='main_house_kilowatt_related', to='share.housenamemodel', verbose_name='House Name'),
        ),
        migrations.AlterField(
            model_name='subkilowattmodel',
            name='sub_house_kwh_FK',
            field=models.ForeignKey(max_length=255, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_house_kilowatt_related', to='share.subhousenamemodel', verbose_name='Sub House Name'),
        ),
        migrations.AlterField(
            model_name='subtenantmodel',
            name='main_tenant_FK',
            field=models.ForeignKey(max_length=255, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='main_house_tenant_related', to='share.housenamemodel', verbose_name='House Name'),
        ),
        migrations.AlterField(
            model_name='subtenantmodel',
            name='sub_house_tenant_FK',
            field=models.OneToOneField(max_length=255, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_house_tenant_related', to='share.subhousenamemodel', verbose_name='Sub House Name'),
        ),
    ]
