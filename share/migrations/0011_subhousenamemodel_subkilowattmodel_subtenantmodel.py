# Generated by Django 3.1.7 on 2021-05-10 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0010_auto_20210510_1304'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubTenantModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_house_tenant', models.CharField(blank=True, max_length=150, null=True)),
                ('sub_start_date', models.DateField()),
                ('sub_end_date', models.DateField()),
                ('sub_days', models.IntegerField(default=0)),
                ('sub_last_updated_tenant', models.DateField(auto_now=True, null=True)),
                ('sub_tenant_FK', models.ForeignKey(max_length=255, on_delete=django.db.models.deletion.CASCADE, related_name='sub_tenant_related', to='share.housenamemodel', verbose_name='House Name')),
            ],
            options={
                'ordering': ['-sub_last_updated_tenant'],
            },
        ),
        migrations.CreateModel(
            name='SubKilowattModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_kwh', models.IntegerField(blank=True, null=True, verbose_name='KWH')),
                ('sub_last_read_kwh', models.IntegerField(blank=True, null=True)),
                ('sub_read_kwh', models.IntegerField(blank=True, help_text='Should be greatter than last read Kwh', null=True)),
                ('sub_last_updated_kwh', models.DateField(auto_now=True, null=True)),
                ('sub_house_kwh_FK', models.ForeignKey(max_length=255, on_delete=django.db.models.deletion.CASCADE, related_name='sub_house_kilowatt_related', to='share.housenamemodel', verbose_name='House Name')),
            ],
            options={
                'ordering': ['-sub_last_updated_kwh'],
            },
        ),
        migrations.CreateModel(
            name='SubHouseNameModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_house_name', models.CharField(max_length=150, verbose_name='Sub House Name')),
                ('sub_meter', models.IntegerField(default=1)),
                ('sub_main_house', models.BooleanField(help_text='Is the bill belongs this house typed above?')),
                ('sub_last_updated_house', models.DateField(auto_now_add=True, null=True)),
                ('sub_house_FK', models.ForeignKey(max_length=255, on_delete=django.db.models.deletion.CASCADE, related_name='sub_house_related', to='share.housenamemodel', verbose_name='House Name')),
            ],
            options={
                'ordering': ['-sub_last_updated_house'],
            },
        ),
    ]