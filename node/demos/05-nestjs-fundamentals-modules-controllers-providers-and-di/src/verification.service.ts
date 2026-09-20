import { Injectable } from "@nestjs/common";

// A PROVIDER: a class Nest can create and hand to anything that asks for
// it. @Injectable() is what marks a class as something Nest is willing to
// manage - without it, Nest has no idea this class exists as a provider.
@Injectable()
export class VerificationService {
  private readonly knownUsers = ["alice", "bob", "carol"];

  verify(username: string): boolean {
    return this.knownUsers.includes(username);
  }
}
