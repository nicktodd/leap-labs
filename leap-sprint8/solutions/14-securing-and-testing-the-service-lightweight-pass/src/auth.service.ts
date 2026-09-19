import { Injectable, UnauthorizedException, ConflictException } from "@nestjs/common";
import * as bcrypt from "bcrypt";
import * as jwt from "jsonwebtoken";
import { randomBytes } from "crypto";
import { logAuthEvent } from "./logger";

interface StoredUser {
  passwordHash: string;
  roles: string[];
  refreshToken: string | null;
}

const SALT_ROUNDS = 10;

// Sprint 6's real auth-stub reads this from process.env.JWT_SECRET, with
// this exact string as its fallback. Exported so the Jest suite can verify
// tokens the same way a real client of this service would.
export const JWT_SECRET = process.env.JWT_SECRET || "mission-control-shared-secret-key-32-bytes-minimum";

@Injectable()
export class AuthService {
  private readonly users = new Map<string, StoredUser>();

  constructor() {
    // alice/mission123/MISSION_OPERATOR - matches Sprint 6's auth-stub.
    void this.register("alice", "mission123", ["MISSION_OPERATOR"]);
  }

  async register(
    username: string,
    password: string,
    roles: string[] = ["MISSION_OPERATOR"],
  ): Promise<{ username: string; registered: true }> {
    if (this.users.has(username)) {
      throw new ConflictException(`${username} is already registered`);
    }
    const passwordHash = await bcrypt.hash(password, SALT_ROUNDS);
    this.users.set(username, { passwordHash, roles, refreshToken: null });
    return { username, registered: true };
  }

  async login(username: string, password: string): Promise<{ accessToken: string; refreshToken: string }> {
    const user = this.users.get(username);
    const passwordMatches = user ? await bcrypt.compare(password, user.passwordHash) : false;
    if (!user || !passwordMatches) {
      throw new UnauthorizedException("invalid username or password");
    }
    const accessToken = this.issueAccessToken(username, user.roles);
    const refreshToken = randomBytes(32).toString("hex");
    user.refreshToken = refreshToken;
    // Log the EVENT and the username - never the password, never either
    // token. Anyone who can read this log line should learn "alice logged
    // in just now", not gain anything usable to act as alice.
    logAuthEvent("login_success", username);
    return { accessToken, refreshToken };
  }

  refresh(refreshToken: string): { accessToken: string } {
    const entry = this.findByRefreshToken(refreshToken);
    if (!entry) {
      throw new UnauthorizedException("invalid or expired refresh token");
    }
    const [username, user] = entry;
    return { accessToken: this.issueAccessToken(username, user.roles) };
  }

  private issueAccessToken(username: string, roles: string[]): string {
    return jwt.sign({ sub: username, roles }, JWT_SECRET, {
      algorithm: "HS256",
      expiresIn: "15m",
    });
  }

  private findByRefreshToken(refreshToken: string): [string, StoredUser] | undefined {
    return [...this.users.entries()].find(([, u]) => u.refreshToken === refreshToken);
  }
}
