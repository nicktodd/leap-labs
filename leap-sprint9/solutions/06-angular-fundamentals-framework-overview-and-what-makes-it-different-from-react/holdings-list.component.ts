import { Component, inject, signal, effect } from '@angular/core';
import { Router } from '@angular/router';

interface Holding {
  ticker: string;
  quantity: number;
}

@Component({
  selector: 'app-holdings-list',
  standalone: true,
  template: `
    <ul>
      @for (holding of holdings(); track holding.ticker) {
        <li>{{ holding.ticker }}: {{ holding.quantity }}</li>
      }
    </ul>
    <button (click)="goToOrders()">Place an Order</button>
  `,
})
export class HoldingsListComponent {
  private router = inject(Router);
  holdings = signal<Holding[]>([]);

  constructor() {
    effect(() => {
      console.log(`Now tracking ${this.holdings().length} holdings`);
    });
  }

  goToOrders(): void {
    this.router.navigate(['/orders']);
  }
}
