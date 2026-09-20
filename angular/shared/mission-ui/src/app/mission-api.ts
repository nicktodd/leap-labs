import { Injectable, inject, signal } from '@angular/core';
import { catchError, finalize, of } from 'rxjs';
import { OrderControllerService, OrderRequestDto, OrderResponseDto } from './generated/mission-api-client';
import { Holdings } from './holdings';

export type { OrderRequestDto, OrderResponseDto };

@Injectable({ providedIn: 'root' })
export class MissionApiService {
  private readonly orderApi = inject(OrderControllerService);
  private readonly holdingsStore = inject(Holdings);

  readonly lastOrder = signal<OrderResponseDto | null>(null);
  readonly error = signal<string | null>(null);
  readonly pending = signal(false);

  submitOrder(order: OrderRequestDto): void {
    this.pending.set(true);
    this.orderApi.submitOrder(1, order).pipe(
      catchError((err) => {
        const msg = err.error?.message ?? err.message;
        this.error.set(`${msg} (${err.status})`);
        return of(null);
      }),
      finalize(() => this.pending.set(false)),
    ).subscribe((res) => {
      if (res) {
        this.error.set(null);
        this.lastOrder.set(res);
        if (order.ticker && res.newHoldingQuantity != null) {
          this.holdingsStore.updateQuantity(order.ticker, res.newHoldingQuantity);
        }
      }
    });
  }
}
