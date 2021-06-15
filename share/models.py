from django.db import models
from django.conf import settings
from django.db.models.query_utils import select_related_descend
from django.forms import widgets
from django.urls import reverse
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.utils.translation import gettext_lazy as _
from django.forms.widgets import DateTimeInput
from decimal import *


class HouseNameModel(models.Model):
    user_FK = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_related', null=False, verbose_name='User')
    house_name = models.CharField(verbose_name="House Name",max_length=100, null=True, blank=True, unique=True,)
    meter = models.IntegerField(default=1)
    # main_house = models.BooleanField(null=False, blank=False, help_text='Is the bill belongs this house typed above?')
    last_updated_house = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.house_name
    
    def get_absolute_url(self):
        return reverse('share:detail_house_name', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-last_updated_house']
    
    def clean(self):
        if self.house_name != None:
            if len(self.house_name) > 25:
                raise ValidationError({
                    'house_name': _(f'Ensure House Name has max 25 characters (it has {len(self.house_name)}).'),
                })
        else:
            raise ValidationError({
                'house_name': _('You must provide a House Name (up to 25 letters).'),
            })
        
class HouseBillModel(models.Model):
    house_bill_FK = models.ForeignKey(HouseNameModel, null=True, blank=True, max_length=255,
                                on_delete=models.CASCADE, related_name='house_bill_related', verbose_name='House Bill')
    amount_bill = models.CharField(null=True, blank= True, max_length=22)
    start_date_bill = models.DateField(null=False, blank=False)
    end_date_bill = models.DateField(null=False, blank=False)
    days_bill = models.IntegerField(default=0)
    last_updated_bill = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-last_updated_bill']

    def __str__(self):
        if self.house_bill_FK and self.amount_bill:
            return str(self.house_bill_FK) + ' - ' + '€' + str(self.amount_bill)
    
    def clean(self):
        if self.start_date_bill and self.end_date_bill:
            self.days_bill = int((self.end_date_bill - self.start_date_bill).days)
            if self.days_bill < 0:
                raise ValidationError({
                    'start_date_bill': _('Is that start date correct?'),
                    'end_date_bill': _('This field should be older!')
                })

        self.amount_bill = Decimal(self.amount_bill.replace(',',''))
        if self.amount_bill < 0:
            raise ValidationError({
                'amount_bill': _('Should be a positive number!'),
            })
    
    def get_absolute_url(self):
        return reverse('share:detail_house_name', kwargs={'pk': self.pk})

class HouseKilowattModel(models.Model):
    house_kwh_FK = models.ForeignKey(HouseNameModel, null=True, blank=True, max_length=255,
                                on_delete=models.CASCADE, related_name='house_kilowatt_related', verbose_name='House Name')
    kwh = models.DecimalField(null=True, blank= True, max_digits=10, decimal_places=0)
    last_read_kwh = models.DecimalField(null=True, blank= True, max_digits=10, decimal_places=0)
    read_kwh = models.DecimalField(null=True, blank= True, max_digits=10, decimal_places=0)
    last_updated_kwh = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-last_updated_kwh']

    def __str__(self):
        return str(self.house_kwh_FK) + ' - ' + str(self.kwh) + 'kwh'

    #https://docs.djangoproject.com/en/3.2/ref/models/instances/
    def clean(self):
        if self.last_read_kwh and self.read_kwh:
            if (self.last_read_kwh > self.read_kwh):
                raise ValidationError({
                    'read_kwh': _('Should be greatter than previous Kw/h read')
                    })
            else:
                self.kwh = self.read_kwh - self.last_read_kwh
            return self.kwh
        elif self.kwh:
            return self.kwh
        else:
            raise ValidationError({
                        'kwh': _('Fill up at least one option!'),
                        'last_read_kwh': _('Fill up at least one option!'),
                        # 'read_kwh' : _('Only Numbers'),
                        })

    def get_absolute_url(self):
        return reverse('share:detail_house_name', kwargs={
                                                        'pk': self.pk,
                                                        'subpk': self.subpk,
                                                        })

class HouseTenantModel(models.Model):
    house_name_FK = models.ForeignKey(HouseNameModel, null=True, blank=True, max_length=255,
                            on_delete=models.CASCADE, related_name='house_tenant_related', verbose_name='Tenant Name')
    house_tenant = models.CharField(max_length=150, null=True, blank=True,)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    days = models.IntegerField(null=True, blank=True, default=0)
    last_updated_tenant = models.DateField(auto_now=True, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.house_tenant
    
    def get_absolute_url(self):
        return reverse('share:detail_house_name', kwargs={
                                                        'pk': self.pk,
                                                        'subpk': self.subpk,
                                                        })

    def clean(self):
        if self.house_tenant:
            concat_sliced_name=''
            for sliced_name in self.house_tenant.split():
                concat_sliced_name = concat_sliced_name + sliced_name.capitalize() + ' '
            self.house_tenant =  concat_sliced_name.strip()
        else:
            raise ValidationError({
                    'house_tenant': _('This field is required.'),
                })
            
    class Meta:
        ordering = ['-last_updated_tenant']

class SubHouseNameModel(models.Model):
    """
        'unique_test': Source--> https://docs.djangoproject.com/en/3.2/ref/models/constraints/#django.db.models.UniqueConstraint
    """
    sub_house_FK = models.ForeignKey(HouseNameModel, null=True, blank=True, max_length=255,
                                on_delete=models.CASCADE, related_name='sub_house_related', verbose_name='House Name')
    sub_house_name = models.CharField(verbose_name="Sub House Name",max_length=100, null=True, blank=True, unique=True, error_messages={'unique':'Sub House Name has already been created! Try some diferent one.'})
    sub_meter = models.IntegerField(null=True, blank=True, default=1)
    sub_main_house = models.BooleanField(null=False, blank=False, help_text='Is the bill belongs this house typed above?')
    sub_last_updated_house = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    unique_test = models.UniqueConstraint(fields= ['sub_house_FK','sub_house_name'], name='unique_sub_house')
    
    def __str__(self) -> str:
        return self.sub_house_name

    def get_absolute_url(self, subpk): 
        return reverse('share:add_sub_house_kwh', kwargs={
                                                        'pk': self.pk,
                                                        'subpk': self.subpk,
                                                        })

    class Meta:
        ordering = ['-sub_last_updated_house']

class SubKilowattModel(models.Model):
    main_house_kwh_FK = models.ForeignKey(HouseNameModel, null=True, blank=True, max_length=255,
                                on_delete=models.CASCADE, related_name='main_house_kilowatt_related', verbose_name='House Name')
    sub_house_kwh_FK = models.ForeignKey(SubHouseNameModel, null=True, blank=True, max_length=255,
                                on_delete=models.CASCADE, related_name='sub_house_kilowatt_related', verbose_name='Sub House Name')              
    sub_kwh = models.DecimalField(null=True, blank= True, max_digits=10, decimal_places=0, default=0)
    sub_amount_bill = models.DecimalField(null=True, blank= True, max_digits=10, decimal_places=0, default=0)
    sub_last_read_kwh = models.DecimalField(null=True, blank= True, max_digits=10, decimal_places=0, default=0)
    sub_read_kwh = models.DecimalField(null=True, blank= True, max_digits=10, decimal_places=0, default=0)
    sub_last_updated_kwh = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-sub_last_updated_kwh']

    def __str__(self):
        return str(self.sub_house_kwh_FK) + ' - ' + str(self.sub_kwh) + 'kwh'

    #https://docs.djangoproject.com/en/3.2/ref/models/instances/
    def clean(self):
        if self.sub_last_read_kwh and self.sub_read_kwh:
            if (self.sub_last_read_kwh > self.sub_read_kwh):
                raise ValidationError({
                    'sub_read_kwh': _('Should be greatter than previous Kw/h read')
                    })
            else:
                self.sub_kwh = self.sub_read_kwh - self.sub_last_read_kwh
            return self.sub_kwh
        elif self.sub_kwh:
            return self.sub_kwh
        else:
            raise ValidationError({
                        'sub_kwh': _('Fill up at least one option!'),
                        'sub_last_read_kwh': _('Fill up at least one option!'),
                        # 'sub_read_kwh' : _('Only Numbers'),
                        })

    def get_absolute_url(self, subpk):
        return reverse('share:detail_sub_house_name', kwargs={
                                                        'pk': self.pk,
                                                        'subpk': self.subpk,
                                                        })

class SubTenantModel(models.Model):
    main_tenant_FK = models.ForeignKey(HouseNameModel, null=True, blank=True, max_length=255,
                                on_delete=models.CASCADE, related_name='main_house_tenant_related', verbose_name='House Name')
    sub_house_tenant_FK = models.ForeignKey(SubHouseNameModel, null=True, blank=True, max_length=255,
                                on_delete=models.CASCADE, related_name='sub_house_tenant_related', verbose_name='Sub House Name')
    sub_house_tenant = models.CharField(max_length=150, null=True, blank=True,)
    sub_start_date = models.DateField(null=True, blank=True)
    sub_end_date = models.DateField(null=True, blank=True)
    sub_days = models.IntegerField(null=True, blank=True, default=0)
    sub_last_updated_tenant = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-sub_last_updated_tenant']

    def __str__(self):
        if self.sub_house_tenant:
            return self.sub_house_tenant
        return self

    def get_absolute_url(self, subpk):
        return reverse('share:detail_sub_house_name', kwargs={
                                                        'pk': self.pk,
                                                        'subpk': self.subpk,
                                                        })

    def clean(self):
        if self.sub_house_tenant:
            concat_sliced_name=''
            for sliced_name in self.sub_house_tenant.split():
                concat_sliced_name = concat_sliced_name + sliced_name.capitalize() + ' '
            self.sub_house_tenant =  concat_sliced_name.strip()

# error_messages={'unique':'Sub House Name has already been created! Try some diferent one.'}

#https://docs.djangoproject.com/en/3.2/ref/models/fields/#unique
# If you don’t want multiple associations between the same instances, add a UniqueConstraint including the from and to fields. Django’s automatically generated many-to-many tables include such a constraint.

