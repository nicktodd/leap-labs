import { Injectable, UnauthorizedException, ConflictException } from "@nestjs/common";

interface StoredUser {
  password: string;
  refreshToken: string | null;
}

// This is the SKELETON - deliberately incomplete in two specific ways,
// both flagged so nothing here is mistaken for "the real thing":
//
//   1. Passwords are stored in PLAIN TEXT. Module 12 (Secure DB Access &
//      Password Hashing) replaces this with real hashing - never do this
//      in anything that isn't a training skeleton.
//   2. Tokens are just random strings, not real JWTs. Module 13 (JWT
//      Essentials) replaces issueAccessToken/issueRefreshToken with real
//      signed tokens - matching the exact contract Sprint 6's real
//      auth-stub already uses (POST /login -> { token }, HS256-signed).
//
// alice/mission123 is preloaded to match Sprint 6's auth-stub exactly -
// this service is the eventual REPLACEMENT for that stub, and Sprint 6's
// mission service must be able to log in against it unchanged.
@Injectable()
export class AuthService {
  private readonly users = new Map<string, StoredUser>([
    ["alice", { password: "mission123", refreshToken: null }],
  ]);

  register(username: string, password: string): { username: string; registered: true } {
    if (this.users.has(username)) {
      throw new ConflictException(`${username} is already registered`);
    }
    this.users.set(username, { password, refreshToken: null });
    return { username, registered: true };
  }

  login(username: string, password: string): { accessToken: string; refreshToken: string } {
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
    const entry = [...this.users.entries()].find(([, u]) => u.refreshToken === refreshToken);
    if (!entry) {
      throw new UnauthorizedException("invalid or expired refresh token");
    }
    const [username] = entry;
    return { accessToken: this.issueStubToken("access", username) };
  }

  // TODO (Module 13): replace this with a real HS256-signed JWT, matching
  // Sprint 6's auth-stub. For now, a random string is enough to prove the
  // REQUEST/RESPONSE SHAPE is right - which is what this module is about.
  private issueStubToken(kind: "access" | "refresh", username: string): string {
    return `stub-${kind}-token-for-${username}-${Math.random().toString(36).slice(2, 10)}`;
  }
}
