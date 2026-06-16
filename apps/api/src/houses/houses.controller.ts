import {
  Controller,
  Get,
  Post,
  Put,
  Delete,
  Param,
  Body,
  UseGuards,
  ParseIntPipe,
  Req,
  HttpCode,
} from '@nestjs/common';
import { HousesService } from './houses.service';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';
import { CreateHouseDto } from './dto/create-house.dto';
import { UpdateHouseDto } from './dto/update-house.dto';
import { CreateBillDto } from './dto/create-bill.dto';
import { CreateKwhDto } from './dto/create-kwh.dto';
import { CreateTenantDto } from './dto/create-tenant.dto';
import { CreateSubHouseDto } from './dto/create-sub-house.dto';
import { CreateSubKwhDto } from './dto/create-sub-kwh.dto';
import { CreateSubTenantDto } from './dto/create-sub-tenant.dto';
import { CalculatorService } from '../calculations/calculator.service';

@UseGuards(JwtAuthGuard)
@Controller('houses')
export class HousesController {
  constructor(
    private readonly housesService: HousesService,
    private readonly calculatorService: CalculatorService,
  ) {}

  // HOUSES
  @Post()
  create(@Req() req: any, @Body() dto: CreateHouseDto) {
    return this.housesService.create(req.user.id, dto);
  }

  @Get()
  findAll(@Req() req: any) {
    return this.housesService.findAllForUser(req.user.id);
  }

  @Get(':id')
  findOne(@Req() req: any, @Param('id', ParseIntPipe) id: number) {
    return this.housesService.findOneOwned(req.user.id, id);
  }

  @Put(':id')
  update(@Req() req: any, @Param('id', ParseIntPipe) id: number, @Body() dto: UpdateHouseDto) {
    return this.housesService.update(req.user.id, id, dto);
  }

  @Delete(':id')
  @HttpCode(204)
  async remove(@Req() req: any, @Param('id', ParseIntPipe) id: number) {
    await this.housesService.remove(req.user.id, id);
  }

  // BILL (nested)
  @Post(':id/bill')
  setBill(@Req() req: any, @Param('id', ParseIntPipe) id: number, @Body() dto: CreateBillDto) {
    return this.housesService.setBill(req.user.id, id, dto);
  }

  @Get(':id/bill')
  getBill(@Req() req: any, @Param('id', ParseIntPipe) id: number) {
    return this.housesService.getBill(req.user.id, id);
  }

  // KWH (nested)
  @Post(':id/kwh')
  setKwh(@Req() req: any, @Param('id', ParseIntPipe) id: number, @Body() dto: CreateKwhDto) {
    return this.housesService.setKwh(req.user.id, id, dto);
  }

  @Get(':id/kwh')
  getKwh(@Req() req: any, @Param('id', ParseIntPipe) id: number) {
    return this.housesService.getKwh(req.user.id, id);
  }

  // TENANTS (nested main)
  @Post(':id/tenants')
  addTenant(@Req() req: any, @Param('id', ParseIntPipe) id: number, @Body() dto: CreateTenantDto) {
    return this.housesService.addTenant(req.user.id, id, dto);
  }

  @Get(':id/tenants')
  listTenants(@Req() req: any, @Param('id', ParseIntPipe) id: number) {
    return this.housesService.listTenants(req.user.id, id);
  }

  @Put(':id/tenants/:tenantId')
  updateTenant(
    @Req() req: any,
    @Param('id', ParseIntPipe) id: number,
    @Param('tenantId', ParseIntPipe) tenantId: number,
    @Body() dto: CreateTenantDto,
  ) {
    return this.housesService.updateTenant(req.user.id, id, tenantId, dto);
  }

  @Delete(':id/tenants/:tenantId')
  @HttpCode(204)
  async removeTenant(@Req() req: any, @Param('id', ParseIntPipe) id: number, @Param('tenantId', ParseIntPipe) tenantId: number) {
    await this.housesService.removeTenant(req.user.id, id, tenantId);
  }

  // SUB-HOUSES
  @Post(':id/sub-houses')
  addSubHouse(@Req() req: any, @Param('id', ParseIntPipe) id: number, @Body() dto: CreateSubHouseDto) {
    return this.housesService.addSubHouse(req.user.id, id, dto);
  }

  @Get(':id/sub-houses')
  listSubHouses(@Req() req: any, @Param('id', ParseIntPipe) id: number) {
    return this.housesService.listSubHouses(req.user.id, id);
  }

  @Delete(':id/sub-houses/:subId')
  @HttpCode(204)
  async removeSubHouse(@Req() req: any, @Param('id', ParseIntPipe) id: number, @Param('subId', ParseIntPipe) subId: number) {
    await this.housesService.removeSubHouse(req.user.id, id, subId);
  }

  // SUB KWH (per sub)
  @Post(':id/sub-houses/:subId/kwh')
  setSubKwh(
    @Req() req: any,
    @Param('id', ParseIntPipe) id: number,
    @Param('subId', ParseIntPipe) subId: number,
    @Body() dto: CreateSubKwhDto,
  ) {
    return this.housesService.setSubKwh(req.user.id, id, subId, dto);
  }

  // SUB TENANTS (per sub)
  @Post(':id/sub-houses/:subId/tenants')
  addSubTenant(
    @Req() req: any,
    @Param('id', ParseIntPipe) id: number,
    @Param('subId', ParseIntPipe) subId: number,
    @Body() dto: CreateSubTenantDto,
  ) {
    return this.housesService.addSubTenant(req.user.id, id, subId, dto);
  }

  @Get(':id/sub-houses/:subId/tenants')
  listSubTenants(@Req() req: any, @Param('id', ParseIntPipe) id: number, @Param('subId', ParseIntPipe) subId: number) {
    return this.housesService.listSubTenants(req.user.id, id, subId);
  }

  @Delete(':id/sub-houses/:subId/tenants/:tenantId')
  @HttpCode(204)
  async removeSubTenant(
    @Req() req: any,
    @Param('id', ParseIntPipe) id: number,
    @Param('subId', ParseIntPipe) subId: number,
    @Param('tenantId', ParseIntPipe) tenantId: number,
  ) {
    await this.housesService.removeSubTenant(req.user.id, id, subId, tenantId);
  }

  // ============ THE KEY CALCULATE ENDPOINT ============
  // POST /api/houses/:id/calculate  -> returns merged (calc_1 + calc_2 + meta) identical to original templates
  @Post(':id/calculate')
  async calculate(@Req() req: any, @Param('id', ParseIntPipe) id: number) {
    const fullHouse = await this.housesService.loadFullHouseForCalc(req.user.id, id);
    // Use pure BillCalculator via service (guarantees parity)
    return this.calculatorService.runCalculationForHouse(fullHouse);
  }
}
