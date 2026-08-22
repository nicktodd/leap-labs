import { IsString, IsNotEmpty, MinLength } from "class-validator";
// TODO 1: import { ApiProperty } from "@nestjs/swagger" here too.

export class RegisterDto {
  @IsString()
  @IsNotEmpty()
  @MinLength(3)
  username!: string;

  @IsString()
  @MinLength(8)
  password!: string;
}
