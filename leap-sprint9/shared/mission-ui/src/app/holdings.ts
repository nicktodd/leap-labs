import { Injectable, computed, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, of } from 'rxjs';

interface Holding {
  ticker: string;
  quantity: number;
  price: number;
}

@Injectable({ providedIn: 'root' })
export class Holdings {
  private readonly http = inject(HttpClient);

  private readonly holdings = signal<Holding[]>([
    { ticker: 'AAPL', quantity: 10, price: 195.5 },
    { ticker: 'MSFT', quantity: 5, price: 420.0 },
  ]);

  readonly all = this.holdings.asReadonly();

  readonly totalValue = computed(() =>
    this.holdings().reduce((sum, h) => sum + h.quantity * h.price, 0)
  );

  readonly loadError = signal<string | null>(null);

  add(): void {
    this.holdings.update((current) => [
      ...current,
      { ticker: 'GOOGL', quantity: 2, price: 175.0 },
    ]);
  }

  remove(ticker: string): void {
    this.holdings.update((current) => current.filter((h) => h.ticker !== ticker));
  }

  updateQuantity(ticker: string, newQuantity: number): void {
    this.holdings.update((current) =>
      current.map((h) => h.ticker === ticker ? { ...h, quantity: newQuantity } : h)
    );
  }

  loadFromApi(url: string): void {
    this.http.get<Holding[]>(url).pipe(
      catchError((err) => {
        this.loadError.set(`${err.message} (${err.status})`);
        return of(null);
      })
    ).subscribe((data) => {
      if (data) {
        this.loadError.set(null);
        this.holdings.set(data);
      }
    });
  }
}
