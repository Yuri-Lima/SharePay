import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  UpdateDateColumn,
  OneToOne,
  JoinColumn,
} from 'typeorm';
import { House } from './house.entity';

@Entity('house_kilowatts')
export class HouseKilowatt {
  @PrimaryGeneratedColumn()
  id!: number;

  @OneToOne(() => House, (house) => house.kilowatt, { onDelete: 'CASCADE' })
  @JoinColumn({ name: 'house_id' })
  house!: House;

  @Column({ type: 'decimal', precision: 10, scale: 0, nullable: true })
  kwh!: string | null; // store decimal as string for precision; parse on use

  @Column({ name: 'last_read_kwh', type: 'decimal', precision: 10, scale: 0, nullable: true })
  lastReadKwh!: string | null;

  @Column({ name: 'read_kwh', type: 'decimal', precision: 10, scale: 0, nullable: true })
  readKwh!: string | null;

  @UpdateDateColumn({ name: 'last_updated_kwh' })
  lastUpdated!: Date;
}
