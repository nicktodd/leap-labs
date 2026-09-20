import { Injectable, UnauthorizedException, ConflictException } from "@nestjs/common";

interface StoredUser {
  password: string;
  refreshToken: string | null;
}

@Injectable()
export class AuthService {
  private readonly users = new Map<string, StoredUser>([
    ["dave", { password: "mission123", refreshToken: null }],
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
    const entry = this.findByRefreshToken(refreshToken);
    if (!entry) {
      throw new UnauthorizedException("invalid or expired refresh token");
    }
    const [username] = entry;
    return { accessToken: this.issueStubToken("access", username) };
  }

  logout(refreshToken: string): { loggedOut: true } {
    const entry = this.findByRefreshToken(refreshToken);
    if (!entry) {
      throw new UnauthorizedException("invalid or expired refresh token");
    }
    const [, user] = entry;
    user.refreshToken = null;
    return { loggedOut: true };
  }

  private findByRefreshToken(refreshToken: string): [string, StoredUser] | undefined {
    return [...this.users.entries()].find(([, u]) => u.refreshToken === refreshToken);
  }

  private issueStubToken(kind: "access" | "refresh", username: string): string {
    return `stub-${kind}-token-for-${username}-${Math.random().toString(36).slice(2, 10)}`;
  }
}
