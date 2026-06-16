import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { BillCalculator, CoreInput } from '@sharepay/calculator';
import { formatEuro } from '@sharepay/shared';

export interface House {
  id: number;
  house_name: string;
  user_id: number;
  bill?: { amount_bill: string; start_date_bill: string; end_date_bill: string; days_bill: number };
  kwh?: { kwh: number; last_read_kwh?: number; read_kwh?: number };
  tenants: Array<{ id: number; house_tenant: string; start_date: string; end_date: string; days: number }>;
  subHouses: Array<{
    id: number;
    sub_house_name: string;
    sub_kwh?: { sub_kwh: number };
    sub_tenants: Array<{ id: number; sub_house_tenant: string; sub_start_date: string; sub_end_date: string; sub_days: number }>;
  }>;
}

const STORAGE_KEY = 'sharepay_houses_v1';

@Injectable({ providedIn: 'root' })
export class HousesService {
  private housesSubject = new BehaviorSubject<House[]>(this.load());
  houses$ = this.housesSubject.asObservable();

  private nextId = Date.now();

  private load(): House[] {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      return raw ? JSON.parse(raw) : [];
    } catch { return []; }
  }

  private persist(houses: House[]) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(houses));
    this.housesSubject.next(houses);
  }

  getAll(): House[] { return this.housesSubject.value; }

  getById(id: number): House | undefined {
    return this.getAll().find(h => h.id === id);
  }

  createHouse(name: string): House {
    const house: House = {
      id: this.nextId++,
      house_name: name.trim(),
      user_id: 1,
      tenants: [],
      subHouses: []
    };
    const all = [...this.getAll(), house];
    this.persist(all);
    return house;
  }

  updateHouseName(id: number, name: string) {
    const all = this.getAll().map(h => h.id === id ? { ...h, house_name: name.trim() } : h);
    this.persist(all);
  }

  deleteHouse(id: number) {
    const all = this.getAll().filter(h => h.id !== id);
    this.persist(all);
  }

  // Bill: amount + dates. Replicate validations from HouseBillModelForm + clean
  setBill(houseId: number, amount: string, start: string, end: string): { ok: boolean; errors?: string[] } {
    const errors: string[] = [];
    const amt = parseFloat(amount.replace(',', '.'));
    if (isNaN(amt) || amt <= 0) errors.push('Should be a positive number!');
    if (amt === 0) errors.push('It cannot be Zero!');
    const s = new Date(start); const e = new Date(end);
    const today = new Date(); today.setHours(0,0,0,0);
    if (s > e) errors.push('Start_Date has to be smaller than End_date');
    if (s.getTime() === e.getTime()) errors.push('It cannot be Equal');
    if (s > today) errors.push('Check if date is out of range.');
    if (e > today) errors.push('Check if date is out of range.');
    if (errors.length) return { ok: false, errors };

    const days = Math.floor((e.getTime() - s.getTime()) / 86400000);
    const all = this.getAll().map(h => {
      if (h.id !== houseId) return h;
      return {
        ...h,
        bill: { amount_bill: amt.toFixed(2), start_date_bill: start, end_date_bill: end, days_bill: days },
        // per original: changing bill clears tenants
        tenants: [],
        subHouses: h.subHouses.map(sh => ({ ...sh, sub_tenants: [] }))
      };
    });
    this.persist(all);
    return { ok: true };
  }

  // Kwh: reads or direct. Replicate HouseKilowattModelForm validations
  setKwh(houseId: number, kwh?: number, last?: number, read?: number): { ok: boolean; errors?: string[] } {
    const errors: string[] = [];
    let computedKwh = kwh;
    if (last != null && read != null) {
      if (last > read) errors.push('Should be greatter than previous Kw/h read');
      else computedKwh = read - last;
    }
    if (computedKwh == null || computedKwh < 0) errors.push('Only Positive Number! or Insert Kilowatts!');
    if (errors.length) return { ok: false, errors };

    const all = this.getAll().map(h => h.id === houseId ? { ...h, kwh: { kwh: Math.floor(computedKwh!), last_read_kwh: last, read_kwh: read } } : h);
    this.persist(all);
    return { ok: true };
  }

  // Tenants main: name + dates. Replicate HouseTenant validations + bill range
  addTenant(houseId: number, name: string, start: string, end: string): { ok: boolean; errors?: string[] } {
    const house = this.getById(houseId);
    if (!house || !house.bill) return { ok: false, errors: ['Bill must be set first'] };
    const errors: string[] = [];
    const capName = this.capitalize(name);
    if (!capName) errors.push('Tenant name required');
    const bs = new Date(house.bill.start_date_bill); const be = new Date(house.bill.end_date_bill);
    const s = new Date(start); const e = new Date(end);
    if (s < bs) errors.push(`Out of Range - ${house.bill.start_date_bill}`);
    if (e > be) errors.push(`Out of Range - ${house.bill.end_date_bill}`);
    const days = Math.floor((e.getTime() - s.getTime()) / 86400000);
    if (days < 0) errors.push('Start_Date has to be smaller than End_date');
    if (days === 0) errors.push('It cannot be Equal');
    if (errors.length) return { ok: false, errors };

    const t = { id: Date.now(), house_tenant: capName, start_date: start, end_date: end, days };
    const all = this.getAll().map(h => h.id === houseId ? { ...h, tenants: [...h.tenants, t] } : h);
    this.persist(all);
    return { ok: true };
  }

  removeTenant(houseId: number, tenantId: number) {
    const all = this.getAll().map(h => h.id === houseId ? { ...h, tenants: h.tenants.filter(t => t.id !== tenantId) } : h);
    this.persist(all);
  }

  // Sub houses
  addSubHouse(houseId: number, name: string): { ok: boolean; errors?: string[] } {
    const errors: string[] = [];
    const cap = this.capitalize(name);
    if (!cap || cap.length > 25) errors.push('Ensure House Name has max 25 characters');
    if (errors.length) return { ok: false, errors };
    const sub = { id: Date.now(), sub_house_name: cap, sub_tenants: [] as any[] };
    const all = this.getAll().map(h => h.id === houseId ? { ...h, subHouses: [...h.subHouses, sub] } : h);
    this.persist(all);
    return { ok: true };
  }

  deleteSubHouse(houseId: number, subId: number) {
    const all = this.getAll().map(h => h.id === houseId ? { ...h, subHouses: h.subHouses.filter(s => s.id !== subId) } : h);
    this.persist(all);
  }

  setSubKwh(houseId: number, subId: number, subKwh: number): { ok: boolean; errors?: string[] } {
    const house = this.getById(houseId);
    const errors: string[] = [];
    if (!house || !house.kwh) { errors.push('Main house KWH must be registered first'); return { ok: false, errors }; }
    const mainKwh = house.kwh.kwh;
    let sum = house.subHouses.filter(s => s.id !== subId && s.sub_kwh).reduce((acc, s) => acc + (s.sub_kwh!.sub_kwh || 0), 0);
    sum += subKwh;
    if (subKwh <= 0) errors.push('You must provide Killowatts Read');
    if (sum > mainKwh) errors.push(`The total of the Sum is ${sum} kwh, it cannot be greatter than kilowatts from the bill. Registered: Max${mainKwh} kwh`);
    if (sum === mainKwh) errors.push(`The total of the Sum of the Kilowatts is ${sum} kwh, it cannot be greatter or equal than kilowatts from the bill. Registered: Max${mainKwh} kwh`);
    if (errors.length) return { ok: false, errors };

    const all = this.getAll().map(h => {
      if (h.id !== houseId) return h;
      return {
        ...h,
        subHouses: h.subHouses.map(s => s.id === subId ? { ...s, sub_kwh: { sub_kwh: subKwh } } : s)
      };
    });
    this.persist(all);
    return { ok: true };
  }

  addSubTenant(houseId: number, subId: number, name: string, start: string, end: string): { ok: boolean; errors?: string[] } {
    const house = this.getById(houseId);
    if (!house || !house.bill) return { ok: false, errors: ['Bill required'] };
    const errors: string[] = [];
    const cap = this.capitalize(name);
    const bs = new Date(house.bill.start_date_bill); const be = new Date(house.bill.end_date_bill);
    const s = new Date(start); const e = new Date(end);
    if (s < bs) errors.push(`Out of Range- ${house.bill.start_date_bill}`);
    if (e > be) errors.push(`Out of Range- ${house.bill.end_date_bill}`);
    const d = Math.floor((e.getTime() - s.getTime()) / 86400000);
    if (d <= 0) errors.push('Start_Date has to be smaller than End_date / cannot be Equal');
    if (errors.length) return { ok: false, errors };

    const t = { id: Date.now(), sub_house_tenant: cap, sub_start_date: start, sub_end_date: end, sub_days: d };
    const all = this.getAll().map(h => {
      if (h.id !== houseId) return h;
      return {
        ...h,
        subHouses: h.subHouses.map(sh => sh.id === subId ? { ...sh, sub_tenants: [...sh.sub_tenants, t] } : sh)
      };
    });
    this.persist(all);
    return { ok: true };
  }

  removeSubTenant(houseId: number, subId: number, tId: number) {
    const all = this.getAll().map(h => {
      if (h.id !== houseId) return h;
      return {
        ...h,
        subHouses: h.subHouses.map(sh => sh.id === subId ? { ...sh, sub_tenants: sh.sub_tenants.filter(t => t.id !== tId) } : sh)
      };
    });
    this.persist(all);
  }

  // === CALC REPORT: EXACT parity with old templates using @sharepay/calculator ===
  // Returns structure matching calc_1 + calc_2 from templates + calc_main_house.html + with_kwh.html
  calculate(houseId: number): any {
    const house = this.getById(houseId);
    if (!house || !house.bill || !house.kwh) {
      return { error: 'Bill and KWH are required to calculate' };
    }

    // Build exact CoreInput shape expected by calculator
    const input: CoreInput = {
      houseName: house.house_name,
      amountBill: parseFloat(house.bill.amount_bill),
      startDateBill: house.bill.start_date_bill,
      endDateBill: house.bill.end_date_bill,
      daysBill: house.bill.days_bill,
      kwhMain: house.kwh.kwh,
      tenantsMain: house.tenants.map(t => ({
        id: t.id, house_tenant: t.house_tenant, start_date: t.start_date, end_date: t.end_date, days: t.days
      })),
      subHouseNames: house.subHouses.map(s => ({ id: s.id, sub_house_name: s.sub_house_name })),
      subTenants: house.subHouses.flatMap(s => s.sub_tenants.map(st => ({
        id: st.id, sub_house_tenant_FK: s.id, sub_house_tenant: st.sub_house_tenant,
        sub_start_date: st.sub_start_date, sub_end_date: st.sub_end_date, sub_days: st.sub_days
      }))),
      subKwhs: house.subHouses
        .filter(s => s.sub_kwh && s.sub_kwh.sub_kwh > 0)
        .map(s => ({ sub_house_kwh_FK: { sub_house_name: s.sub_house_name, id: s.id }, sub_kwh: s.sub_kwh!.sub_kwh }))
    };

    // Authoritative calc from the library (exact same logic as original Python + templates)
    const calc = new BillCalculator(input).calculate();

    // Attach a few top-level fields used in old templates for display parity
    (calc as any)['user'] = 'demo'; // placeholder like old (index signature)
    return calc;
  }

  private capitalize(n: string): string {
    if (!n) return '';
    return n.split(/\s+/).map(w => w[0]?.toUpperCase() + w.slice(1).toLowerCase()).join(' ').trim();
  }
}
