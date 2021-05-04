# Generated by Django 3.1.7 on 2021-05-04 08:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('share', '0006_auto_20210504_0833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='housebillmodel',
            name='house_bill_FK',
            field=models.ForeignKey(max_length=255, on_delete=django.db.models.deletion.CASCADE, related_name='house_bill_related', to='share.housenamemodel', verbose_name='House Bill'),
        ),
        migrations.AlterField(
            model_name='housekilowattmodel',
            name='house_kwh_FK',
            field=models.ForeignKey(max_length=255, on_delete=django.db.models.deletion.CASCADE, related_name='house_kilowatt_related', to='share.housenamemodel', verbose_name='House Name'),
        ),
        migrations.AlterField(
            model_name='housenamemodel',
            name='user_FK',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_related', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='housetenantmodel',
            name='house_name_FK',
            field=models.ForeignKey(max_length=255, on_delete=django.db.models.deletion.CASCADE, related_name='house_tenant_related', to='share.housenamemodel', verbose_name='Tenant Name'),
        ),
    ]
