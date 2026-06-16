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

@Entity('house_tenants')
@Unique(['house', 'houseTenant']) // mirrors unique_test_HouseTenant
export class HouseTenant {
  @PrimaryGeneratedColumn()
  id!: number;

  @ManyToOne(() => House, (house) => house.tenants, { nullable: false, onDelete: 'CASCADE' })
  @JoinColumn({ name: 'house_id' })
  house!: House;

  @Column({ name: 'house_tenant', length: 150, nullable: true })
  houseTenant!: string; // always capitalized on write

  @Column({ name: 'start_date', type: 'date', nullable: false })
  startDate!: string;

  @Column({ name: 'end_date', type: 'date', nullable: false })
  endDate!: string;

  @Column({ default: 0 })
  days!: number;

  @UpdateDateColumn({ name: 'last_updated_tenant', type: 'date' })
  lastUpdated!: Date;
}
