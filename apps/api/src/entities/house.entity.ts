import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
  ManyToOne,
  OneToOne,
  OneToMany,
  JoinColumn,
  Unique,
} from 'typeorm';
import { User } from './user.entity';
import { HouseBill } from './house-bill.entity';
import { HouseKilowatt } from './house-kilowatt.entity';
import { HouseTenant } from './house-tenant.entity';
import { SubHouse } from './sub-house.entity';

@Entity('houses')
@Unique(['user', 'houseName']) // mirrors unique_test_HouseName
export class House {
  @PrimaryGeneratedColumn()
  id!: number;

  @ManyToOne(() => User, (user) => user.houses, { nullable: false, onDelete: 'CASCADE' })
  @JoinColumn({ name: 'user_id' })
  user!: User;

  @Column({ name: 'house_name', length: 100, nullable: true })
  houseName!: string;

  @Column({ default: 1 })
  meter!: number;

  @CreateDateColumn({ name: 'last_updated_house' })
  lastUpdated!: Date;

  // 1:1 relations (enforced at app level like forms)
  @OneToOne(() => HouseBill, (bill) => bill.house, { cascade: true, eager: false })
  bill?: HouseBill;

  @OneToOne(() => HouseKilowatt, (kwh) => kwh.house, { cascade: true, eager: false })
  kilowatt?: HouseKilowatt;

  @OneToMany(() => HouseTenant, (tenant) => tenant.house, { cascade: true })
  tenants!: HouseTenant[];

  @OneToMany(() => SubHouse, (sub) => sub.house, { cascade: true })
  subHouses!: SubHouse[];
}
