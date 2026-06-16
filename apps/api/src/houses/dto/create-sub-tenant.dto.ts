import { IsString, IsDateString, MinLength, MaxLength } from 'class-validator';

export class CreateSubTenantDto {
  @IsString()
  @MinLength(1)
  @MaxLength(150)
  sub_house_tenant!: string;

  @IsDateString()
  sub_start_date!: string;

  @IsDateString()
  sub_end_date!: string;
}
