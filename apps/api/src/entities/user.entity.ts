import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  UpdateDateColumn,
  OneToMany,
} from 'typeorm';
import { House } from './house.entity';

@Entity('users')
export class User {
  @PrimaryGeneratedColumn()
  id!: number;

  @Column({ unique: true, length: 150 })
  username!: string;

  @Column({ length: 255 })
  password!: string; // hashed

  @CreateDateColumn({ name: 'date_joined' })
  createdAt!: Date;

  @UpdateDateColumn({ name: 'last_login' })
  updatedAt!: Date;

  @OneToMany(() => House, (house) => house.user)
  houses!: House[];
}
