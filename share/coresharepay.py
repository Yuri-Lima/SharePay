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

from datetime import datetime, timedelta
from django.utils.translation import gettext_lazy as _
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
        self.range_dates_bill = [self.start_date_bill_main_house + timedelta(days=x) for x in range(self.days_bill_main_house)]#Add day by day acording to days_bill_main_house
        """
            Dont' change this order
        """
        # 1
        self.split_bill()
        # 2
        self.check_if_which_sub_house_hasnt_kwh_filled()
        # 3
        self.create_range_date_by_tenant()
        

        super(CoreSharePay, self).__init__()
    # 1
    def split_bill(self, *args, **kwargs):
        """
            Step -1. iterate throuth all sub kwh houses
            Step -2. get each kwh and decrease from the main kwh
            Step -3. calc how much going to be the new main value of the bill
        """
        self.new_main_kwh = self.kwh_main_house
        self.main_amount_bill = self.amount_bill_main_house

        self.amount_by_sub_houses_with_kwh = dict()

        #step 1:
        getcontext().prec = 8 #manter alta precisao, pois no somatorio sera necessario.
        for each_kwh in self.sub_kwh_sub_house:
        #step 2:
            self.new_main_kwh = self.new_main_kwh - each_kwh.sub_kwh
            self.amount_by_sub_houses_with_kwh[each_kwh.sub_house_kwh_FK] = (Decimal(self.main_amount_bill) * Decimal(each_kwh.sub_kwh))/self.kwh_main_house
        # print(f'amount--->>{self.amount_by_sub_houses_with_kwh}\n')
        """
            #step 3 Calc:
            main_amount --- main_kwh
                x       --- r
        """
        #step 3:
        getcontext().prec = 6 #manter alta precisao, pois no somatorio sera necessario.
        self.new_amount_main_bill = (Decimal(self.main_amount_bill) * Decimal(self.new_main_kwh))/self.kwh_main_house
        # print(f"new_amount_main_bill: {self.new_amount_main_bill}")
    # 2
    def check_if_which_sub_house_hasnt_kwh_filled(self, _names_with_kwh=False, _names_without_kwh=False, _subid_without_kwh=False, _subid_with_kwh=False, *args, **kwargs):
        """
            _names: Se True retorna apenas nomes dos moradores que moram em sub casas sem kwh registrados
            _names e _kilowatts: Se True retorna nomes dos moradores que moram em sub casas com kwh registrados
            _subid_without_kwh: Se True retorna o id das sub casas que nao tem kwh cadastrados
            _subid_with_kwh: Se True retorna o id das sub casas que nao tem kwh cadastrados
        """
        #=======xxxxx Sub xxxx===========
        sub_tenants = self.tenants_sub_house
        self.dict_date_range_for_sub_tenants = dict()
        #Condicao para incluir os sub tenants no calculo da main house, caso o kwh nao tenha sido preenchido
        #Pois sera levado em consideracao que a Sub house nao tem medidor, por tanto, sera dividos como se morassem na main house
        self.subid_without_kwh=dict()
        self.subid_with_kwh=dict()

        self.tenants_name_without_kwh = dict()
        self.tenants_name_with_kwh = dict()

        for obj in self.sub_house_names:#Todas as sub casas
            if not obj.sub_house_name in [k.sub_house_kwh_FK.sub_house_name for k in self.sub_kwh_sub_house]:#verifica qual e a casa que nao tem kwh cadastrado
                #print(sub_tenants.filter(sub_house_tenant_FK=obj.id))#pega apenas os tenants que pertencem a casa que nao tem kwh cadastrado
                self.tenants_name_without_kwh[obj.sub_house_name]= sub_tenants.filter(sub_house_tenant_FK=obj.id)
                self.subid_without_kwh[obj.sub_house_name]=obj.id
            else:#casas com kilowatts preenchidos
                self.tenants_name_with_kwh[obj.sub_house_name]= sub_tenants.filter(sub_house_tenant_FK=obj.id)
                self.subid_with_kwh[obj.sub_house_name]=obj.id

        if _names_with_kwh:
            return self.tenants_name_with_kwh

        if _subid_with_kwh:
            return self.subid_with_kwh

        if _names_without_kwh:
            return self.tenants_name_without_kwh

        if _subid_without_kwh:
            return self.subid_without_kwh
    # 3
    def create_range_date_by_tenant(self, request=None, *args, **kwargs):
        """
            Colocar o range(inicio ate o fim) de permanencia do morador em um dicionario do morador
            Insert a range(start to end) to a dictionary for each tenant
            Example: 
            Given data for Jonh--> start_date= 2021-05-01 end_date= 2021-05-30
            The range data for Jonh is -->2021-05-01, 2021-05-02, 2021-05-03,....,2021-05-30
        """
        #=======xxxxx Main House xxxx===========
        tenants = self.tenants_main_house
        self.dict_date_range_for_tenants_without_kwh = dict()
        
        self.dict_date_range_for_tenants_without_kwh= {
            str('main'):{
                str(self.house_name_main_house): {
                        str(t1.house_tenant): {
                            str('dates'): [t1.start_date + timedelta(days=x) for x in range(t1.days)],
                        }for t1 in tenants
                    }
            }
        }
        # print(f"-->>{self.dict_date_range_for_tenants_without_kwh}")
        
        #=======xxxxx Range Sub Without kwh which will belongs to the Main house xxxx===========
        sub_tenants = self.tenants_sub_house
        subids_without_kwh = self.subid_without_kwh
        #{"Naira's House": 14}--> Example of subids_without_kwh
        
        self.dict_date_range_for_tenants_without_kwh['main'].update({
            str(name): {
                    str(sub_t1_names) : {
                        str('dates'): [sub_t1_names.sub_start_date + timedelta(days=x) for x in range(sub_t1_names.sub_days)],
                    }for sub_t1_names in sub_tenants.filter(sub_house_tenant_FK= subid_without_kwh)
                }for name, subid_without_kwh in subids_without_kwh.items()
            }
        )
        """[to_remove]
            to_remove contains sub houses without any data. It happens, because the user has registered only the name of the sub house
            I had to remove it, otherwise it will affects the calculation of the bill.
        """
        to_remove= str()
        for key, value in self.dict_date_range_for_tenants_without_kwh['main'].items():
            if not value:
                to_remove = str(key)
        if to_remove:
            del self.dict_date_range_for_tenants_without_kwh['main'][to_remove]
        
        """[to_remove]"""

        #=======xxxxx Range Sub With Kwh xxxx===========
        self.dict_date_range_for_tenants_with_kwh = dict()
        sub_tenants = self.tenants_sub_house
        subids_with_kwh = self.subid_with_kwh
        self.dict_date_range_for_tenants_with_kwh.update({
            str(name): {
                    str(sub_t1_names) : {
                        str('dates'): [sub_t1_names.sub_start_date + timedelta(days=x) for x in range(sub_t1_names.sub_days)],
                    }for sub_t1_names in sub_tenants.filter(sub_house_tenant_FK= subid_with_kwh)
                }for name, subid_with_kwh in subids_with_kwh.items()
            }
        )
        # print(f"--->>{self.dict_date_range_for_tenants_with_kwh}")




    def value_by_day(self, _without_kwh=False, _with_kwh=False, *args, **kwargs):
        #Preciso separar por dia tbm, porem tenho que descobrir como criar variavaeis com   os valores de cada sub house com kwh cadastrados.
        getcontext().prec = 8
        if _without_kwh:
            self.value_by_day_without_kwh = dict()
            amount_bill_without_kwh = self.new_amount_main_bill
            days_bill = self.days_bill_main_house
            self.value_by_day_without_kwh = Decimal(amount_bill_without_kwh)/days_bill
            return self.value_by_day_without_kwh

        if _with_kwh:
            self.value_by_day_with_kwh = dict()
            subid_with_kwh = self.subid_with_kwh
            days_bill = self.days_bill_main_house
            for nameA in subid_with_kwh:
                for nameB, value in self.amount_by_sub_houses_with_kwh.items():
                    if str(nameA) == str(nameB):
                        # print(f'nameA: {nameA} - value: {value}\n')
                        self.value_by_day_with_kwh.update({nameA : Decimal(value)/days_bill})
                    
            # print(f"value_by_day_with_kwh--> {value_by_day_with_kwh}")
            return self.value_by_day_with_kwh

    def get_tenants_by_day(self,request=None, _get_date= None, _both = False,_with_kwh=False, _without_kwh=False, *args, **kwargs):
        """
            Retorna e Filtra quais sao os tenants que estao na casa de acordo com a data enviada
            Return and Filter which tenants how is in the house by date sent.
            Return data like this --> {datetime.date(2021, 3, 14): {'Daiane', 'Nathalia', 'Eugenio', 'Elizagela', 'Ellen', 'José'}}
        """
        date_bill_verification_by_day = _get_date
        
        #START get_tenants_by_day without kwh
        if _without_kwh:
            data_dict_date_by_day_without_kwh = self.dict_date_range_for_tenants_without_kwh
            end =dict()
            data_set_tenants_by_day_without_kwh = set()
            left_over_without_kwh = set()
            mount_without_kwh = str()
            for main, houses_data in data_dict_date_by_day_without_kwh.items():
                data_set_tenants_by_day_without_kwh.clear()
                # left_over_without_kwh.clear()
                for house_name, tenant_name_and_dates in houses_data.items():
                    data_set_tenants_by_day_without_kwh.clear()
                    for tenant_name, dates in tenant_name_and_dates.items():
                        if date_bill_verification_by_day in dates['dates']:
                            data_set_tenants_by_day_without_kwh.add(str(tenant_name))
                        else:
                            mount_without_kwh = f'left_{house_name}_{date_bill_verification_by_day}'
                            data_set_tenants_by_day_without_kwh.add(mount_without_kwh)

                    if data_set_tenants_by_day_without_kwh:
                        if len(data_set_tenants_by_day_without_kwh) > 1 and mount_without_kwh in data_set_tenants_by_day_without_kwh:
                            data_set_tenants_by_day_without_kwh.discard(mount_without_kwh)
                        end.update({
                            str(house_name):{
                                str(date_bill_verification_by_day): [x for x in data_set_tenants_by_day_without_kwh],
                            },
                        })
                    
            # print(f'{end}\n')
            return end  
            
        #END get_tenants_by_day without kwh

        #START get_tenants_by_day with kwh
        if _with_kwh:
            range_dates_tenants_with_kwh = self.dict_date_range_for_tenants_with_kwh
            # print(f'sub_houses--> {sub_houses}')
            end =dict()
            data_set_tenants_by_day_with_kwh = set()
            left_over_with_kwh = set()
            mount_with_kwh = str()
            for house_name, tenant_name_and_dates in range_dates_tenants_with_kwh.items():
                # print(f'{house_name}-->{tenant_name_and_dates}\n')
                data_set_tenants_by_day_with_kwh.clear()
                left_over_with_kwh.clear()
                for tenant_name, dates in tenant_name_and_dates.items():
                    # print(f'{house_name}-->{tenant_name}')
                    if date_bill_verification_by_day in dates['dates'] :
                        data_set_tenants_by_day_with_kwh.add(str(tenant_name))
                    else:
                        mount_with_kwh = f'left_{house_name}_{date_bill_verification_by_day}'
                        data_set_tenants_by_day_with_kwh.add(mount_with_kwh)
                        # left_over_with_kwh.add(f'left_{house_name} - {tenant_name} - {date_bill_verification_by_day}')

                if data_set_tenants_by_day_with_kwh:
                    # if left_over_with_kwh:
                    #     data_set_tenants_by_day_with_kwh.update(left_over_with_kwh)
                    if len(data_set_tenants_by_day_with_kwh) > 1 and mount_with_kwh in data_set_tenants_by_day_with_kwh:
                            data_set_tenants_by_day_with_kwh.discard(mount_with_kwh)
                    end.update({
                            str(house_name):{
                                str(date_bill_verification_by_day): [x for x in data_set_tenants_by_day_with_kwh],
                            },
                        })
                # else:
                #     end.update({f"left_over_with_kwh_{house_name}":[x for x in left_over_with_kwh if x.startswith(f'left_{house_name}')]})
            
            # print(f'{end}\n')
            return end

        #START get_tenants_by_day get both
        if _both:
            #========================== Without Kilowatts =================================================
            data_dict_date_by_day_without_kwh = self.dict_date_range_for_tenants_without_kwh
            end =dict()
            data_set_tenants_by_day_without_kwh = set()
            left_over_without_kwh = set()

            for main, houses_data in data_dict_date_by_day_without_kwh.items():
                data_set_tenants_by_day_without_kwh.clear()
                # left_over_without_kwh.clear()
                for house_name, tenant_name_and_dates in houses_data.items():
                    # left_over_without_kwh.clear()
                    for tenant_name, dates in tenant_name_and_dates.items():
                        if date_bill_verification_by_day in dates['dates']:
                            data_set_tenants_by_day_without_kwh.add(str(tenant_name))
                        else:
                            left_over_without_kwh.add(f'left_{house_name} - {tenant_name} - {date_bill_verification_by_day}')
                            # print(f"House: {house_name} Tenant: {tenant_name} Date: {date_bill_verification_by_day}")
                    
                if data_set_tenants_by_day_without_kwh:
                    # print(f"House: {house_name} Tenant: {tenant_name} Date: {date_bill_verification_by_day}")
                    if left_over_without_kwh:
                        data_set_tenants_by_day_without_kwh.update(left_over_without_kwh)
                    end.update({str(house_name):[x for x in data_set_tenants_by_day_without_kwh]})
                    # if left_over_without_kwh:
                    #     end.update({"left_over_without_kwh":left_over_without_kwh})
                else:
                    end.update({f"left_over_without_kwh":[x for x in left_over_without_kwh]})
            #========================== With Kilowatts =================================================
            range_dates_tenants_with_kwh = self.dict_date_range_for_tenants_with_kwh
            # print(f'sub_houses--> {sub_houses}')
            end =dict()
            data_set_tenants_by_day_with_kwh = set()
            left_over_with_kwh = set()
            
            for house_name, tenant_name_and_dates in range_dates_tenants_with_kwh.items():
                # print(f'{house_name}-->{tenant_name_and_dates}\n')
                data_set_tenants_by_day_with_kwh.clear()
                left_over_with_kwh.clear()
                for tenant_name, dates in tenant_name_and_dates.items():
                    # print(f'{house_name}-->{tenant_name}')
                    if date_bill_verification_by_day in dates['dates'] :
                        data_set_tenants_by_day_with_kwh.add(str(tenant_name))
                    else:
                        left_over_with_kwh.add(f'left_{house_name} - {tenant_name} - {date_bill_verification_by_day}')

                if data_set_tenants_by_day_with_kwh:
                    if left_over_with_kwh:
                        data_set_tenants_by_day_with_kwh.update(left_over_with_kwh)
                    end.update({str(house_name):[x for x in data_set_tenants_by_day_with_kwh]})
                else:
                    end.update({f"left_over_with_kwh_{house_name}":[x for x in left_over_with_kwh if x.startswith(f'left_{house_name}')]})

            return end

        #END get_tenants_by_day get both

    def get_tenants_by_name(self, tenant_name=None, request=None, *args, **kwargs): 
        """
        #Retorna e Filtra quais foram os tenants que estavam com o Tenant enviado e returna todos eles mostrando em que data ele esteve junto.
        #Return and Filter which tenants was toguther with the tenant sent by parametrs and return all of them with your respectve date.
        """ 
         
        data_set_bill = dict()
        data_dict_tenants = dict()
        tenant_name_to_filter = {str(tenant_name)}#eu preciso colocar algum nome para funcionar
        
        for date in self.range_dates_bill:
            data_dict_tenants = self.get_tenants_by_day(_get_date=date)
            if tenant_name_to_filter.issubset(data_dict_tenants[date]):#Is verifired if tenant_name_to_filter be part of the data_dict_tenants into the date
                data_set_bill[date] = data_dict_tenants[date] #- tenant_name_to_filter

        #{datetime.date(2021, 5, 10): {'Daiane', 'Jamile', 'Ellen', 'José', 'Eugenio', 'Nathalia', 'Elizagela'}}
        return data_set_bill

    def filter_all_tenant_from_bill_period(self, _without_kwh=False, _with_kwh=False, request=None, *args, **kwargs):
        """
            Parameters: date - Format(YYYY-MM-DD)
            Retorna e Filtra quais sao os moradores em cada dia da conta
            Return and Filter each tenant into each day's bill
        """          
        if _without_kwh:
            data_dict_from_bill_period_without_kwh = dict()
            for enum, each_date in enumerate(self.range_dates_bill,1):
                data_dict_from_bill_period_without_kwh[enum] = self.get_tenants_by_day(_get_date=each_date, _without_kwh= True)
            return data_dict_from_bill_period_without_kwh
        
        if _with_kwh:
            data_dict_from_bill_period_with_kwh = dict()
            for enum, each_date in enumerate(self.range_dates_bill,1):
                data_dict_from_bill_period_with_kwh[enum] = self.get_tenants_by_day(_get_date=each_date, _with_kwh= True)
            # print(f"{data_dict_from_bill_period_with_kwh}")
            return data_dict_from_bill_period_with_kwh

        #57: {datetime.date(2021, 5, 9): {'Daiane', 'Elizagela', 'José', 'Ellen', 'Nathalia', 'Eugenio'}}

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
        filter_all_tenant_from_bill_period = self.filter_all_tenant_from_bill_period(_without_kwh=True)
        # print(f"--> {filter_all_tenant_from_bill_period}")
        #============== Start Calcs ======================================================
        #Step -1
        days_value_one_house_one_bill = self.value_by_day(_without_kwh=True)
        #Steds -2,3,4,5,6
        tenants_main_house = self.tenants_main_house
        total_by_each_tenant = dict()
        total_by_each_tenant_converted =  dict()
        
        house_name_main_house = self.house_name_main_house
        getcontext().prec = 8 #manter alta precisao, pois no somatorio sera necessario.
        rounded = 3
        A = list()
        for day_number, AB in filter_all_tenant_from_bill_period.items():# 3-->{'names': {'Sebastiao Correia', 'Laura Sophia'}} or 29-->{'left_over_without_kwh': {'Ebenezer Terrance 18 - 2021-01-29': '0', "Naira's House - 2021-01-29": '0'}}
            # print(f"{day_number}-->{AB}")
            for house_name, data in AB.items():
                # A.clear()
                for date, names in data.items():
                    # print(f"day: {day_number} {house_name}: {date}: {names} Size: {len(names)}\n")
                    if len(AB)>=2:#para fazer a uniao dos nomes em um data so
                        # print(f"day: {day_number} {house_name}: {date}: {names} Size: {len(names)}\n")
                        A = names + A
                        break
                    if len(AB)==1:
                        #Step -2
                        check_zero = (1 if not len(names) else len(names))
                        #Step -3
                        v = Decimal(days_value_one_house_one_bill) / check_zero
                        #Step -4
                        # names = [name for name in date.items()]
                        step_3 = { name : v for name in names}
                        # print(f"day: {day_number} step_3: {step_3}\n")
                        #Step -5
                        total_by_each_tenant = Counter(step_3) + Counter(total_by_each_tenant)
                        #Step -6
                        total_by_each_tenant_converted['all'] = {key : value for key, value in total_by_each_tenant.items() if not key.startswith('left')}#tiver que converter, pois v estava em Decimal Class
                        total_by_each_tenant_converted['Left_Over_without_kwh'] = {key : value for key, value in total_by_each_tenant.items() if key.startswith('left')}
            if len(AB)>=2:
                #Step -2
                check_zero = (1 if not len(A) else len(A))
                #Step -3
                v = Decimal(days_value_one_house_one_bill) / check_zero
                #Step -4
                # names = [name for name in date.items()]
                step_3 = { name : v for name in A}
                # print(f"day: {day_number} step_3: {step_3}\n")
                #Step -5
                total_by_each_tenant = Counter(step_3) + Counter(total_by_each_tenant)
                #Step -6
                total_by_each_tenant_converted['all'] = {key : value for key, value in total_by_each_tenant.items() if not key.startswith('left')}#tiver que converter, pois v estava em Decimal Class
                total_by_each_tenant_converted['Left_Over_without_kwh'] = {key : value for key, value in total_by_each_tenant.items() if key.startswith('left')}
                # print(f"Total: {total_by_each_tenant}\n")
                A.clear()
                    #Step -7
        # print(f"{total_by_each_tenant}\n")
        # print(f"{total_by_each_tenant_converted['Left_Over_without_kwh']}\n")
        #================================= 
        #Step -8
        sub_tenants_filtered_without_kwh= self.tenants_name_without_kwh

        #Step -9
         #--> Main Houses Data <---
        total_by_each_tenant_converted['main_house'] = {
            str(house_name_main_house) : {
                str(each_name) : {
                    str('value'): f"€{round(total_by_each_tenant_converted['all'].pop(str(each_name)),rounded)}",
                    str('date'): f'{each_name.start_date} to {each_name.end_date}',
                    str('days'): f'{each_name.days}',
                }for each_name in tenants_main_house
            }#there is no another main house, because there is just one by each views(one PK)
        }
        #--> Sub Houses Data without <---        
        total_by_each_tenant_converted['sub_house_without'] = {
            str(sub_house_name) : {
                str(each_name) : {
                    str('value'): f'€{round(total_by_each_tenant_converted["all"].pop(str(each_name)),rounded)}',
                    str('date'): f'{each_name.sub_start_date} to {each_name.sub_end_date}',
                    str('days'): f'{each_name.sub_days}',
                    }for each_name in sub_tenants_names#should be all sub tenants
                }for sub_house_name, sub_tenants_names in sub_tenants_filtered_without_kwh.items()#should be only sub_houses_name
            }#there are some possibilities which we can have multiple sub house it means multiples sub_pk's
        
        #--> Left Houses Data <---
        if total_by_each_tenant_converted['Left_Over_without_kwh']:
            total_by_each_tenant_converted['left_over1'] = {
                str(key) : {
                    str('left_over1') : f'€{round(sum(values_dict.values()),rounded)}',
                    str('days_left_over') : f'{len(values_dict)}',
                    str('details_date'): values_dict,
                }for key, values_dict in total_by_each_tenant_converted.items() if key.startswith('Left_Over_without_kwh')
            }
            
            # print([{key:value} for key, value in total_by_each_tenant_converted.items() if key.startswith('Left_Over_without_kwh')])
            # total_by_each_tenant_converted.pop('Left_Over_without_kwh')

        # total_by_each_tenant_converted.pop('all')

        #Step -10
        total_by_each_tenant_converted['kwh'] = self.kwh_main_house
        total_by_each_tenant_converted['bill_value'] = f'€{self.amount_bill_main_house}'
        total_by_each_tenant_converted['period_bill'] = f'{self.start_date_bill_main_house} to {self.end_date_bill_main_house}'
        total_by_each_tenant_converted['user'] = self.user_main_house
        total_by_each_tenant_converted['new_amount'] = f'€{round(self.new_amount_main_bill,3)}'
        total_by_each_tenant_converted['new_main_kwh'] = self.new_main_kwh

        #Step -10
        # getcontext().prec = 5 #Reduz a precisao um pouco pois nao sera mais necessario, uma vez que os valores ja teve sua alta precisao
        # total_bill = Decimal(sum(total_by_each_tenant.values()))
        # print(total_bill)


        #Validations
        """
            Reminds: Create validations
        """
        #Steps -11
   
        return total_by_each_tenant_converted

    def calc_2(self, request=None, *args, **kwargs):
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
            #fill some elements from all tenants from bill period
            filter_all_tenant_from_bill_period = self.filter_all_tenant_from_bill_period(_with_kwh=True)
            #============== Start Calcs ======================================================
            #Step -1
            days_value_one_house_one_bill = self.value_by_day(_with_kwh=True)
            #Steds -2,3,4,5,6
            total_by_each_tenant = dict()
            total_by_each_tenant_converted =  dict()
            
            getcontext().prec = 8 #manter alta precisao, pois no somatorio sera necessario.
            rounded = 3
            A = list()
            for house_name_1, value in days_value_one_house_one_bill.items():
                for day_number, AB in filter_all_tenant_from_bill_period.items():# 3-->{'names': {'Sebastiao Correia', 'Laura Sophia'}} or 29-->{'left_over_without_kwh': {'Ebenezer Terrance 18 - 2021-01-29': '0', "Naira's House - 2021-01-29": '0'}}
                    # print(f"{day_number}-->{AB}")
                    for house_name_2, data in AB.items(): #{house name):{tenant_names}}
                        for date, names in data.items():
                            if (house_name_1 == house_name_2) or (house_name_2 == f'left_over_with_kwh_{house_name_1}'):
                                # print(f"day: {day_number} House: {house_name_2} Tenants: {names} Size: {len(names)} Value: {value}\n")
                                if len(AB)>=2:#para fazer a uniao dos nomes em um data so
                                    A = names + A
                                    break
                                elif len(AB)==1:
                                    #Step -2
                                    check_zero = (1 if not len(names) else len(names))
                                    #Step -3
                                    v = Decimal(value) / check_zero
                                    #Step -4
                                    # names = [name for name in date.items()]
                                    step_3 = { name : v for name in names}
                                    # print(f"day: {day_number} step_3: {step_3}\n")
                                    #Step -5
                                    total_by_each_tenant = Counter(step_3) + Counter(total_by_each_tenant)
                                    #Step -6
                                    total_by_each_tenant_converted['all'] = {key : value for key, value in total_by_each_tenant.items() if not key.startswith('left')}#tiver que converter, pois v estava em Decimal Class
                                    total_by_each_tenant_converted['Left_Over_with_kwh'] = {key : value for key, value in total_by_each_tenant.items() if key.startswith('left')}
                    if len(AB)>=2:
                        #Step -2
                        check_zero = (1 if not len(A) else len(A))
                        #Step -3
                        v = Decimal(value) / check_zero
                        #Step -4
                        # names = [name for name in date.items()]
                        step_3 = { name : v for name in A}
                        # print(f"day: {day_number} step_3: {step_3}\n")
                        #Step -5
                        total_by_each_tenant = Counter(step_3) + Counter(total_by_each_tenant)
                        #Step -6
                        total_by_each_tenant_converted['all'] = {key : value for key, value in total_by_each_tenant.items() if not key.startswith('left')}#tiver que converter, pois v estava em Decimal Class
                        total_by_each_tenant_converted['Left_Over_with_kwh'] = {key : value for key, value in total_by_each_tenant.items() if key.startswith('left')}
                        A.clear()
            #================================= 
            # print(f"left: {total_by_each_tenant_converted['Left_Over_without_kwh']}")
            #Step -8
            sub_tenants_filtered_with_kwh= self.tenants_name_with_kwh

            #Step -9
            #--> Sub Houses Data without <---        
            total_by_each_tenant_converted['sub_house_with'] = {
                str(sub_house_name) : {
                    str(each_name) : {
                        str('tenant_value'): f'€{round(total_by_each_tenant_converted["all"].pop(str(each_name)),rounded)}',
                        str('date'): f'{each_name.sub_start_date} to {each_name.sub_end_date}',
                        str('days'): f'{each_name.sub_days}',
                        str('kwh_infor'): {int(x.sub_kwh) for x in self.sub_kwh_sub_house if str(sub_house_name) == str(x.sub_house_kwh_FK)},
                        str('bill_value'): f"€{round([Decimal(value) for name, value in self.amount_by_sub_houses_with_kwh.items() if str(sub_house_name) == str(name)].pop(), rounded)}",
                    }for each_name in sub_tenants_names#should be all sub tenants
                }for sub_house_name, sub_tenants_names in sub_tenants_filtered_with_kwh.items()#should be only sub_houses_name
            }#there are some possibilities which we can have multiple sub house it means multiples sub_pk's

            #--> Left Houses Data <---            
            temporary_left = [ {key:value} for key, value in total_by_each_tenant_converted.items() if key.startswith('Left_Over_with_kwh')]
            if temporary_left:
                total_by_each_tenant_converted['left_over1'] = {
                    str(f"{key.replace('Left_Over_with_kwh_','')}") : {
                        str('left_over1') : f'€{round(sum(value.values()),rounded)}',
                        str('days_left_over') : f'{len(value.values())}',
                        str('details_date'): value,
                    }for key, value in total_by_each_tenant_converted.items() if key.startswith('Left_Over_with_kwh')
                }
            # print([ {x.replace('Left_Over_with_kwh_',''):y} for x, y in total_by_each_tenant_converted.items() if x.startswith('Left_Over_with_kwh')])
            # total_by_each_tenant_converted.pop('all')

            #Validations
            """
                Reminds: Create validations
            """
            #Steps -11
    
            return total_by_each_tenant_converted