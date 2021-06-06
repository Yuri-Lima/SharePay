"""
    --> Source Seach
    https://www.programiz.com/python-programming/set
    https://www.geeksforgeeks.org/python-sort-given-list-of-dictionaries-by-date/
    --> Aim
"""
"""========HouseNameModel=============="""
# user_FK=None - house_name=None - meter=None
"""========HouseBillModel=============="""
# house_bill_FK=None - amount_bill=None - start_date_bill=None - end_date_bill=None - days_bill=None
"""========HouseKilowattModel=========="""
#house_kwh_FK=None - kwh=None - last_read_kwh=None - read_kwh=None
"""========HouseTenantModel============"""
#house_name_FK=None - house_tenant=None - start_date=None - end_date=None - days=None
"""========SubHouseNameModel============"""
#sub_house_FK=None - sub_house_name=None - sub_meter=None - sub_main_house=None
"""========SubKilowattModel============="""
#main_house_kwh_FK=None - sub_house_kwh_FK=None - sub_kwh=None - sub_last_read_kwh=None - sub_read_kwh=None
"""========SubTenantModel==============="""
#main_tenant_FK=None - sub_house_tenant_FK=None - sub_house_tenant=None - sub_start_date=None - sub_end_date=None - sub_days=None

from datetime import timedelta
import datetime
from django.db.models.fields import DateTimeCheckMixin
from django.shortcuts import resolve_url
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from collections import Counter

class CoreSharePay(object):
    decimal_places_core_sharepay = None

    def __init__(self, *args, **kwargs):
        """
            kwargs: Contains all data from each House Models respective for the views
            Once you're into a views page, all data necessary for display are provided by Kwargs
            Also, kwargs contais Primary Keys(pk) and Sub Primary Keys(subpk), the last one is only provided 
            if you're in Sub Houses Pages.
        """
        self.data = kwargs

        #Set variables for Main House Name
        for d in self.data['Main_House']:
            #Related of Main House
            self.user_main_house = d.user_FK
            self.house_name_main_house = d.house_name
            self.amount_bill_main_house = d.house_bill_related.first().amount_bill
            self.start_date_bill_main_house = d.house_bill_related.first().start_date_bill
            self.end_date_bill_main_house = d.house_bill_related.first().end_date_bill
            self.days_bill_main_house = d.house_bill_related.first().days_bill
            self.kwh_main_house = d.house_kilowatt_related.first().kwh
            self.tenants_main_house = d.house_tenant_related.all()
            #Related of Sub House
            self.tenants_sub_house = d.main_house_tenant_related.all()
            self.sub_kwh_sub_house = d.main_house_kilowatt_related.all()
            
            
        #Calc for Sub House Name
        # if 'subpk' in self.data:
        #     print('There is a SubPK')
        # else:
        #     print('There is no SubPK')
        self.data_dict_date = self.main_create_range_date_by_tenant()
        self.data_dict_sub_date = self.sub_create_range_date_by_tenant()

        super(CoreSharePay, self).__init__()


    def main_create_range_date_by_tenant(self, request=None, *args, **kwargs):
        """
            Colocar o range(inicio ate o fim) de permanencia do morador em um dicionario do morador
            Insert a range(start to end) to a dictionary for each tenant
            Example: 
            Given data for Jonh--> start_date= 2021-05-01 end_date= 2021-05-30
            The range data for Jonh is -->2021-05-01, 2021-05-02, 2021-05-03,....,2021-05-30
        """
        tenants = self.tenants_main_house
        data_dict_date_range_date_by_tenant = dict()
        
        for t1 in tenants:
            data_dict_date_range_date_by_tenant[t1.house_tenant] = [t1.start_date + timedelta(days=x) for x in range(t1.days)]#Add day by day acording to t1.day
        
        return data_dict_date_range_date_by_tenant
    
    def sub_create_range_date_by_tenant(self, request=None, *args, **kwargs):
        """
            Thise functions does the same as main_create_range_date_by_tenant
        """
        sub_tenants = self.tenants_sub_house
        data_dict_date_range_date_by_sub_tenant = dict()
        #Condicao para incluir os sub tenants no calculo da main house, caso o kwh nao tenha sido preenchido
        #Pois sera levado em consideracao que a Sub house nao tem medidor, por tanto, sera dividos como se morassem na main house
        if not self.sub_kwh_sub_house:
            for sub_t1 in sub_tenants:
                data_dict_date_range_date_by_sub_tenant[sub_t1.sub_house_tenant] = [sub_t1.sub_start_date + timedelta(days=x) for x in range(sub_t1.sub_days)]#Add day by day acording to t1.day

        return data_dict_date_range_date_by_sub_tenant

    def get_tenants_by_day(self,request=None, get_date= None, *args, **kwargs):
        """
            Retorna e Filtra quais sao os tenants que estao na casa de acordo com a data enviada
            Return and Filter which tenants how is in the house by date sent.
        """
        # if not isinstance(get_date, datetime.date):
        #     try:
        #         get_date = datetime.date.fromisoformat(get_date)
        #     except ValueError as e:
        #         messages.add_message(
        #             message= "Date Format is incorret, try: YYYY-MM-DD.",
        #             level= messages.ERROR,
        #              request=request
        #         )
        #         raise ValueError('Date Format is incorret, try: YYY-MM-DD')

        date_bill_verification_by_day= get_date if get_date else self.start_date_bill_main_house
        data_dict_date_by_day = self.data_dict_date
        data_set_tenants_by_day = set()
        data_set_date_by_day = dict()
        new_dict = set()
        
        for name, date in data_dict_date_by_day.items():
            for d1 in date:
                if d1 == date_bill_verification_by_day:
                    data_set_tenants_by_day.add(name) 
        data_set_date_by_day[date_bill_verification_by_day] = data_set_tenants_by_day

        return data_set_date_by_day

    
    def get_tenants_by_name(self, tenant_name=None, request=None, *args, **kwargs): 
        """
        #Retorna e Filtra quais foram os tenants que estavam com o Tenant enviado e returna todos eles mostrando em que data ele esteve junto.
        #Return and Filter which tenants was toguther with the tenant sent by parametrs and return all of them with your respectve date.
        """ 
         
        data_set_bill = dict()
        data_dict_tenants = dict()
        tenant_name_to_filter = {str(tenant_name)}#eu preciso colocar algum nome para funcionar
        while self.start_date_bill_main_house <= self.end_date_bill_main_house:
            data_dict_tenants = self.get_tenants_by_day()
            if tenant_name_to_filter.issubset(data_dict_tenants[self.start_date_bill_main_house]):#Is verifired if tenant_name_to_filter be part of the data_dict_tenants into the date
                data_set_bill[self.start_date_bill_main_house] = data_dict_tenants[self.start_date_bill_main_house] - tenant_name_to_filter

            #Don't Remove it    
            #Increment start_date_bill_main_house
            self.start_date_bill_main_house += timedelta(days=1)
        return data_set_bill

    def filter_all_tenant_from_bill_period(self, request=None, *args, **kwargs):
        """
            Parameters: date - Format(YYYY-MM-DD)
            Retorna e Filtra quais sao os moradores em cada dia da conta
            Return and Filter each tenant into each day's bill
        """ 
        data_dict_from_bill_period = dict()
        dates = set()

        dates = [self.start_date_bill_main_house + timedelta(days=x) for x in range(self.days_bill_main_house)]#Add day by day acording to days_bill_main_house

        for enum, each_date in enumerate(dates,1):
            data_dict_from_bill_period[enum] = self.get_tenants_by_day(get_date=each_date)

        return data_dict_from_bill_period

    ############ START CALCS FOR EACH HOUSE'S CONDITION ############

    def check_same_period_tenant_from_bill(self, request= None, *args, **kwargs):
        """
            Check if all tenant's day are the same.
            If they are, return True, otherwise False
        """
        set_days_bill_check_same = {self.days_bill_main_house}#set
        set_days_main_tenants_check_same = {t_main.days for t_main in self.tenants_main_house}
        set_days_sub_tenants_check_same = {t_sub.sub_days for t_sub in self.tenants_sub_house}
        # Set union method
        check_same = set_days_bill_check_same | set_days_main_tenants_check_same | set_days_sub_tenants_check_same
        
        if len(check_same) > 1:#Should has just one date from the Bill
            return False
        return True

    """
        --> Simple Case <--
        1 - Valor da Conta / Moradores
        1 - Bill's Value / Tenant
    """
    def bill_divided_by_all_tenants_simple_case(self, request= None, *args, **kwargs):
        decimal_simple_case = 4
        decimal_places_simple_case = self.decimal_places_core_sharepay if self.decimal_places_core_sharepay else decimal_simple_case
        bills_value_simple_case = self.amount_bill_main_house
        tenants_simple_case = len(self.tenants_main_house)
        sub_tenants_simple_case = len(self.tenants_sub_house)

        return round(bills_value_simple_case / (tenants_simple_case + sub_tenants_simple_case), decimal_places_simple_case)

    def value_by_day(self,*args, **kwargs):
        bills_value_by_day = self.amount_bill_main_house
        days_bill_value_by_day = self.days_bill_main_house
        days_value_value_by_day = round(bills_value_by_day/days_bill_value_by_day, self.decimal_places_core_sharepay)
        return days_value_value_by_day
    
    def calc_only_main_house(self, request=None, *args, **kwargs):
        #Se sub house nao preencheu kwh pego todos os tenants da casa pai e filha
        """
        Step - 1. pegar o valor da bill e dividi pelo periodo da conta para saber o valor diario da conta
        Step - 2. checar quantos moradores tem com cada morador se zero, coloca 1 para fazer a divisao correta
        Step - 3. divir o valor diario pelo total de moradores que tem em cada dia da conta e guardar na variavel V
        Step - 4. guardar o valor da variavel V em cada morador por dia
        Step - 5. soma todos os valores que cada morador em um loop ate que todos os moradore tenham seus valores diarios somados em cada morador
        Step - 6. pegar os valores de cada morador e somar e guardar em uma variavel total_bill
        Step - 7. comparar o total_bill com amount_bill, para havera sobra --> left_over
        Step - 8. se nao for igual, guardar o valor residual e anexar em alguma variavel
        """
        data_dict_tenant_with_value_day = dict()
        #fill some elements from all tenants from bill period
        filter_all_tenant_from_bill_period = self.filter_all_tenant_from_bill_period()
        amount_bill_main_house = self.amount_bill_main_house
        #============== Start Calcs ======================================================
        #Step -1
        days_value_one_house_one_bill = self.value_by_day()
        #Steds -2,3,4,5,6
        total_by_each_tenant = dict()
        for t in self.tenants_main_house:
            for enum, tenant in enumerate(self.get_tenants_by_name(tenant_name=t.house_tenant).values(), 1):
                #Step -2
                check_zero = (1 if not len(tenant) else len(tenant))
                #Step -3
                v = round(days_value_one_house_one_bill / check_zero, self.decimal_places_core_sharepay)
                #Step -4
                step_3 = { key : v for key in tenant }
                print(step_3)
                #Step -5
                total_by_each_tenant = Counter(step_3) + Counter(total_by_each_tenant)
        #Step -6
        total_bill = round(sum(total_by_each_tenant.values()),2)
        
        #Steps -7 , 8
        if int(total_bill) == int(amount_bill_main_house):
            print(f'Step -6 --> {total_bill} - {total_bill - amount_bill_main_house}')
            return dict(total_by_each_tenant)
        else:
            total_by_each_tenant['left_over'] = amount_bill_main_house - total_bill
            print(f'Step -6 --> left_over {total_bill - amount_bill_main_house}')
        

                
        return dict(total_by_each_tenant)

