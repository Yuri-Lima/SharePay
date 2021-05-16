# Generated by Django 3.1.7 on 2021-05-13 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0018_auto_20210512_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subkilowattmodel',
            name='sub_kwh',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='KWH'),
        ),
        migrations.AlterField(
            model_name='subtenantmodel',
            name='sub_house_tenant_FK',
            field=models.ForeignKey(max_length=255, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_house_tenant_related', to='share.subhousenamemodel', verbose_name='Sub House Name'),
        ),
    ]
