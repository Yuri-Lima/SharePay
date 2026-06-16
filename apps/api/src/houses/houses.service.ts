import { Injectable, NotFoundException, ForbiddenException, BadRequestException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository, In } from 'typeorm';
import { capitalizeName, daysBetween } from '@sharepay/shared';
import { House } from '../entities/house.entity';
import { HouseBill } from '../entities/house-bill.entity';
import { HouseKilowatt } from '../entities/house-kilowatt.entity';
import { HouseTenant } from '../entities/house-tenant.entity';
import { SubHouse } from '../entities/sub-house.entity';
import { SubKilowatt } from '../entities/sub-kilowatt.entity';
import { SubTenant } from '../entities/sub-tenant.entity';
import { CreateHouseDto } from './dto/create-house.dto';
import { UpdateHouseDto } from './dto/update-house.dto';
import { CreateBillDto } from './dto/create-bill.dto';
import { CreateKwhDto } from './dto/create-kwh.dto';
import { CreateTenantDto } from './dto/create-tenant.dto';
import { CreateSubHouseDto } from './dto/create-sub-house.dto';
import { CreateSubKwhDto } from './dto/create-sub-kwh.dto';
import { CreateSubTenantDto } from './dto/create-sub-tenant.dto';
import { CalculatorService } from '../calculations/calculator.service';

@Injectable()
export class HousesService {
  constructor(
    @InjectRepository(House)
    private readonly housesRepo: Repository<House>,
    @InjectRepository(HouseBill)
    private readonly billsRepo: Repository<HouseBill>,
    @InjectRepository(HouseKilowatt)
    private readonly kwhsRepo: Repository<HouseKilowatt>,
    @InjectRepository(HouseTenant)
    private readonly tenantsRepo: Repository<HouseTenant>,
    @InjectRepository(SubHouse)
    private readonly subHousesRepo: Repository<SubHouse>,
    @InjectRepository(SubKilowatt)
    private readonly subKwhsRepo: Repository<SubKilowatt>,
    @InjectRepository(SubTenant)
    private readonly subTenantsRepo: Repository<SubTenant>,
    private readonly calculatorService: CalculatorService,
  ) {}

  // ============ HOUSE CRUD + OWNERSHIP ============
  async create(userId: number, dto: CreateHouseDto): Promise<House> {
    const name = capitalizeName(dto.house_name).slice(0, 25);
    if (!name) throw new BadRequestException('You must provide a House Name (up to 25 letters).');

    const house = this.housesRepo.create({
      user: { id: userId } as any,
      houseName: name,
      meter: 1,
    });
    return this.housesRepo.save(house);
  }

  async findAllForUser(userId: number): Promise<House[]> {
    return this.housesRepo.find({
      where: { user: { id: userId } },
      order: { lastUpdated: 'DESC' },
      relations: ['bill', 'kilowatt'],
    });
  }

  async findOneOwned(userId: number, id: number): Promise<House> {
    const house = await this.housesRepo.findOne({
      where: { id, user: { id: userId } },
      relations: ['bill', 'kilowatt', 'tenants', 'subHouses', 'subHouses.kilowatts', 'subHouses.tenants'],
    });
    if (!house) throw new NotFoundException('House not found or access denied');
    return house;
  }

  async findOneOwnedLight(userId: number, id: number): Promise<House> {
    const house = await this.housesRepo.findOne({ where: { id, user: { id: userId } } });
    if (!house) throw new NotFoundException('House not found or access denied');
    return house;
  }

  async update(userId: number, id: number, dto: UpdateHouseDto): Promise<House> {
    const house = await this.findOneOwnedLight(userId, id);
    if (dto.house_name !== undefined) {
      const name = capitalizeName(dto.house_name).slice(0, 25);
      if (!name) throw new BadRequestException('Invalid house name');
      house.houseName = name;
    }
    return this.housesRepo.save(house);
  }

  async remove(userId: number, id: number): Promise<void> {
    const house = await this.findOneOwnedLight(userId, id);
    await this.housesRepo.remove(house);
  }

  // ============ BILL (exactly 1 per house) ============
  async setBill(userId: number, houseId: number, dto: CreateBillDto): Promise<HouseBill> {
    const house = await this.findOneOwnedLight(userId, houseId);

    const start = dto.start_date_bill;
    const end = dto.end_date_bill;
    const days = daysBetween(start, end);
    if (days < 0) throw new BadRequestException({ start_date_bill: 'Start_Date has to be smaller than End_date', end_date_bill: 'End_Date has to be bigger than Start_date' });
    if (days === 0) throw new BadRequestException({ start_date_bill: 'It cannot be Equal', end_date_bill: 'It cannot be Equal' });

    const todayStr = new Date().toISOString().slice(0, 10);
    if (start > todayStr) throw new BadRequestException({ start_date_bill: 'Check if date is out of range.' });
    if (end > todayStr) throw new BadRequestException({ end_date_bill: 'Check if date is out of range.' });

    // Parse amount: support '1.234,56' or '1234.56' like original
    let amountStr = dto.amount_bill.replace(',', '.').replace(/[^\d.]/g, '');
    const amountNum = parseFloat(amountStr);
    if (isNaN(amountNum) || amountNum <= 0) throw new BadRequestException({ amount_bill: 'Should be a positive number!' });
    if (amountNum === 0) throw new BadRequestException({ amount_bill: 'It cannot be Zero!' });

    // Mirror destructive delete of tenants on bill date change
    const existingBill = await this.billsRepo.findOne({ where: { house: { id: houseId } } });
    const dateChanged = existingBill && (existingBill.startDateBill !== start || existingBill.endDateBill !== end);
    if (dateChanged) {
      await this.tenantsRepo.delete({ house: { id: houseId } });
      // also delete all sub tenants
      const subIds = (await this.subHousesRepo.find({ where: { house: { id: houseId } }, select: ['id'] })).map(s => s.id);
      if (subIds.length) {
        await this.subTenantsRepo.delete({ subHouse: { id: In(subIds) } });
      }
    }

    const billData = {
      house,
      amountBill: amountNum.toFixed(2),
      startDateBill: start,
      endDateBill: end,
      daysBill: days,
    };

    if (existingBill) {
      Object.assign(existingBill, billData);
      return this.billsRepo.save(existingBill);
    }
    const bill = this.billsRepo.create(billData);
    return this.billsRepo.save(bill);
  }

  async getBill(userId: number, houseId: number): Promise<HouseBill | null> {
    await this.findOneOwnedLight(userId, houseId);
    return this.billsRepo.findOne({ where: { house: { id: houseId } } });
  }

  // ============ KWH (exactly 1 per house) ============
  async setKwh(userId: number, houseId: number, dto: CreateKwhDto): Promise<HouseKilowatt> {
    const house = await this.findOneOwnedLight(userId, houseId);

    let kwhValue: number | null = null;
    if (dto.last_read_kwh && dto.read_kwh) {
      const last = parseInt(dto.last_read_kwh, 10);
      const read = parseInt(dto.read_kwh, 10);
      if (last > read) throw new BadRequestException({ read_kwh: 'Should be greatter than previous Kw/h read' });
      kwhValue = read - last;
    } else if (dto.kwh !== undefined) {
      kwhValue = parseInt(dto.kwh, 10);
      if (kwhValue < 0) throw new BadRequestException({ kwh: 'Only Positive Number!' });
    } else {
      throw new BadRequestException({ kwh: 'Insert Kilowatts!' });
    }
    if (kwhValue === null || kwhValue < 0) throw new BadRequestException({ kwh: 'Only Positive Number!' });

    const existing = await this.kwhsRepo.findOne({ where: { house: { id: houseId } } });
    const data = {
      house,
      kwh: String(kwhValue),
      lastReadKwh: dto.last_read_kwh || null,
      readKwh: dto.read_kwh || null,
    };
    if (existing) {
      Object.assign(existing, data);
      return this.kwhsRepo.save(existing);
    }
    return this.kwhsRepo.save(this.kwhsRepo.create(data));
  }

  async getKwh(userId: number, houseId: number): Promise<HouseKilowatt | null> {
    await this.findOneOwnedLight(userId, houseId);
    return this.kwhsRepo.findOne({ where: { house: { id: houseId } } });
  }

  // ============ TENANTS (main house) ============
  async addTenant(userId: number, houseId: number, dto: CreateTenantDto): Promise<HouseTenant> {
    const house = await this.findOneOwned(userId, houseId); // loads bill for validation
    const bill = house.bill;
    if (!bill) throw new BadRequestException('Bill must be set before adding tenants');

    const start = dto.start_date;
    const end = dto.end_date;
    const days = daysBetween(start, end);
    if (days <= 0) {
      throw new BadRequestException(days < 0
        ? { start_date: 'Start_Date has to be smaller than End_date', end_date: 'End_Date has to be bigger than Start_date' }
        : { start_date: 'It cannot be Equal', end_date: 'It cannot be Equal' });
    }
    // Range validation against bill period (exact mirror of form)
    if (start < bill.startDateBill) {
      throw new BadRequestException({ start_date: `Out of Range - ${bill.startDateBill}` });
    }
    if (end > bill.endDateBill) {
      throw new BadRequestException({ end_date: `Out of Range - ${bill.endDateBill}` });
    }

    const tenantName = capitalizeName(dto.house_tenant);
    const tenant = this.tenantsRepo.create({
      house,
      houseTenant: tenantName,
      startDate: start,
      endDate: end,
      days,
    });
    return this.tenantsRepo.save(tenant);
  }

  async listTenants(userId: number, houseId: number): Promise<HouseTenant[]> {
    await this.findOneOwnedLight(userId, houseId);
    return this.tenantsRepo.find({ where: { house: { id: houseId } }, order: { lastUpdated: 'DESC' } });
  }

  async updateTenant(userId: number, houseId: number, tenantId: number, dto: CreateTenantDto): Promise<HouseTenant> {
    await this.findOneOwnedLight(userId, houseId);
    const tenant = await this.tenantsRepo.findOne({ where: { id: tenantId, house: { id: houseId } } });
    if (!tenant) throw new NotFoundException('Tenant not found');
    // re-use add validation by constructing temp dto
    const bill = (await this.getBill(userId, houseId))!;
    const start = dto.start_date;
    const end = dto.end_date;
    const days = daysBetween(start, end);
    if (days <= 0) throw new BadRequestException('Invalid date range');
    if (start < bill.startDateBill || end > bill.endDateBill) throw new BadRequestException('Out of bill date range');
    tenant.houseTenant = capitalizeName(dto.house_tenant);
    tenant.startDate = start;
    tenant.endDate = end;
    tenant.days = days;
    return this.tenantsRepo.save(tenant);
  }

  async removeTenant(userId: number, houseId: number, tenantId: number): Promise<void> {
    await this.findOneOwnedLight(userId, houseId);
    const res = await this.tenantsRepo.delete({ id: tenantId, house: { id: houseId } });
    if (!res.affected) throw new NotFoundException('Tenant not found');
  }

  // ============ SUB HOUSES ============
  async addSubHouse(userId: number, houseId: number, dto: CreateSubHouseDto): Promise<SubHouse> {
    const house = await this.findOneOwnedLight(userId, houseId);
    const name = capitalizeName(dto.sub_house_name).slice(0, 25);
    const sub = this.subHousesRepo.create({
      house,
      subHouseName: name,
      subMeter: 1,
      subMainHouse: !!dto.sub_main_house,
    });
    return this.subHousesRepo.save(sub);
  }

  async listSubHouses(userId: number, houseId: number): Promise<SubHouse[]> {
    await this.findOneOwnedLight(userId, houseId);
    return this.subHousesRepo.find({ where: { house: { id: houseId } }, relations: ['kilowatts', 'tenants'] });
  }

  async removeSubHouse(userId: number, houseId: number, subId: number): Promise<void> {
    await this.findOneOwnedLight(userId, houseId);
    const res = await this.subHousesRepo.delete({ id: subId, house: { id: houseId } });
    if (!res.affected) throw new NotFoundException('Sub-house not found');
  }

  // ============ SUB KWH (1 per sub) + strict sum < main validation ============
  async setSubKwh(userId: number, houseId: number, subId: number, dto: CreateSubKwhDto): Promise<SubKilowatt> {
    await this.findOneOwnedLight(userId, houseId);
    const sub = await this.subHousesRepo.findOne({ where: { id: subId, house: { id: houseId } }, relations: ['house'] });
    if (!sub) throw new NotFoundException('Sub-house not found');

    const subKwhNum = parseInt(dto.sub_kwh, 10);
    if (isNaN(subKwhNum) || subKwhNum <= 0) {
      throw new BadRequestException({ sub_kwh: 'You must provide Killowatts Read' });
    }

    // Load main kwh
    const mainKwh = await this.kwhsRepo.findOne({ where: { house: { id: houseId } } });
    if (!mainKwh || !mainKwh.kwh) throw new BadRequestException('Main house kWh must be set first');
    const mainKwhNum = parseInt(mainKwh.kwh, 10);

    // Sum other subs excluding this one (or current if updating)
    const existingForThis = await this.subKwhsRepo.findOne({ where: { subHouse: { id: subId } } });
    const otherSubs = await this.subKwhsRepo.find({ where: { mainHouse: { id: houseId } } });
    let sum = 0;
    for (const sk of otherSubs) {
      if (sk.subHouse && sk.subHouse.id === subId) continue;
      sum += sk.subKwh ? parseInt(sk.subKwh, 10) : 0;
    }
    sum += subKwhNum;

    if (sum > mainKwhNum) {
      throw new BadRequestException({ sub_kwh: `The total of the Sum is ${sum} kwh, it cannot be greatter than kilowatts from the bill. Registreded: Max${mainKwhNum} kwh` });
    }
    if (sum === mainKwhNum) {
      throw new BadRequestException({ sub_kwh: `The total of the Sum of the Kilowatts is ${sum} kwh, it cannot be greatter or equal than kilowatts from the bill. Registered: Max${mainKwhNum} kwh` });
    }

    const data: Partial<SubKilowatt> = {
      mainHouse: { id: houseId } as any,
      subHouse: sub,
      subKwh: String(subKwhNum),
    };
    if (existingForThis) {
      Object.assign(existingForThis, data);
      return this.subKwhsRepo.save(existingForThis);
    }
    return this.subKwhsRepo.save(this.subKwhsRepo.create(data));
  }

  // ============ SUB TENANTS ============
  async addSubTenant(userId: number, houseId: number, subId: number, dto: CreateSubTenantDto): Promise<SubTenant> {
    const house = await this.findOneOwned(userId, houseId);
    const bill = house.bill;
    if (!bill) throw new BadRequestException('Bill must be set before adding sub tenants');

    const sub = await this.subHousesRepo.findOne({ where: { id: subId, house: { id: houseId } } });
    if (!sub) throw new NotFoundException('Sub-house not found');

    const start = dto.sub_start_date;
    const end = dto.sub_end_date;
    const days = daysBetween(start, end);
    if (days <= 0) {
      throw new BadRequestException(days < 0
        ? { sub_start_date: 'Start_Date has to be smaller than End_date', sub_end_date: 'End_Date has to be bigger than Start_date' }
        : { sub_start_date: 'It cannot be Equal', sub_end_date: 'It cannot be Equal' });
    }
    if (start < bill.startDateBill) throw new BadRequestException({ sub_start_date: `Out of Range- ${bill.startDateBill}` });
    if (end > bill.endDateBill) throw new BadRequestException({ sub_end_date: `Out of Range- ${bill.endDateBill}` });

    const name = capitalizeName(dto.sub_house_tenant);
    const st = this.subTenantsRepo.create({
      mainHouse: house,
      subHouse: sub,
      subHouseTenant: name,
      subStartDate: start,
      subEndDate: end,
      subDays: days,
    });
    return this.subTenantsRepo.save(st);
  }

  async listSubTenants(userId: number, houseId: number, subId: number): Promise<SubTenant[]> {
    await this.findOneOwnedLight(userId, houseId);
    return this.subTenantsRepo.find({ where: { subHouse: { id: subId } } });
  }

  async removeSubTenant(userId: number, houseId: number, subId: number, tenantId: number): Promise<void> {
    await this.findOneOwnedLight(userId, houseId);
    const res = await this.subTenantsRepo.delete({ id: tenantId, subHouse: { id: subId } });
    if (!res.affected) throw new NotFoundException();
  }

  // For calculator: load full aggregate data for owned house
  async loadFullHouseForCalc(userId: number, houseId: number) {
    const house = await this.housesRepo.findOne({
      where: { id: houseId, user: { id: userId } },
      relations: [
        'bill',
        'kilowatt',
        'tenants',
        'subHouses',
        'subHouses.kilowatts',
        'subHouses.tenants',
      ],
    });
    if (!house) throw new NotFoundException('House not found or access denied');
    if (!house.bill || !house.kilowatt) {
      throw new BadRequestException('House must have bill and kwh set to calculate');
    }
    return house;
  }
}
