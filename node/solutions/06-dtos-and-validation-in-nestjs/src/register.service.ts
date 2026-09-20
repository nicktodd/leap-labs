import { Injectable } from "@nestjs/common";
import { RegisterDto } from "./register.dto";

@Injectable()
export class RegisterService {
  register(dto: RegisterDto) {
    return { username: dto.username, email: dto.email, registered: true };
  }
}
