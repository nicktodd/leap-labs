import { Body, Controller, Post, HttpCode } from "@nestjs/common";
import { AuthService } from "./auth.service";
import { LoginDto } from "./login.dto";
import { RegisterDto } from "./register.dto";

@Controller("auth")
export class AuthController {
  constructor(private readonly authService: AuthService) {}

  @Post("register")
  register(@Body() body: RegisterDto) {
    return this.authService.register(body.username, body.password);
  }

  @Post("login")
  @HttpCode(200)
  login(@Body() body: LoginDto) {
    return this.authService.login(body.username, body.password);
  }
}
