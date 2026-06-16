import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { HousesController } from './houses.controller';
import { HousesService } from './houses.service';
import { House } from '../entities/house.entity';
import { HouseBill } from '../entities/house-bill.entity';
import { HouseKilowatt } from '../entities/house-kilowatt.entity';
import { HouseTenant } from '../entities/house-tenant.entity';
import { SubHouse } from '../entities/sub-house.entity';
import { SubKilowatt } from '../entities/sub-kilowatt.entity';
import { SubTenant } from '../entities/sub-tenant.entity';
import { CalculatorService } from '../calculations/calculator.service';

@Module({
  imports: [
    TypeOrmModule.forFeature([
      House,
      HouseBill,
      HouseKilowatt,
      HouseTenant,
      SubHouse,
      SubKilowatt,
      SubTenant,
    ]),
  ],
  controllers: [HousesController],
  providers: [HousesService, CalculatorService],
  exports: [HousesService, CalculatorService],
})
export class HousesModule {}
