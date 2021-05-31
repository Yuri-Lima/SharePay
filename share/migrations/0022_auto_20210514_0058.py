# Generated by Django 3.1.7 on 2021-05-14 00:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0021_auto_20210514_0049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='housebillmodel',
            name='house_bill_FK',
            field=models.ForeignKey(blank=True, max_length=255, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='house_bill_related', to='share.housenamemodel', verbose_name='House Bill'),
        ),
        migrations.AlterField(
            model_name='housekilowattmodel',
            name='house_kwh_FK',
            field=models.ForeignKey(blank=True, max_length=255, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='house_kilowatt_related', to='share.housenamemodel', verbose_name='House Name'),
        ),
        migrations.AlterField(
            model_name='housenamemodel',
            name='house_name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='House Name'),
        ),
        migrations.AlterField(
            model_name='housetenantmodel',
            name='house_name_FK',
            field=models.ForeignKey(blank=True, max_length=255, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='house_tenant_related', to='share.housenamemodel', verbose_name='Tenant Name'),
        ),
        migrations.AlterField(
            model_name='subkilowattmodel',
            name='sub_house_kwh_FK',
            field=models.ForeignKey(blank=True, max_length=255, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_house_kilowatt_related', to='share.subhousenamemodel', verbose_name='Sub House Name'),
        ),
    ]