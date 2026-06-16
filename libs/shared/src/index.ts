// @sharepay/shared
// Shared domain types, DTOs, and small utilities for SharePay.
// Strict types to ensure calc parity and API contracts.

export interface DateRange {
  start: string; // YYYY-MM-DD
  end: string;
}

export interface Tenant {
  id: number | string;
  name: string; // Capitalized as in original
  startDate: string;
  endDate: string;
  days: number;
}

export interface SubTenant extends Tenant {}

export interface Bill {
  amount: number; // decimal stored as number for transport; use Decimal internally for calc
  startDate: string;
  endDate: string;
  days: number;
}

export interface Kilowatt {
  kwh: number;
  lastRead?: number;
  read?: number;
}

export interface SubKilowatt {
  subHouseId: number | string;
  subHouseName: string;
  subKwh: number;
}

export interface HouseData {
  id: number | string;
  houseName: string;
  userId?: number | string;
  bill: Bill;
  kwh: number;
  tenants: Tenant[];
  subHouses: Array<{
    id: number | string;
    name: string;
    meter?: number;
  }>;
  subKwhs: SubKilowatt[];
  subTenants: Array<SubTenant & { subHouseId: number | string; subHouseName: string }>;
}

export interface CalcResult {
  kwh: number;
  bill_value: string; // '€xx.xx'
  period_bill: string;
  user?: any;
  new_amount: string;
  new_main_kwh: number;
  main_house: Record<string, Record<string, { value: string; date: string; days: string }>>;
  sub_house_without: Record<string, Record<string, { value: string; date: string; days: string }>>;
  sub_house_with?: Record<string, Record<string, {
    tenant_value: string;
    date: string;
    days: string;
    kwh_infor: number[];
    bill_value: string;
  }>>;
  left_over1?: Record<string, {
    left_over1: string;
    days_left_over: string;
    details_date: Record<string, number>;
  }>;
  [key: string]: any; // allow left over variants for exact shape match
}

export function capitalizeName(name: string): string {
  if (!name) return name;
  return name
    .split(/\s+/)
    .map((s) => s.charAt(0).toUpperCase() + s.slice(1).toLowerCase())
    .join(' ')
    .trim();
}

export function daysBetween(start: string, end: string): number {
  const s = new Date(start);
  const e = new Date(end);
  const diff = Math.floor((e.getTime() - s.getTime()) / (1000 * 3600 * 24));
  return diff;
}

// Build array of dates (inclusive) for range used by core logic
export function dateRangeArray(start: string, days: number): Date[] {
  const dates: Date[] = [];
  const base = new Date(start);
  for (let i = 0; i < days; i++) {
    const d = new Date(base);
    d.setDate(d.getDate() + i);
    dates.push(d);
  }
  return dates;
}

export function formatEuro(n: number | string): string {
  const num = typeof n === 'string' ? parseFloat(n) : n;
  return `€${num.toFixed(3)}`; // match original round( ,3) + €
}
