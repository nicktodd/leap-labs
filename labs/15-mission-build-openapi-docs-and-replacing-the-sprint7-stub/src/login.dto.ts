import { IsString, IsNotEmpty } from "class-validator";
import { ApiProperty } from "@nestjs/swagger";

export class LoginDto {
  @ApiProperty({ example: "alice", description: "The user's username" })
  @IsString()
  @IsNotEmpty()
  username!: string;

  @ApiProperty({ example: "mission123", description: "The user's password" })
  @IsString()
  @IsNotEmpty()
  password!: string;
}
