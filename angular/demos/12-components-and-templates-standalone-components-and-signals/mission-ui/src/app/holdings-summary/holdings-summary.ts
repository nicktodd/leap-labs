import { Component, signal, computed } from '@angular/core';
import { DecimalPipe } from '@angular/common';

interface Holding {
  ticker: string;
  quantity: number;
  price: number;
}

@Component({
  selector: 'app-holdings-summary',
  imports: [DecimalPipe],
  templateUrl: './holdings-summary.html',
  styleUrl: './holdings-summary.css',
})
export class HoldingsSummary {
  protected readonly holdings = signal<Holding[]>([
    { ticker: 'ULVR.L', quantity: 500, price: 42.1 },
    { ticker: 'AZN.L', quantity: 120, price: 108.5 },
  ]);

  protected readonly totalValue = computed(() =>
    this.holdings().reduce((sum, h) => sum + h.quantity * h.price, 0),
  );

  protected addHolding(): void {
    this.holdings.update((current) => [
      ...current,
      { ticker: 'BP.L', quantity: 200, price: 4.8 },
    ]);
  }

  protected removeHolding(ticker: string): void {
    this.holdings.update((current) => current.filter((h) => h.ticker !== ticker));
  }
}
