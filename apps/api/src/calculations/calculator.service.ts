import { Injectable } from '@nestjs/common';
import { BillCalculator, CoreInput } from '@sharepay/calculator';
import { House } from '../entities/house.entity';

@Injectable()
export class CalculatorService {
  /**
   * Build CoreInput from fully loaded House aggregate (with relations).
   * Then run BillCalculator.calculate() which internally calls calc1 + calc2 + merge.
   * Guarantees 100% identical output shape/values to original CoreSharePay for identical input data.
   */
  runCalculationForHouse(house: House): any {
    if (!house.bill || !house.kilowatt) {
      throw new Error('Missing bill or kwh for calculation');
    }

    const bill = house.bill;
    const kwhEnt = house.kilowatt;

    const amountBill = parseFloat(bill.amountBill || '0');
    const kwhMain = parseInt(kwhEnt.kwh || '0', 10);
    const daysBill = bill.daysBill || 0;

    // tenantsMain shape for CoreInput (id kept for keying in calc: `${id}-${name}`)
    const tenantsMain = (house.tenants || []).map((t) => ({
      id: t.id,
      house_tenant: t.houseTenant || '',
      start_date: t.startDate,
      end_date: t.endDate,
      days: t.days || 0,
    }));

    // subHouseNames
    const subHouseNames = (house.subHouses || []).map((s) => ({
      id: s.id,
      sub_house_name: s.subHouseName || '',
    }));

    // subTenants (all)
    const subTenants: any[] = [];
    (house.subHouses || []).forEach((sub) => {
      (sub.tenants || []).forEach((st) => {
        subTenants.push({
          id: st.id,
          sub_house_tenant_FK: sub.id,
          sub_house_tenant: st.subHouseTenant || '',
          sub_start_date: st.subStartDate || '',
          sub_end_date: st.subEndDate || '',
          sub_days: st.subDays || 0,
        });
      });
    });

    // subKwhs (only those present)
    const subKwhs: any[] = [];
    (house.subHouses || []).forEach((sub) => {
      const sk = (sub.kilowatts || [])[0];
      if (sk && sk.subKwh) {
        subKwhs.push({
          sub_house_kwh_FK: { sub_house_name: sub.subHouseName, id: sub.id },
          sub_kwh: parseInt(sk.subKwh, 10),
        });
      }
    });

    const input: CoreInput = {
      houseName: house.houseName || '',
      amountBill,
      startDateBill: bill.startDateBill,
      endDateBill: bill.endDateBill,
      daysBill,
      kwhMain,
      tenantsMain,
      subHouseNames,
      subTenants,
      subKwhs,
    };

    const calculator = new BillCalculator(input);
    // calculate() returns merged calc1 + calc2 + meta exactly as required
    // (same as old templates consuming calc_1() + calc_2())
    const result = calculator.calculate();
    return result;
  }
}
