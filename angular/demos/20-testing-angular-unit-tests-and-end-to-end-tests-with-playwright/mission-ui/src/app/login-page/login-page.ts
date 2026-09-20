import { Component, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthApi } from '../auth-api';
import { TokenStore } from '../token-store';

@Component({
  selector: 'app-login-page',
  imports: [ReactiveFormsModule],
  templateUrl: './login-page.html',
  styleUrl: './login-page.css',
})
export class LoginPage {
  private readonly fb = inject(FormBuilder);
  private readonly authApi = inject(AuthApi);
  private readonly tokenStore = inject(TokenStore);
  private readonly router = inject(Router);

  protected readonly error = signal<string | null>(null);

  protected readonly loginForm = this.fb.group({
    username: ['alice', Validators.required],
    password: ['mission123', Validators.required],
  });

  protected submit(): void {
    if (this.loginForm.invalid) {
      this.loginForm.markAllAsTouched();
      return;
    }

    this.error.set(null);
    const { username, password } = this.loginForm.getRawValue();

    this.authApi.login(username!, password!).subscribe({
      next: (response) => {
        this.tokenStore.setToken(response.accessToken, username!);
        this.router.navigate(['/holdings']);
      },
      error: () => {
        this.error.set('Invalid username or password.');
      },
    });
  }
}
