import { Body, Controller, Post, HttpCode } from "@nestjs/common";
import { AuthService } from "./auth.service";
import { LoginDto } from "./login.dto";
import { RegisterDto } from "./register.dto";
import { RefreshDto } from "./refresh.dto";

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

  @Post("refresh")
  @HttpCode(200)
  refresh(@Body() body: RefreshDto) {
    return this.authService.refresh(body.refreshToken);
  }

  @Post("logout")
  @HttpCode(200)
  logout(@Body() body: RefreshDto) {
    return this.authService.logout(body.refreshToken);
  }
}
