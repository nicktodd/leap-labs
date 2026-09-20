// Given, unchanged - the exact DTO from the demo.
import { IsString, IsNotEmpty, MinLength } from "class-validator";

export class VerifyCredentialsDto {
  @IsString()
  @IsNotEmpty()
  @MinLength(3)
  username!: string;
}
