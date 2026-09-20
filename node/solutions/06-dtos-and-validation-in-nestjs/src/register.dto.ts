import { IsString, IsNotEmpty, MinLength, IsEmail } from "class-validator";

export class RegisterDto {
  @IsString()
  @IsNotEmpty()
  @MinLength(3)
  username!: string;

  @IsString()
  @MinLength(8)
  password!: string;

  @IsEmail()
  email!: string;
}
