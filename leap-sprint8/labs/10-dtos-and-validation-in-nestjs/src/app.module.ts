import { Module } from "@nestjs/common";
import { VerificationController } from "./verification.controller";
import { VerificationService } from "./verification.service";
import { RegisterController } from "./register.controller";
import { RegisterService } from "./register.service";

// TODO 2: add RegisterController to controllers and RegisterService to
// providers, alongside the Verification pieces already here.
@Module({
  controllers: [VerificationController],
  providers: [VerificationService],
})
export class AppModule {}
