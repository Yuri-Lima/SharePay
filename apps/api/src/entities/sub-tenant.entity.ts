import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  UpdateDateColumn,
  ManyToOne,
  JoinColumn,
  Unique,
} from 'typeorm';
import { House } from './house.entity';
import { SubHouse } from './sub-house.entity';

@Entity('sub_tenants')
@Unique(['subHouse', 'subHouseTenant']) // mirrors unique_test_SubTenant
export class SubTenant {
  @PrimaryGeneratedColumn()
  id!: number;

  @ManyToOne(() => House, { nullable: true, onDelete: 'CASCADE' })
  @JoinColumn({ name: 'main_tenant_id' })
  mainHouse!: House;

  @ManyToOne(() => SubHouse, (sub) => sub.tenants, { nullable: false, onDelete: 'CASCADE' })
  @JoinColumn({ name: 'sub_house_tenant_id' })
  subHouse!: SubHouse;

  @Column({ name: 'sub_house_tenant', length: 150, nullable: true })
  subHouseTenant!: string; // capitalized on write

  @Column({ name: 'sub_start_date', type: 'date', nullable: true })
  subStartDate!: string | null;

  @Column({ name: 'sub_end_date', type: 'date', nullable: true })
  subEndDate!: string | null;

  @Column({ name: 'sub_days', default: 0 })
  subDays!: number;

  @UpdateDateColumn({ name: 'sub_last_updated_tenant' })
  lastUpdated!: Date;
}
