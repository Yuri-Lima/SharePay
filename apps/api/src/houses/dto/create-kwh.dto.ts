import { IsOptional, IsNumberString, ValidateIf } from 'class-validator';

export class CreateKwhDto {
  @IsOptional()
  @IsNumberString()
  kwh?: string;

  @IsOptional()
  @IsNumberString()
  last_read_kwh?: string;

  @IsOptional()
  @IsNumberString()
  read_kwh?: string;
}
