import { IsString, IsNotEmpty } from "class-validator";
// TODO 1: import { ApiProperty } from "@nestjs/swagger" here.

export class LoginDto {
  // TODO 1: add @ApiProperty({ example: "alice", description: "..." })
  // above each field below, so they show up correctly in the OpenAPI
  // document Module 10's DTOs never needed to worry about.
  @IsString()
  @IsNotEmpty()
  username!: string;

  @IsString()
  @IsNotEmpty()
  password!: string;
}
