import { Module } from "@nestjs/common";
import { VerificationController } from "./verification.controller";
import { VerificationService } from "./verification.service";
import { AttemptsController } from "./attempts.controller";
import { AttemptsService } from "./attempts.service";

// TODO 2: add AttemptsController to the controllers array, and
// AttemptsService to the providers array, alongside the Verification
// pieces already here. Without this, injecting AttemptsService into
// AttemptsController fails, even though both classes are written
// correctly.
@Module({
  controllers: [VerificationController, AttemptsController],
  providers: [VerificationService, AttemptsService],
})
export class AppModule {}
