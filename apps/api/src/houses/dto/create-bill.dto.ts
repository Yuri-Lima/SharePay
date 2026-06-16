import { IsString, IsDateString, Validate, IsOptional } from 'class-validator';
import { Transform } from 'class-transformer';

// amount as string to support masked input like original forms (e.g. '120,50')
export class CreateBillDto {
  @IsString()
  @Transform(({ value }) => (typeof value === 'number' ? String(value) : value))
  amount_bill!: string;

  @IsDateString()
  start_date_bill!: string;

  @IsDateString()
  end_date_bill!: string;
}
