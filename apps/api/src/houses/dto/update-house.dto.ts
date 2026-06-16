import { IsOptional, IsString, MaxLength, MinLength } from 'class-validator';

// Manual partial (no @nestjs/mapped-types dep)
export class UpdateHouseDto {
  @IsOptional()
  @IsString()
  @MinLength(1)
  @MaxLength(25)
  house_name?: string;
}
