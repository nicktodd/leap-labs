import { Component, inject } from '@angular/core';
import { DecimalPipe } from '@angular/common';
import { Holdings } from '../holdings';

const API_BASE = 'http://localhost:3500/api/holdings';

@Component({
  selector: 'app-holdings-summary',
  imports: [DecimalPipe],
  templateUrl: './holdings-summary.html',
  styleUrl: './holdings-summary.css',
})
export class HoldingsSummary {
  private readonly holdingsService = inject(Holdings);

  protected readonly holdings = this.holdingsService.all;
  protected readonly totalValue = this.holdingsService.totalValue;
  protected readonly loadError = this.holdingsService.loadError;

  protected addHolding(): void {
    this.holdingsService.add({ ticker: 'BP.L', quantity: 200, price: 4.8 });
  }

  protected removeHolding(ticker: string): void {
    this.holdingsService.remove(ticker);
  }

  protected loadFromApi(): void {
    this.holdingsService.loadFromApi(API_BASE);
  }

  protected simulateApiError(): void {
    this.holdingsService.loadFromApi(`${API_BASE}/error`);
  }
}
