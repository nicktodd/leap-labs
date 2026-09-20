import { Module } from "@nestjs/common";
import { VerificationController } from "./verification.controller";
import { VerificationService } from "./verification.service";
import { RegisterController } from "./register.controller";
import { RegisterService } from "./register.service";

@Module({
  controllers: [VerificationController, RegisterController],
  providers: [VerificationService, RegisterService],
})
export class AppModule {}
