import { Controller, Get, Param } from "@nestjs/common";
import { VerificationService } from "./verification.service";

// A CONTROLLER: handles incoming requests, delegates the actual work to a
// provider. @Controller("verify") means every route below is prefixed
// with /verify.
@Controller("verify")
export class VerificationController {
  // CONSTRUCTOR INJECTION: Nest sees this parameter needs a
  // VerificationService and hands one in automatically - nothing in this
  // class ever writes `new VerificationService()` itself.
  constructor(private readonly verificationService: VerificationService) {}

  @Get(":username")
  checkUsername(@Param("username") username: string) {
    const verified = this.verificationService.verify(username);
    return { username, verified };
  }
}
