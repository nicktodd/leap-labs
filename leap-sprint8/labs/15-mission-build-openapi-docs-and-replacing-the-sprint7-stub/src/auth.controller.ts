import { Body, Controller, Post, HttpCode } from "@nestjs/common";
// TODO 2: import { ApiTags, ApiOperation, ApiResponse } from "@nestjs/swagger" here.
import { AuthService } from "./auth.service";
import { LoginDto } from "./login.dto";
import { RegisterDto } from "./register.dto";

// TODO 2: add @ApiTags("auth") above the class, so both routes below are
// grouped together in the generated docs instead of sitting in "default".
@Controller("auth")
export class AuthController {
  constructor(private readonly authService: AuthService) {}

  // TODO 2: add @ApiOperation({ summary: "..." }) and two @ApiResponse(...)
  // decorators (one per status code this endpoint can actually return -
  // check auth.service.ts for what register() throws).
  @Post("register")
  register(@Body() body: RegisterDto) {
    return this.authService.register(body.username, body.password);
  }

  // TODO 2: same again for login - one @ApiOperation, and an @ApiResponse
  // for each status code login() can return.
  @Post("login")
  @HttpCode(200)
  login(@Body() body: LoginDto) {
    return this.authService.login(body.username, body.password);
  }
}
