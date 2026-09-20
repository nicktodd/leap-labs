import { Component, inject } from '@angular/core';
import { DecimalPipe } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, Validators } from '@angular/forms';
import { MissionApiService } from '../mission-api';

@Component({
  selector: 'app-place-order',
  standalone: true,
  imports: [DecimalPipe, ReactiveFormsModule],
  templateUrl: './place-order.html',
  styleUrl: './place-order.css',
})
export class PlaceOrderComponent {
  readonly svc = inject(MissionApiService);
  private readonly fb = inject(FormBuilder);

  readonly form = this.fb.group({
    ticker: ['', Validators.required],
    instrumentType: ['', Validators.required],
    quantity: [null as number | null, [Validators.required, Validators.min(0.01)]],
    price: [null as number | null, [Validators.required, Validators.min(0.01)]],
    side: ['', Validators.required],
  });

  submit(): void {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }
    const v = this.form.getRawValue();
    this.svc.submitOrder({
      ticker: v.ticker!,
      instrumentType: v.instrumentType!,
      quantity: v.quantity!,
      price: v.price!,
      side: v.side!,
      buy: v.side === 'BUY',
    });
  }
}
