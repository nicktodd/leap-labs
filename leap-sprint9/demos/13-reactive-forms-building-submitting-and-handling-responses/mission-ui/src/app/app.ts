import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HoldingsSummary } from './holdings-summary/holdings-summary';
import { PortfolioBadge } from './portfolio-badge/portfolio-badge';
import { PlaceOrder } from './place-order/place-order';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, HoldingsSummary, PortfolioBadge, PlaceOrder],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('mission-ui');
}
