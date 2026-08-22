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

  // TODO 1: implement logout(refreshToken) - find the user holding this
  // refresh token (findByRefreshToken is given, below), set their
  // refreshToken back to null so it can never be used again, and return
  // { loggedOut: true }. If no user holds this token, throw
  // UnauthorizedException("invalid or expired refresh token") - same as
  // refresh() does.
  logout(refreshToken: string): { loggedOut: true } {
    throw new Error("TODO 1: implement logout");
  }

  private findByRefreshToken(refreshToken: string): [string, StoredUser] | undefined {
    return [...this.users.entries()].find(([, u]) => u.refreshToken === refreshToken);
  }

  private issueStubToken(kind: "access" | "refresh", username: string): string {
    return `stub-${kind}-token-for-${username}-${Math.random().toString(36).slice(2, 10)}`;
  }
}
