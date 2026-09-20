import { Injectable, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, switchMap, of } from 'rxjs';

export interface OrderRequest {
  ticker: string;
  instrumentType: string;
  quantity: number;
  price: number;
  side: 'BUY' | 'SELL';
}

export interface OrderResponse {
  status: string;
  fee: number;
  newHoldingQuantity: number;
}

// Module 15 builds the real login form and JWT interceptor - this is a
// deliberately minimal stand-in so today can focus on the mission service
// call itself, not on building auth UI a second time.
const AUTH_URL = 'http://localhost:3000/auth/login';
const MISSION_URL = 'http://localhost:8090/accounts/1/orders';

@Injectable({
  providedIn: 'root',
})
export class MissionApi {
  private readonly http = inject(HttpClient);

  readonly lastOrder = signal<OrderResponse | null>(null);
  readonly error = signal<string | null>(null);

  submitOrder(order: OrderRequest): void {
    this.error.set(null);

    this.http
      .post<{ accessToken: string }>(AUTH_URL, { username: 'alice', password: 'mission123' })
      .pipe(
        switchMap((auth) =>
          this.http.post<OrderResponse>(MISSION_URL, order, {
            headers: { Authorization: `Bearer ${auth.accessToken}` },
          }),
        ),
        catchError((error) => {
          this.error.set(`Order failed: ${error.message}`);
          return of(null);
        }),
      )
      .subscribe((response) => {
        if (response) {
          this.lastOrder.set(response);
        }
      });
  }
}
