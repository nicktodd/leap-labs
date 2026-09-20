import { IsString, IsNotEmpty, MinLength } from "class-validator";

// A DTO (Data Transfer Object): a plain class describing the SHAPE of an
// incoming request body, with class-validator decorators describing the
// RULES that shape must satisfy. Nest validates an incoming body against
// this class BEFORE the route handler ever runs.
export class VerifyCredentialsDto {
  @IsString()
  @IsNotEmpty()
  @MinLength(3)
  username!: string;
}
