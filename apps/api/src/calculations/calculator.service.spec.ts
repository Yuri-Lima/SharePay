import { Test, TestingModule } from '@nestjs/testing';
import { CalculatorService } from './calculator.service';
import { BillCalculator } from '@sharepay/calculator';
import { House } from '../entities/house.entity';
import { HouseBill } from '../entities/house-bill.entity';
import { HouseKilowatt } from '../entities/house-kilowatt.entity';

describe('CalculatorService', () => {
  let service: CalculatorService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [CalculatorService],
    }).compile();

    service = module.get<CalculatorService>(CalculatorService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });

  it('runCalculationForHouse produces merged calc output using pure BillCalculator (parity shape)', () => {
    // Build minimal in-memory aggregate mirroring persisted entities
    const house = new House();
    house.id = 1;
    house.houseName = 'Test Main';

    const bill = new HouseBill();
    bill.amountBill = '120';
    bill.startDateBill = '2021-05-01';
    bill.endDateBill = '2021-05-31';
    bill.daysBill = 31;
    house.bill = bill;

    const kwh = new HouseKilowatt();
    kwh.kwh = '300';
    house.kilowatt = kwh;

    house.tenants = [
      { id: 1, houseTenant: 'Alice Example', startDate: '2021-05-01', endDate: '2021-05-31', days: 31 } as any,
      { id: 2, houseTenant: 'Bob Test', startDate: '2021-05-10', endDate: '2021-05-31', days: 22 } as any,
    ];

    house.subHouses = [
      {
        id: 10,
        subHouseName: 'SubA',
        kilowatts: [{ subKwh: '80' } as any],
        tenants: [
          { id: 100, subHouseTenant: 'Sara Sub', subStartDate: '2021-05-01', subEndDate: '2021-05-31', subDays: 31 } as any,
        ],
      } as any,
      {
        id: 11,
        subHouseName: 'SubB',
        kilowatts: [],
        tenants: [
          { id: 101, subHouseTenant: 'Tom Sub', subStartDate: '2021-05-05', subEndDate: '2021-05-25', subDays: 21 } as any,
        ],
      } as any,
    ];

    const result = service.runCalculationForHouse(house);

    expect(result).toBeTruthy();
    expect(result.kwh).toBe(300);
    expect(result.new_main_kwh).toBeLessThan(300);
    expect(result.new_amount).toMatch(/^€/);
    expect(result.main_house).toBeDefined();
    expect(result.sub_house_without).toBeDefined();
    expect(result.sub_house_with).toBeDefined();

    // Ensure we can also invoke the lib directly with same input shape for parity
    const directInput = {
      houseName: 'Test Main',
      amountBill: 120,
      startDateBill: '2021-05-01',
      endDateBill: '2021-05-31',
      daysBill: 31,
      kwhMain: 300,
      tenantsMain: [
        { id: 1, house_tenant: 'Alice Example', start_date: '2021-05-01', end_date: '2021-05-31', days: 31 },
        { id: 2, house_tenant: 'Bob Test', start_date: '2021-05-10', end_date: '2021-05-31', days: 22 },
      ],
      subHouseNames: [
        { id: 10, sub_house_name: 'SubA' },
        { id: 11, sub_house_name: 'SubB' },
      ],
      subTenants: [
        { id: 100, sub_house_tenant_FK: 10, sub_house_tenant: 'Sara Sub', sub_start_date: '2021-05-01', sub_end_date: '2021-05-31', sub_days: 31 },
        { id: 101, sub_house_tenant_FK: 11, sub_house_tenant: 'Tom Sub', sub_start_date: '2021-05-05', sub_end_date: '2021-05-25', sub_days: 21 },
      ],
      subKwhs: [{ sub_house_kwh_FK: { sub_house_name: 'SubA' }, sub_kwh: 80 }],
    };
    const direct = new BillCalculator(directInput).calculate();
    expect(direct.kwh).toBe(result.kwh);
  });
});
