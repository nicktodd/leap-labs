// Given, unchanged - the exact controller from the demo.
import { Controller, Get, Param } from "@nestjs/common";
import { VerificationService } from "./verification.service";

@Controller("verify")
export class VerificationController {
  constructor(private readonly verificationService: VerificationService) {}

  @Get(":username")
  checkUsername(@Param("username") username: string) {
    const verified = this.verificationService.verify(username);
    return { username, verified };
  }
}
