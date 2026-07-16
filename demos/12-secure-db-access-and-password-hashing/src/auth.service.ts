import { Injectable, UnauthorizedException, ConflictException } from "@nestjs/common";
import * as bcrypt from "bcrypt";

interface StoredUser {
  passwordHash: string;
  refreshToken: string | null;
}

// SALT_ROUNDS controls how expensive bcrypt's hashing is - higher is
// slower (more secure against brute force) but slower for every real
// login too. 10 is bcrypt's own commonly recommended default in 2026.
const SALT_ROUNDS = 10;

@Injectable()
export class AuthService {
  private readonly users = new Map<string, StoredUser>();

  constructor() {
    // Preloaded to match Sprint 6's auth-stub - but the password is now
    // HASHED, not stored as "mission123" in plain text the way Module
    // 11's skeleton left it.
    void this.register("alice", "mission123");
  }

  async register(username: string, password: string): Promise<{ username: string; registered: true }> {
    if (this.users.has(username)) {
      throw new ConflictException(`${username} is already registered`);
    }
    // bcrypt.hash generates a random SALT internally and folds it into
    // the result - two users with the same password get DIFFERENT
    // hashes. Never write your own salting scheme; bcrypt already does
    // this correctly.
    const passwordHash = await bcrypt.hash(password, SALT_ROUNDS);
    this.users.set(username, { passwordHash, refreshToken: null });
    return { username, registered: true };
  }

  async login(username: string, password: string): Promise<{ accessToken: string; refreshToken: string }> {
    const user = this.users.get(username);
    // bcrypt.compare re-hashes the SUBMITTED password using the SAME
    // salt embedded in the stored hash, then compares the two hashes -
    // the plain-text password is never stored or compared directly.
    const passwordMatches = user ? await bcrypt.compare(password, user.passwordHash) : false;
    if (!user || !passwordMatches) {
      throw new UnauthorizedException("invalid username or password");
    }
    const accessToken = this.issueStubToken("access", username);
    const refreshToken = this.issueStubToken("refresh", username);
    user.refreshToken = refreshToken;
    return { accessToken, refreshToken };
  }

  refresh(refreshToken: string): { accessToken: string } {
    const entry = this.findByRefreshToken(refreshToken);
    if (!entry) {
      throw new UnauthorizedException("invalid or expired refresh token");
    }
    const [username] = entry;
    return { accessToken: this.issueStubToken("access", username) };
  }

  private findByRefreshToken(refreshToken: string): [string, StoredUser] | undefined {
    return [...this.users.entries()].find(([, u]) => u.refreshToken === refreshToken);
  }

  // Still a stub - Module 13 replaces this with a real signed JWT.
  private issueStubToken(kind: "access" | "refresh", username: string): string {
    return `stub-${kind}-token-for-${username}-${Math.random().toString(36).slice(2, 10)}`;
  }
}
