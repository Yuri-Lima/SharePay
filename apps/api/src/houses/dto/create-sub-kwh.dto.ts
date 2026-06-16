import { IsNumberString } from 'class-validator';

export class CreateSubKwhDto {
  @IsNumberString()
  sub_kwh!: string;
}
