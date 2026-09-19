import { Component, signal, inject } from '@angular/core';
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
  protected readonly tokenStore = inject(TokenStore);
  private readonly router = inject(Router);

  protected logout(): void {
    this.tokenStore.clear();
    this.router.navigate(['/login']);
  }
}
