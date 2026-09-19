import { Body, Controller, Post } from "@nestjs/common";
import { RegisterService } from "./register.service";
import { RegisterDto } from "./register.dto";

@Controller("register")
export class RegisterController {
  constructor(private readonly registerService: RegisterService) {}

  @Post()
  register(@Body() body: RegisterDto) {
    return this.registerService.register(body);
  }
}
