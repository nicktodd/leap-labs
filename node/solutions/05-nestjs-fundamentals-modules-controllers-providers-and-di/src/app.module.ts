import { Module } from "@nestjs/common";
import { VerificationController } from "./verification.controller";
import { VerificationService } from "./verification.service";
import { AttemptsController } from "./attempts.controller";
import { AttemptsService } from "./attempts.service";

@Module({
  controllers: [VerificationController, AttemptsController],
  providers: [VerificationService, AttemptsService],
})
export class AppModule {}
