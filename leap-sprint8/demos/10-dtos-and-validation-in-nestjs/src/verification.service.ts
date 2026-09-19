import { Injectable } from "@nestjs/common";

@Injectable()
export class VerificationService {
  private readonly knownUsers = ["alice", "bob", "carol"];

  verify(username: string): boolean {
    return this.knownUsers.includes(username);
  }
}
