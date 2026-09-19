// Given, unchanged - the exact provider from the demo.
import { Injectable } from "@nestjs/common";

@Injectable()
export class VerificationService {
  private readonly knownUsers = ["dave", "erin", "frank"];

  verify(username: string): boolean {
    return this.knownUsers.includes(username);
  }
}
