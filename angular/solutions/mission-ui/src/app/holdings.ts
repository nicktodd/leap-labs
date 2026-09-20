import { Injectable, signal, computed, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, of } from 'rxjs';

export interface Holding {
  ticker: string;
  quantity: number;
  price: number;
}

@Injectable({
  providedIn: 'root',
})
export class Holdings {
  private readonly http = inject(HttpClient);

  private readonly holdings = signal<Holding[]>([
    { ticker: 'ULVR.L', quantity: 500, price: 42.1 },
    { ticker: 'AZN.L', quantity: 120, price: 108.5 },
  ]);

  readonly all = this.holdings.asReadonly();

  readonly totalValue = computed(() =>
    this.holdings().reduce((sum, h) => sum + h.quantity * h.price, 0),
  );

  readonly loadError = signal<string | null>(null);

  add(holding: Holding): void {
    this.holdings.update((current) => [...current, holding]);
  }

  remove(ticker: string): void {
    this.holdings.update((current) => current.filter((h) => h.ticker !== ticker));
  }

  // Sets a holding's quantity to an authoritative value from the backend
  // (e.g. after an order), rather than adding on top of a possibly-stale
  // local figure. Adds the ticker if it wasn't already held.
  setQuantity(ticker: string, quantity: number, price: number): void {
    this.holdings.update((current) => {
      const existing = current.find((h) => h.ticker === ticker);
      if (existing) {
        return current.map((h) => (h.ticker === ticker ? { ...h, quantity, price } : h));
      }
      return [...current, { ticker, quantity, price }];
    });
  }

  loadFromApi(url: string): void {
    this.http
      .get<Holding[]>(url)
      .pipe(
        catchError((error) => {
          this.loadError.set(`Could not load holdings: ${error.message}`);
          return of(null);
        }),
      )
      .subscribe((data) => {
        if (data) {
          this.loadError.set(null);
          this.holdings.set(data);
        }
      });
  }
}
