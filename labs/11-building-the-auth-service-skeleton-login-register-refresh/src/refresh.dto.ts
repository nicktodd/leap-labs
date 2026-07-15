// Given, unchanged. Reused for TODO 2's logout route - the request shape
// is identical: "here is a refresh token."
import { IsString, IsNotEmpty } from "class-validator";

export class RefreshDto {
  @IsString()
  @IsNotEmpty()
  refreshToken!: string;
}
