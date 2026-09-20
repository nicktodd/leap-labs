import { Controller, Get } from "@nestjs/common";
import { AttemptsService } from "./attempts.service";

@Controller("attempts")
export class AttemptsController {
  constructor(private readonly attemptsService: AttemptsService) {}

  @Get("summary")
  summary() {
    return this.attemptsService.getSummary();
  }
}
