import { Injectable, UnauthorizedException, ConflictException } from "@nestjs/common";
// TODO 1: import bcrypt here.

interface StoredUser {
  // TODO 1: this should store a HASH, not the plain-text password -
  // rename this field to passwordHash once you're storing a hash here
  // instead (update every reference below to match).
  password: string;
  refreshToken: string | null;
}

const SALT_ROUNDS = 10;

@Injectable()
export class AuthService {
  private readonly users = new Map<string, StoredUser>();

  constructor() {
    void this.register("dave", "mission123");
  }

  // TODO 1: this method needs to be async, and needs to HASH password
  // with bcrypt.hash(password, SALT_ROUNDS) before storing it.
  async register(username: string, password: string): Promise<{ username: string; registered: true }> {
    if (this.users.has(username)) {
      throw new ConflictException(`${username} is already registered`);
    }
    this.users.set(username, { password, refreshToken: null });
    return { username, registered: true };
  }

  // TODO 2: this method needs to use bcrypt.compare(password,
  // user.password) instead of a direct === comparison - a hash can
  // never be compared with === against the plain-text password that
  // produced it.
  async login(username: string, password: string): Promise<{ accessToken: string; refreshToken: string }> {
    const user = this.users.get(username);
    if (!user || user.password !== password) {
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

  private issueStubToken(kind: "access" | "refresh", username: string): string {
    return `stub-${kind}-token-for-${username}-${Math.random().toString(36).slice(2, 10)}`;
  }
}
