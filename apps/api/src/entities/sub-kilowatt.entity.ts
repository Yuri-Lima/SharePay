import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  UpdateDateColumn,
  ManyToOne,
  JoinColumn,
} from 'typeorm';
import { House } from './house.entity';
import { SubHouse } from './sub-house.entity';

@Entity('sub_kilowatts')
export class SubKilowatt {
  @PrimaryGeneratedColumn()
  id!: number;

  @ManyToOne(() => House, { nullable: true, onDelete: 'CASCADE' })
  @JoinColumn({ name: 'main_house_kwh_id' })
  mainHouse!: House; // mirrors FK to HouseNameModel for main kwh

  @ManyToOne(() => SubHouse, (sub) => sub.kilowatts, { nullable: false, onDelete: 'CASCADE' })
  @JoinColumn({ name: 'sub_house_kwh_id' })
  subHouse!: SubHouse;

  @Column({ name: 'sub_kwh', type: 'decimal', precision: 10, scale: 0, nullable: true })
  subKwh!: string | null;

  @Column({ name: 'sub_amount_bill', type: 'decimal', precision: 10, scale: 0, nullable: true })
  subAmountBill!: string | null;

  @Column({ name: 'sub_last_read_kwh', type: 'decimal', precision: 10, scale: 0, nullable: true })
  subLastReadKwh!: string | null;

  @Column({ name: 'sub_read_kwh', type: 'decimal', precision: 10, scale: 0, nullable: true })
  subReadKwh!: string | null;

  @UpdateDateColumn({ name: 'sub_last_updated_kwh' })
  lastUpdated!: Date;
}
