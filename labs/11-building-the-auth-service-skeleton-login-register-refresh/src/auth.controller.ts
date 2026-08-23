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

  // TODO 2: add a POST /auth/logout route here, following the exact same
  // shape as refresh() above - @Post("logout"), @HttpCode(200), a
  // @Body() body: RefreshDto parameter, calling
  // this.authService.logout(body.refreshToken).
}
