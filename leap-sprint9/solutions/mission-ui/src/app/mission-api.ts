import { Injectable, inject, signal } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { catchError, of } from 'rxjs';
import { OrderControllerService, OrderRequestDto, OrderResponseDto } from './generated/mission-api-client';
import { Holdings } from './holdings';

const ACCOUNT_ID = 1;

@Injectable({
  providedIn: 'root',
})
export class MissionApi {
  private readonly orderApi = inject(OrderControllerService);
  private readonly holdings = inject(Holdings);

  readonly lastOrder = signal<OrderResponseDto | null>(null);
  readonly error = signal<string | null>(null);
  readonly submitting = signal(false);

  submitOrder(order: OrderRequestDto): void {
    this.error.set(null);
    this.submitting.set(true);

    // No login call, no manually-set credentials here - authInterceptor
    // attaches the Authorization header to this request automatically,
    // reading the token from TokenStore.
    this.orderApi
      .submitOrder(ACCOUNT_ID, order)
      .pipe(
        catchError((error: HttpErrorResponse) => {
          const serverMessage = error.error?.message;
          this.error.set(`Order failed: ${serverMessage ?? error.message}`);
          return of(null);
        }),
      )
      .subscribe((response) => {
        this.submitting.set(false);
        if (response) {
          this.lastOrder.set(response);
          // The order response is the source of truth for the resulting
          // position - Holdings previously had no idea an order had even
          // been placed, so the badge and holdings list silently drifted
          // from what the backend actually recorded.
          if (response.newHoldingQuantity !== undefined) {
            this.holdings.setQuantity(order.ticker, response.newHoldingQuantity, order.price ?? 0);
          }
        }
      });
  }
}
