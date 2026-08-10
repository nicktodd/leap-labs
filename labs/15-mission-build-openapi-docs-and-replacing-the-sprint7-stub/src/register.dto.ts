import { IsString, IsNotEmpty, MinLength } from "class-validator";
import { ApiProperty } from "@nestjs/swagger";

export class RegisterDto {
  @ApiProperty({ example: "alice", description: "Username, at least 3 characters" })
  @IsString()
  @IsNotEmpty()
  @MinLength(3)
  username!: string;

  @ApiProperty({ example: "mission123", description: "Password, at least 8 characters" })
  @IsString()
  @MinLength(8)
  password!: string;
}
