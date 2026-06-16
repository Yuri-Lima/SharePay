import { IsString, MaxLength, MinLength, IsOptional, IsBoolean } from 'class-validator';

export class CreateSubHouseDto {
  @IsString()
  @MinLength(1)
  @MaxLength(25)
  sub_house_name!: string;

  @IsOptional()
  @IsBoolean()
  sub_main_house?: boolean;
}
