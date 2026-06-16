import { IsString, IsDateString, MinLength, MaxLength } from 'class-validator';

export class CreateTenantDto {
  @IsString()
  @MinLength(1)
  @MaxLength(150)
  house_tenant!: string;

  @IsDateString()
  start_date!: string;

  @IsDateString()
  end_date!: string;
}
