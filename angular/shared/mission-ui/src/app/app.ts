import { Component, inject, signal } from '@angular/core';
import { RouterOutlet, RouterLink, RouterLinkActive, Router } from '@angular/router';
import { PortfolioBadge } from './portfolio-badge/portfolio-badge';
import { TokenStore } from './token-store';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterLink, RouterLinkActive, PortfolioBadge],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('mission-ui');
  readonly tokenStore = inject(TokenStore);
  private readonly router = inject(Router);

  logout(): void {
    this.tokenStore.clear();
    this.router.navigate(['/login']);
  }
}
