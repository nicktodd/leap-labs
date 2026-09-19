import { Injectable, inject, signal } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';
import { catchError, of } from 'rxjs';
import { OrderControllerService, OrderRequestDto, OrderResponseDto } from './generated/mission-api-client';

const ACCOUNT_ID = 1;

@Injectable({
  providedIn: 'root',
})
export class MissionApi {
  private readonly orderApi = inject(OrderControllerService);

  readonly lastOrder = signal<OrderResponseDto | null>(null);
  readonly error = signal<string | null>(null);

  submitOrder(order: OrderRequestDto): void {
    this.error.set(null);

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
        if (response) {
          this.lastOrder.set(response);
        }
      });
  }
}
