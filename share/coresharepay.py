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
from decimal import *

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
            self.sub_house_names = d.sub_house_related.all()
            self.tenants_sub_house = d.main_house_tenant_related.all()
            self.sub_kwh_sub_house = d.main_house_kilowatt_related.all()

            #Related of get_tenants_by_day
            self._empty_days = 0

            self._check_if_there_is_day_without_tenants()
            self.create_range_date_by_tenant()

        super(CoreSharePay, self).__init__()

    def _check_if_there_is_day_without_tenants(self, *args, **kwargs):
        # print(type(self.tenants_main_house))
        # self.tenants_sub_house 
        pass
        
  
    def create_range_date_by_tenant(self, request=None, *args, **kwargs):
        """
            Colocar o range(inicio ate o fim) de permanencia do morador em um dicionario do morador
            Insert a range(start to end) to a dictionary for each tenant
            Example: 
            Given data for Jonh--> start_date= 2021-05-01 end_date= 2021-05-30
            The range data for Jonh is -->2021-05-01, 2021-05-02, 2021-05-03,....,2021-05-30
        """
        #=======xxxxx Main xxxx===========
        tenants = self.tenants_main_house
        self.dict_date_range_for_tenants = dict()
        
        for t1 in tenants:
            self.dict_date_range_for_tenants[t1.house_tenant] = [t1.start_date + timedelta(days=x) for x in range(t1.days)]#Add day by day acording to t1.day
        
        #=======xxxxx Sub xxxx===========
        sub_tenants = self.tenants_sub_house
        subids = self.check_if_which_sub_house_hasnt_kwh_filled()
        for name, subid in subids.items():
            for sub_t1 in sub_tenants.filter(sub_house_tenant_FK=subid):
                self.dict_date_range_for_tenants[sub_t1] = [sub_t1.sub_start_date + timedelta(days=x) for x in range(sub_t1.sub_days)]#Add day by day acording to t1.sub_day

    def check_if_which_sub_house_hasnt_kwh_filled(self, kilowatts= False, names=False, *args, **kwargs):
        """
            retorna o id de quem nao tem o sub kwh cadastrado
        """
        #=======xxxxx Sub xxxx===========
        sub_tenants = self.tenants_sub_house
        self.dict_date_range_for_sub_tenants = dict()
        #Condicao para incluir os sub tenants no calculo da main house, caso o kwh nao tenha sido preenchido
        #Pois sera levado em consideracao que a Sub house nao tem medidor, por tanto, sera dividos como se morassem na main house
        subid=dict()
        tenants_name = dict()
        for obj in self.sub_house_names:#Todas as sub casas
            if not obj.sub_house_name in [k.sub_house_kwh_FK.sub_house_name for k in self.sub_kwh_sub_house]:#verifica qual e a casa que nao tem kwh cadastrado
                #print(sub_tenants.filter(sub_house_tenant_FK=obj.id))#pega apenas os tenants que pertencem a casa que nao tem kwh cadastrado
                tenants_name[obj.sub_house_name]= sub_tenants.filter(sub_house_tenant_FK=obj.id)
                subid[obj.sub_house_name]=obj.id
            # else:#casas com kilowatts preenchidos
            #     print(obj.sub_house_name)

        #if names and kilowatts are true
        if names:
            return tenants_name
        return subid


    def get_tenants_by_day(self,request=None, get_date= None, *args, **kwargs):
        """
            Retorna e Filtra quais sao os tenants que estao na casa de acordo com a data enviada
            Return and Filter which tenants how is in the house by date sent.
            Return data like this --> {datetime.date(2021, 3, 14): {'Daiane', 'Nathalia', 'Eugenio', 'Elizagela', 'Ellen', 'José'}}
        """

        date_bill_verification_by_day= get_date if get_date else self.start_date_bill_main_house
        data_dict_date_by_day = self.dict_date_range_for_tenants
        data_set_tenants_by_day = set()
        data_set_date_by_day = dict()
        
        for name, date in data_dict_date_by_day.items():
            if date_bill_verification_by_day in date:
                data_set_tenants_by_day.add(str(name))


        data_set_date_by_day[date_bill_verification_by_day] = data_set_tenants_by_day

        if not data_set_date_by_day[date_bill_verification_by_day]:
            self._empty_days =  self._empty_days + 1
            data_set_date_by_day[date_bill_verification_by_day] = {'Left'}
        
        
        return data_set_date_by_day

    
    def get_tenants_by_name(self, tenant_name=None, request=None, *args, **kwargs): 
        """
        #Retorna e Filtra quais foram os tenants que estavam com o Tenant enviado e returna todos eles mostrando em que data ele esteve junto.
        #Return and Filter which tenants was toguther with the tenant sent by parametrs and return all of them with your respectve date.
        """ 
         
        data_set_bill = dict()
        data_dict_tenants = dict()
        tenant_name_to_filter = {str(tenant_name)}#eu preciso colocar algum nome para funcionar
        start_date_bill_main_house = self.start_date_bill_main_house 
        
        dates = [start_date_bill_main_house + timedelta(days=x) for x in range(self.days_bill_main_house)]#Add day by day acording to days_bill_main_house
        
        for date in dates:
            data_dict_tenants = self.get_tenants_by_day(get_date=date)
            if tenant_name_to_filter.issubset(data_dict_tenants[date]):#Is verifired if tenant_name_to_filter be part of the data_dict_tenants into the date
                data_set_bill[date] = data_dict_tenants[date] #- tenant_name_to_filter

        #{datetime.date(2021, 5, 10): {'Daiane', 'Jamile', 'Ellen', 'José', 'Eugenio', 'Nathalia', 'Elizagela'}}
        return data_set_bill

    def filter_all_tenant_from_bill_period(self, request=None, *args, **kwargs):
        """
            Parameters: date - Format(YYYY-MM-DD)
            Retorna e Filtra quais sao os moradores em cada dia da conta
            Return and Filter each tenant into each day's bill
        """ 
        data_dict_from_bill_period = dict()
        dates = set()
        start_date_bill_main_house = self.start_date_bill_main_house 

        dates = [start_date_bill_main_house + timedelta(days=x) for x in range(self.days_bill_main_house)]#Add day by day acording to days_bill_main_house

        for enum, each_date in enumerate(dates,1):
            data_dict_from_bill_period[enum] = self.get_tenants_by_day(get_date=each_date)

        #57: {datetime.date(2021, 5, 9): {'Daiane', 'Elizagela', 'José', 'Ellen', 'Nathalia', 'Eugenio'}}
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


    def bill_divided_by_all_tenants_simple_case(self, request= None, *args, **kwargs):
        decimal_simple_case = 4
        decimal_places_simple_case = self.decimal_places_core_sharepay if self.decimal_places_core_sharepay else decimal_simple_case
        bills_value_simple_case = self.amount_bill_main_house
        tenants_simple_case = len(self.tenants_main_house)
        sub_tenants_simple_case = len(self.tenants_sub_house)

        return round(bills_value_simple_case / (tenants_simple_case + sub_tenants_simple_case), decimal_places_simple_case)

    def value_by_day(self,*args, **kwargs):
        bills_value_by_day = float(self.amount_bill_main_house)
        days_bill_value_by_day = self.days_bill_main_house
        days_value_value_by_day = round(bills_value_by_day/days_bill_value_by_day, self.decimal_places_core_sharepay)
        return days_value_value_by_day
    
    def calc_1(self, request=None, *args, **kwargs):
        #Se sub house nao preencheu kwh pego todos os tenants da casa pai e filhos(Nao se pega pai'S' somente todos os filhos)
        """
        Step - 1. pegar o valor da bill e dividi pelo periodo da conta para saber o valor diario da conta
        Step - 2. checar quantos inquilinos moram com o mesmo, se nenhum(zero), coloca 1 para fazer a divisao correta
        Step - 3. divir o valor diario pelo total de moradores que tem em cada dia da conta e guardar na variavel V
        Step - 4. guardar o valor da variavel V em cada morador por dia
        Step - 5. soma todos os valores que cada morador em um loop ate que todos os moradore tenham seus valores diarios somados em cada morador
        Step - 6. logo apos a soma converter os valores v de Decimal Class to Float
        Step - 7. verifica se tem left_over se tem coloca em sua proria dict
        Step - 8. pegar todos os moradores das sub houses que nao possuem kwh preenchidos, pois se nao tem, o calculo da divisao sera feito junto com a casa principal
        Step - 9.
            --> cria um novo dicionario dentro de total_by_each_tenant_converted, definindo chaves e valores, 
            para identificar quem sao subhouses e seus atributos e quem e a casa principal e seus atributos.
            dict[casa]={dict[nome_do_morador]:{valor: , data:  , dia:  ,}}
        Step - 10. soma todos os valors por morador gerando o total de cada morador
        Step - 11. validations
        """
        data_dict_tenant_with_value_day = dict()
        #fill some elements from all tenants from bill period
        filter_all_tenant_from_bill_period = self.filter_all_tenant_from_bill_period()
        #============== Start Calcs ======================================================
        #Step -1
        days_value_one_house_one_bill = self.value_by_day()
        #Steds -2,3,4,5,6
        tenants_main_house = self.tenants_main_house
        total_by_each_tenant = dict()
        total_by_each_tenant_converted =  dict()
        
        house_name_main_house = self.house_name_main_house
        getcontext().prec = 9 #manter alta precisao, pois no somatorio sera necessario.
        
        for day_number, date_1 in filter_all_tenant_from_bill_period.items():# day_number: {date_1):{names}}
            for date_2, names in date_1.items(): #{date_2):{names}}
                #Step -2
                check_zero = (1 if not len(names) else len(names))
                #Step -3
                v = round(days_value_one_house_one_bill / check_zero, getcontext().prec - 1)
                #Step -4
                step_3 = { key : v for key in names }
                #Step -5
                total_by_each_tenant = Counter(step_3) + Counter(total_by_each_tenant)
                #Step -6
                total_by_each_tenant_converted['all'] = {key : float(value) for key, value in total_by_each_tenant.items() if key != 'Left'}#tiver que converter, pois v estava em Decimal Class
                total_by_each_tenant_converted['Left_Over'] = {key : float(value) for key, value in total_by_each_tenant.items() if key == 'Left'}
                #Step -7
        
        #================================= 
        #Step -8
        sub_tenants_filtered = self.check_if_which_sub_house_hasnt_kwh_filled(names=True)
        #Step -9
         #--> Main Houses Data <---
        total_by_each_tenant_converted['main_house'] = {
            str(house_name_main_house) : {
                str(each_name) : {
                    str('value'): f"€{round(total_by_each_tenant_converted['all'].pop(str(each_name)),2)}",
                    str('date'): f'{each_name.start_date} to {each_name.end_date}',
                    str('days'): f'{each_name.days}',
                }for each_name in tenants_main_house
            }#there is no another main house, because there is just one by each views(one PK)
        }
        #--> Sub Houses Data <---        
        total_by_each_tenant_converted['sub_house'] = {
            str(sub_house_name) : {
                str(each_name) : {
                    str('value'): f'€{round(total_by_each_tenant_converted["all"].pop(str(each_name)),2)}',
                    str('date'): f'{each_name.sub_start_date} to {each_name.sub_end_date}',
                    str('days'): f'{each_name.sub_days}',
                    }for each_name in sub_tenants_names#should be all sub tenants
                }for sub_house_name, sub_tenants_names in sub_tenants_filtered.items()#should be only sub_houses_name
            }#there are some possibilities which we can have multiple sub house it means multiples sub_pk's

        #--> Left Houses Data <---
        if total_by_each_tenant_converted['Left_Over']:
            total_by_each_tenant_converted['left_over'] = {
                str('Left_Over') : {
                    str('description') : 'This is a value which no one was living as a tenant.',
                    str('left_over') : f'€{round(total_by_each_tenant_converted["Left_Over"]["Left"],2)}',
                    str('days_left_over') : f'{self._empty_days}',
                }
            }
            total_by_each_tenant_converted.pop('Left_Over')

        total_by_each_tenant_converted.pop('all')

        #Step -10
        total_by_each_tenant_converted['kwh'] = self.kwh_main_house
        total_by_each_tenant_converted['bill_value'] = self.amount_bill_main_house
        total_by_each_tenant_converted['period_bill'] = f'{self.start_date_bill_main_house} to {self.end_date_bill_main_house}'
        total_by_each_tenant_converted['user'] = self.user_main_house

        #Step -10
        getcontext().prec = 5 #Reduz a precisao um pouco pois nao sera mais necessario, uma vez que os valores ja teve sua alta precisao
        # total_bill = Decimal(sum(total_by_each_tenant.values()))
        # print(total_bill)


        #Validations
        """
            Reminds: Create validations
        """
        #Steps -11
   
        return total_by_each_tenant_converted

