import { Body, Controller, Post } from "@nestjs/common";
import { VerificationService } from "./verification.service";
import { VerifyCredentialsDto } from "./verify-credentials.dto";

@Controller("verify")
export class VerificationController {
  constructor(private readonly verificationService: VerificationService) {}

  @Post()
  checkCredentials(@Body() body: VerifyCredentialsDto) {
    const verified = this.verificationService.verify(body.username);
    return { username: body.username, verified };
  }
}
