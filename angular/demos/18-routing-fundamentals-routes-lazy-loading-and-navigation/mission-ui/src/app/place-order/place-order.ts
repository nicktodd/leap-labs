import { Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { MissionApi } from '../mission-api';

@Component({
  selector: 'app-place-order',
  imports: [ReactiveFormsModule],
  templateUrl: './place-order.html',
  styleUrl: './place-order.css',
})
export class PlaceOrder {
  private readonly missionApi = inject(MissionApi);
  private readonly fb = inject(FormBuilder);

  protected readonly lastOrder = this.missionApi.lastOrder;
  protected readonly error = this.missionApi.error;

  // Client-side validation - the same instincts Day 1's native HTML forms
  // taught (required, minimum values), just expressed through Angular's
  // reactive layer instead of HTML attributes.
  protected readonly orderForm = this.fb.group({
    ticker: ['ULVR.L', Validators.required],
    instrumentType: ['EQUITY', Validators.required],
    quantity: [1, [Validators.required, Validators.min(0.01)]],
    price: [40.0, [Validators.required, Validators.min(0.01)]],
    side: ['BUY', Validators.required],
  });

  protected submit(): void {
    if (this.orderForm.invalid) {
      this.orderForm.markAllAsTouched();
      return;
    }

    const { ticker, instrumentType, quantity, price, side } = this.orderForm.getRawValue();
    this.missionApi.submitOrder({
      ticker: ticker!,
      instrumentType: instrumentType!,
      quantity: quantity!,
      price: price!,
      side: side!,
    });
  }
}
