import { Body, Controller, Post, HttpCode } from "@nestjs/common";
import { ApiTags, ApiOperation, ApiResponse } from "@nestjs/swagger";
import { AuthService } from "./auth.service";
import { LoginDto } from "./login.dto";
import { RegisterDto } from "./register.dto";

@ApiTags("auth")
@Controller("auth")
export class AuthController {
  constructor(private readonly authService: AuthService) {}

  @ApiOperation({ summary: "Register a new user" })
  @ApiResponse({ status: 201, description: "User registered successfully" })
  @ApiResponse({ status: 409, description: "Username already taken" })
  @Post("register")
  register(@Body() body: RegisterDto) {
    return this.authService.register(body.username, body.password);
  }

  @ApiOperation({ summary: "Log in and receive access and refresh tokens" })
  @ApiResponse({ status: 200, description: "Login successful, tokens returned" })
  @ApiResponse({ status: 401, description: "Invalid username or password" })
  @Post("login")
  @HttpCode(200)
  login(@Body() body: LoginDto) {
    return this.authService.login(body.username, body.password);
  }
}
