import { IsString, MaxLength, MinLength, IsOptional } from 'class-validator';

export class CreateHouseDto {
  @IsString()
  @MinLength(1)
  @MaxLength(25, { message: 'Ensure House Name has max 25 characters.' })
  house_name!: string;
}
