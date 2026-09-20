import { IsString, IsNotEmpty, MinLength } from "class-validator";

export class RegisterDto {
  @IsString()
  @IsNotEmpty()
  @MinLength(3)
  username!: string;

  @IsString()
  @MinLength(8)
  password!: string;
}
