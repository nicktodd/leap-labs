import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

const AUTH_URL = 'http://localhost:3000/auth/login';

interface LoginResponse {
  accessToken: string;
  refreshToken: string;
}

@Injectable({
  providedIn: 'root',
})
export class AuthApi {
  private readonly http = inject(HttpClient);

  login(username: string, password: string): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(AUTH_URL, { username, password });
  }
}
