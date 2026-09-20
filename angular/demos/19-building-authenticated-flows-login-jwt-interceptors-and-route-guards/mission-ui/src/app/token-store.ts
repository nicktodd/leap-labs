import { Injectable, signal, computed } from '@angular/core';

// In-memory only, deliberately: no localStorage/cookie. The token
// disappears on a page refresh, which is the correct behaviour for
// this sprint - a persistent session is a separate concern this
// module doesn't build.
@Injectable({
  providedIn: 'root',
})
export class TokenStore {
  private readonly token = signal<string | null>(null);
  private readonly username = signal<string | null>(null);

  readonly isAuthenticated = computed(() => this.token() !== null);
  readonly currentUsername = this.username.asReadonly();

  setToken(token: string, username: string): void {
    this.token.set(token);
    this.username.set(username);
  }

  getToken(): string | null {
    return this.token();
  }

  clear(): void {
    this.token.set(null);
    this.username.set(null);
  }
}
