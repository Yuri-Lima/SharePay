import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  ManyToOne,
  OneToMany,
  JoinColumn,
  Unique,
} from 'typeorm';
import { House } from './house.entity';
import { SubKilowatt } from './sub-kilowatt.entity';
import { SubTenant } from './sub-tenant.entity';

@Entity('sub_houses')
@Unique(['house', 'subHouseName']) // mirrors unique_test_SubHouseName
export class SubHouse {
  @PrimaryGeneratedColumn()
  id!: number;

  @ManyToOne(() => House, (house) => house.subHouses, { nullable: false, onDelete: 'CASCADE' })
  @JoinColumn({ name: 'house_id' })
  house!: House;

  @Column({ name: 'sub_house_name', length: 100, nullable: true })
  subHouseName!: string;

  @Column({ name: 'sub_meter', nullable: true, default: 1 })
  subMeter!: number;

  @Column({ name: 'sub_main_house', default: false })
  subMainHouse!: boolean;

  @CreateDateColumn({ name: 'sub_last_updated_house' })
  lastUpdated!: Date;

  @OneToMany(() => SubKilowatt, (kwh) => kwh.subHouse, { cascade: true })
  kilowatts!: SubKilowatt[];

  @OneToMany(() => SubTenant, (tenant) => tenant.subHouse, { cascade: true })
  tenants!: SubTenant[];
}
