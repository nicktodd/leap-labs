import { Component, inject, signal } from '@angular/core';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthApiService } from '../auth-api';
import { TokenStore } from '../token-store';

@Component({
  selector: 'app-login-page',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './login-page.html',
  styleUrl: './login-page.css',
})
export class LoginPageComponent {
  private readonly authApi = inject(AuthApiService);
  private readonly tokenStore = inject(TokenStore);
  private readonly router = inject(Router);
  private readonly fb = inject(FormBuilder);

  readonly error = signal<string | null>(null);

  readonly form = this.fb.group({
    username: ['', Validators.required],
    password: ['', Validators.required],
  });

  submit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }
    const { username, password } = this.form.getRawValue();
    this.authApi.login(username!, password!).subscribe({
      next: ({ accessToken }) => {
        this.tokenStore.setToken(accessToken, username!);
        this.router.navigate(['/holdings']);
      },
      error: () => this.error.set('Invalid username or password'),
    });
  }
}
