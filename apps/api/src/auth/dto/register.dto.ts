import { IsString, MinLength, MaxLength, Matches } from 'class-validator';

export class RegisterDto {
  @IsString()
  @MinLength(3)
  @MaxLength(150)
  @Matches(/^[a-zA-Z0-9_.-]+$/, { message: 'Username may only contain letters, numbers, ., - and _' })
  username!: string;

  @IsString()
  @MinLength(6)
  @MaxLength(128)
  password!: string;
}
