from django.db import models
from django.conf import settings
from django.forms import widgets
from django.urls import reverse
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.utils.translation import gettext_lazy as _
from django.forms.widgets import DateTimeInput


class HouseNameModel(models.Model):
    user_FK = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_related', null=False, verbose_name='User')
    house_name = models.CharField(verbose_name="House Name",max_length=150, null=False, blank=False)
    meter = models.IntegerField(default=1)
    last_updated_house = models.DateField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.house_name
    
    def get_absolute_url(self):
        return reverse('share:detail_house_name', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-last_updated_house']
    

class HouseTenantModel(models.Model):
    house_name_FK = models.ForeignKey(HouseNameModel, null=False, blank=False, max_length=255,
                            on_delete=models.CASCADE, related_name='house_tenant_related', verbose_name='Tenant Name')
    house_tenant = models.CharField(max_length=150, null=True, blank=True)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    days = models.IntegerField(default=0)
    last_updated_tenant = models.DateField(auto_now=True, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.house_tenant
    
    def get_absolute_url(self):
        return reverse('share:detail_house_name', kwargs={'pk': self.pk})

    def clean(self):
        self.house_tenant = self.house_tenant.capitalize()
        if self.start_date and self.end_date:
            self.days = int((self.end_date - self.start_date).days)
        else:
            self.days = 30
            
    class Meta:
        ordering = ['-last_updated_tenant']
        
class HouseBillModel(models.Model):
    house_bill_FK = models.ForeignKey(HouseNameModel, null=False, blank= False, max_length=255,
                                on_delete=models.CASCADE, related_name='house_bill_related', verbose_name='House Bill')
    amount_bill = models.DecimalField(null=True, blank= True, max_digits=10, decimal_places=2)
    start_date_bill = models.DateField(null=False, blank=False)
    end_date_bill = models.DateField(null=False, blank=False)
    days_bill = models.IntegerField(default=0)
    last_updated_bill = models.DateField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-last_updated_bill']

    def __str__(self):
        return str(self.house_bill_FK) + ' - ' + '€' + str(self.amount_bill)
    
    def clean(self):
        if self.start_date_bill and self.end_date_bill:
            self.days_bill = int((self.end_date_bill - self.start_date_bill).days)
        else:
            self.days_bill = 30
    
    def get_absolute_url(self):
        return reverse('share:detail_house_name', kwargs={'pk': self.pk})

class HouseKilowattModel(models.Model):
    house_kwh_FK = models.ForeignKey(HouseNameModel, null=False, blank=False, max_length=255,
                                on_delete=models.CASCADE, related_name='house_kilowatt_related', verbose_name='House Name')
    kwh = models.IntegerField(null=True, blank=True, verbose_name='KWH')
    last_read_kwh = models.IntegerField(null=True, blank=True)
    read_kwh = models.IntegerField(null=True, blank=True, help_text='Should be greatter than last read Kwh')
    last_updated_kwh = models.DateField(auto_now=True, null=True, blank=True)

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
        return reverse('share:detail_house_name', kwargs={'pk': self.pk})

