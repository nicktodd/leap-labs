import { Module } from "@nestjs/common";
import { VerificationController } from "./verification.controller";
import { VerificationService } from "./verification.service";

// A MODULE: wires controllers to the providers they need. Nest reads this
// to know which VerificationService instance to hand VerificationController
// - without listing VerificationService here, injecting it would fail.
@Module({
  controllers: [VerificationController],
  providers: [VerificationService],
})
export class AppModule {}
