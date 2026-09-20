import { Injectable, inject, signal } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { catchError, switchMap, of } from 'rxjs';
import { OrderControllerService, OrderRequestDto, OrderResponseDto } from './generated/mission-api-client';

// Module 15 builds the real login form and JWT interceptor - this is a
// deliberately minimal stand-in so today can focus on the mission service
// call itself, not on building auth UI a second time.
const AUTH_URL = 'http://localhost:3000/auth/login';
const ACCOUNT_ID = 1;

@Injectable({
  providedIn: 'root',
})
export class MissionApi {
  private readonly http = inject(HttpClient);
  private readonly orderApi = inject(OrderControllerService);

  readonly lastOrder = signal<OrderResponseDto | null>(null);
  readonly error = signal<string | null>(null);

  submitOrder(order: OrderRequestDto): void {
    this.error.set(null);

    this.http
      .post<{ accessToken: string }>(AUTH_URL, { username: 'alice', password: 'mission123' })
      .pipe(
        switchMap((auth) => {
          // Setting credentials on the generated client's configuration,
          // once the token is known - Module 15's interceptor replaces
          // this exact line with something automatic, on every request.
          this.orderApi.configuration.credentials = {
            bearerAuth: () => auth.accessToken,
          };
          return this.orderApi.submitOrder(ACCOUNT_ID, order);
        }),
        catchError((error: HttpErrorResponse) => {
          // The mission service's GlobalExceptionHandler always returns a
          // real ErrorResponse body ({ status, error, message, path }) -
          // error.message here is just Angular's generic "Http failure
          // response for ..." wrapper, not what the SERVER actually said.
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
