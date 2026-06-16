import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
  OneToOne,
  JoinColumn,
} from 'typeorm';
import { House } from './house.entity';

@Entity('house_bills')
export class HouseBill {
  @PrimaryGeneratedColumn()
  id!: number;

  @OneToOne(() => House, (house) => house.bill, { onDelete: 'CASCADE' })
  @JoinColumn({ name: 'house_id' })
  house!: House;

  @Column({ name: 'amount_bill', type: 'varchar', length: 22, nullable: true })
  amountBill!: string; // store as string to mirror char field + mask handling; parse to Decimal on use

  @Column({ name: 'start_date_bill', type: 'date', nullable: false })
  startDateBill!: string;

  @Column({ name: 'end_date_bill', type: 'date', nullable: false })
  endDateBill!: string;

  @Column({ name: 'days_bill', default: 0 })
  daysBill!: number;

  @UpdateDateColumn({ name: 'last_updated_bill' })
  lastUpdated!: Date;
}
