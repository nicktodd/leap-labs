// Given, unchanged - once TODO 1 (attempts.service.ts) and TODO 2
// (app.module.ts) are done, GET /attempts/summary should work.
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
