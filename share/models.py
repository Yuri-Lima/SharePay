from django.db import models
from django.conf import settings
from django.forms import widgets
from django.urls import reverse
from django.forms.widgets import DateTimeInput

class HouseNameModel(models.Model):
    user_FK = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_related', null=False)
    house_name = models.CharField(verbose_name="House name",max_length=150, null=False, blank=False)
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
                            on_delete=models.CASCADE, related_name='house_tenant_related')
    house_tenant = models.CharField(max_length=150, null=True, blank=True)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)
    days = models.IntegerField(default=0)
    last_updated_tenant = models.DateField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.house_tenant
    
    def get_absolute_url(self):
        return reverse('share:detail_house_name', kwargs={'pk': self.pk})

    def clean(self):
        if self.start_date and self.end_date:
            self.days = int((self.end_date - self.start_date).days)
        else:
            self.days = 30
    class Meta:
        ordering = ['-last_updated_tenant']
        
class HouseBillModel(models.Model):
    house_bill_FK = models.ForeignKey(HouseNameModel, null=False, blank= False, max_length=255,
                                on_delete=models.CASCADE, related_name='house_bill_related')
    amount_bill = models.DecimalField(null=True, blank= True, max_digits=10, decimal_places=2)
    start_date_bill = models.DateField(null=False, blank=False)
    end_date_bill = models.DateField(null=False, blank=False)
    days_bill = models.IntegerField(default=0)
    last_updated_bill = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ['-last_updated_bill']

    def __str__(self):
        return str(self.house_bill_FK) + ' - ' + str(self.amount_bill)
    
    def clean(self):
        if self.start_date_bill and self.end_date_bill:
            self.days_bill = int((self.end_date_bill - self.start_date_bill).days)
            return self.days_bill
        self.days_bill = 30
        return self.days_bill
    
    def get_absolute_url(self):
        return reverse('share:detail_house_name', kwargs={'pk': self.pk})

class HouseKilowattModel(models.Model):
    house_kwh_FK = models.ForeignKey(HouseNameModel, null=False, blank=False, max_length=255,
                                on_delete=models.CASCADE, related_name='house_kilowatt_related')
    kwh = models.IntegerField(null=True, blank=True, default=0)
    last_read_kwh = models.IntegerField(null=True, blank=True)
    read_kwh = models.IntegerField(null=True, blank=True)
    last_updated_kwh = models.DateField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ['-last_updated_kwh']

    def __str__(self):
        return str(kwh)

    def clean(self):
        if self.last_read_kwh and self.read_kwh:
            self.kwh = int(self.read_kwh - self.last_read_kwh)
            return self.kwh
        return self.kwh

    def get_absolute_url(self):
        return reverse('share:detail_house_name', kwargs={'pk': self.pk})

